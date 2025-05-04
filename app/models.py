from typing import Any, Dict, Optional

from pydantic import BaseModel


class PoolInfo(BaseModel):
    pairId: str
    liquidity: float
    baseToken: Dict[str, Any]
    quoteToken: Dict[str, Any]

class TokenInfo(BaseModel):
    chain: str
    address: str
    largest_pool: Optional[PoolInfo]
    aggregated_liquidity: float
    number_of_pools: int
