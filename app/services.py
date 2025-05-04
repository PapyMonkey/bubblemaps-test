from typing import Any, Dict, List

import httpx

from app import models

# Base URL for the Dexscreener API
BASE_URL = "https://api.dexscreener.com/token-pairs/v1/"


async def fetch_pairs_for_token(
    chain_id: str, token_address: str
) -> List[Dict[str, Any]]:
    """
    Query the Dexscreener API and return a list of liquidity pools (pairs)
    for the specified blockchain "chain" and token "address".
    """
    url = f"{BASE_URL}/{chain_id}/{token_address}"

    async with httpx.AsyncClient(timeout=10) as http_client:
        response = await http_client.get(url)
        response.raise_for_status()
        response_data = response.json()

    return response_data


def compute_aggregates(pool_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute the following aggregated metrics for the given list of pools:
      - largest_pool: details of the pool with the highest liquidity
      - aggregated_liquidity: total combined liquidity across all pools
      - number_of_pools: count of pools in the list
    """
    if not pool_list:
        return {"largest_pool": None, "aggregated_liquidity": 0.0, "number_of_pools": 0}

    # Extract and convert all pool[liquidity][usd] into a float
    for pool_data in pool_list:
        extracted_usd = pool_data.get("liquidity", {}).get("usd", 0.0)
        pool_data["liquidityUsd"] = float(extracted_usd)

    # Total number of pools for this token
    total_pools = len(pool_list)

    # Sum of all liquidities in USD across pools
    total_liquidity = sum(pool_data["liquidityUsd"] for pool_data in pool_list)

    # Identify the pool having the maximum liquidity
    pool_with_max = max(pool_list, key=lambda pool_data: pool_data["liquidityUsd"])
    largest_pool_info = {
        "pairId": pool_with_max.get("pairAddress"),
        "dexId": pool_with_max.get("dexId"),
        "liquidity": pool_with_max["liquidityUsd"],
        "baseToken": pool_with_max.get("baseToken", {}),
        "quoteToken": pool_with_max.get("quoteToken", {}),
    }

    return {
        "largest_pool": largest_pool_info,
        "aggregated_liquidity": total_liquidity,
        "number_of_pools": total_pools,
    }


async def get_token_info(chain_id: str, token_address: str) -> models.TokenInfo:
    """
    Orchestrate retrieving pool data and computing aggregated metrics for
    a given token specified by its blockchain "chainId" and "tokenAddress".
    Based on Dexscreener.
    """
    # Retrieve the list of pools from Dexscreener
    pool_data_list = await fetch_pairs_for_token(chain_id, token_address)

    # Compute aggregated metrics
    aggregates = compute_aggregates(pool_data_list)

    # Construct and return the Pydantic TokenInfo model
    if aggregates["largest_pool"]:
        largest_pool = models.PoolInfo(**aggregates["largest_pool"])
    else:
        largest_pool = None

    return models.TokenInfo(
        chain=chain_id,
        address=token_address,
        largest_pool=largest_pool,
        aggregated_liquidity=aggregates["aggregated_liquidity"],
        number_of_pools=aggregates["number_of_pools"],
    )
