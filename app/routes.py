from fastapi import APIRouter

from app import models, services

router = APIRouter()


@router.get("/token/{chain}/{address}", response_model=models.TokenInfo)
async def get_token_info(chain: str, address: str):
    return await services.get_token_info(chain, address)
