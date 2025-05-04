import asyncio
from typing import List

import httpx
from fastapi import APIRouter, HTTPException

from app import models, services

router = APIRouter()


@router.get(
    "/token/{chain}/{address}",
    response_model=models.TokenInfo,
    summary="Fetch aggregated info for a single token",
)
async def get_single_token_info(chain_id: str, token_address: str):
    """
    Returns TokenInfo (largest pool, total liquidity, count)
    for the specified chain and token address.
    """
    try:
        return await services.get_token_info(chain_id, token_address)
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail=f"Upstream error fetching {chain_id}:{token_address}",
        )


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

    async def _fetch_one(token_req: models.TokenRequest):
        try:
            return await services.get_token_info(token_req.chain, token_req.address)
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=503,
                detail=f"Upstream error fetching {token_req.chain}:{token_req.address}",
            )

    # New async task for each token
    tasks = [_fetch_one(tok) for tok in request.tokens]
    # Paralleling tasks
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # If a task returns an HTTPException we propagate it here
    for res in results:
        if isinstance(res, HTTPException):
            raise res

    return results
