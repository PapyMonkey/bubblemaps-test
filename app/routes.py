import asyncio
from typing import List

from fastapi import APIRouter

from app import models, services

router = APIRouter()


@router.get(
    "/token/{chain}/{address}",
    response_model=models.TokenInfo,
    summary="Fetch aggregated info for a single token",
)
async def get_single_token_info(chain: str, address: str):
    """
    Returns TokenInfo (largest pool, total liquidity, count)
    for the specified chain and token address.
    """
    return await services.get_token_info(chain, address)


@router.post(
    "/tokens/info",
    response_model=List[models.TokenInfo],
    summary="Fetch aggregated info for multiple tokens",
)
async def get_multiple_tokens_info(request: models.TokensBatchRequest):
    """
    Returns a list of TokenInfo for each chain/address pair
    provided in the request body.
    """
    tasks = []

    for token_request in request.tokens:
        task = services.get_token_info(token_request.chain, token_request.address)
        tasks.append(task)
    return await asyncio.gather(*tasks)
