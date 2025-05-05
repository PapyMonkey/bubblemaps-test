# Bubblemaps Technical Test

## Token Info API

This service provides aggregated liquidity information for SPL tokens (solana) via the [Dexscreener API](https://docs.dexscreener.com/api/reference). It exposes two endpoints:

- **GET** `/token/{chain}/{address}`
  Fetch info for a single token.
- **POST** `/tokens/info`
  Fetch info in batch for multiple tokens.

---

## Prerequisites

- Python 3.11
- Docker (for containerization)
- `gcloud` CLI (for deployment on Google Cloud Platform)

---

## Installation

1. Clone the repo and enter the directory:

   ```bash
   git clone https://github.com/papymonkey/bubblemaps-test.git
   cd bubblemaps-test
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Usage/Endpoints

### 1. Single token

```
GET /token/{chain}/{address}
```

- **Path parameters**

  - `chain` (string): e.g. `solana`
  - `address` (string): e.g. `FQgtfugBdpFN7PZ6NdPrZpVLDBrPGxXesi4gVu3vErhY`

- **Success (200)**

  ```json
  {
    "chain": "solana",
    "address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "largest_pool": {
      "pairId": "C1MgLojNLWBKADvu9BHdtgzz1oZX4dZ5zGdGcgvvW8Wz",
      "liquidity": 1446848.24,
      "baseToken": {
        "address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "name": "Jupiter",
        "symbol": "JUP"
      },
      "quoteToken": {
        "address": "So11111111111111111111111111111111111111112",
        "name": "Wrapped SOL",
        "symbol": "SOL"
      }
    },
    "aggregated_liquidity": 4392335.14,
    "number_of_pools": 30
  }
  ```

### 2. Batch tokens

```
POST /tokens/info
Content-Type: application/json

{
  "tokens": [
    { "chain": "solana", "address": "JUPyiw…CN" },
    { "chain": "solana", "address": "EPjFWd…hi" }
  ]
}
```

- **Success (200)**
  Returns an array of the same objects as the single endpoint, in order.

---

## Assumptions

- Only **Solana** (`chainId = "solana"`) is supported.
- **Dexscreener API** endpoints are public (no API key required).
- Tokens with zero pools return a valid `200` with `"largest_pool": null`.
- Batch calls execute **concurrently** via `asyncio.gather`.
- No authentication is implemented (public API).
