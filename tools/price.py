# tools/price.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RECALL_API_KEY")
BASE_URL = os.getenv("RECALL_API_URL", "https://api.competitions.recall.network")

# ✅ Token addresses required by the Recall API
TOKEN_ADDRESSES = {
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "DAI":  "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
}

def get_token_price(symbol, chain="evm", specific_chain="eth"):
    """
    Get token price from Recall API
    
    Args:
        symbol (str): Token symbol (USDC, DAI, WETH)
        chain (str): Blockchain type (default: "evm")
        specific_chain (str): Specific chain (default: "eth")
    
    Returns:
        float: Token price in USD, or 0.0 if error
    """
    token_address = TOKEN_ADDRESSES.get(symbol.upper())
    if not token_address:
        print(f"❌ Unknown token symbol: {symbol}")
        return 0.0

    url = f"{BASE_URL}/api/price"
    params = {
        "token": token_address,
        "chain": chain,
        "specificChain": specific_chain
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("success") and "price" in result:
            price = float(result["price"])
            print(f"💰 {symbol} price: ${price:.4f}")
            return price
        else:
            print(f"❌ Price API error for {symbol}: {result.get('error', 'Unknown error')}")
            return 0.0
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error fetching {symbol} price: {e}")
        return 0.0
    except Exception as e:
        print(f"❌ Error fetching {symbol} price: {e}")
        return 0.0

def get_all_prices():
    """
    Get prices for all supported tokens
    
    Returns:
        dict: Dictionary with token symbols as keys and prices as values
    """
    prices = {}
    for token in TOKEN_ADDRESSES.keys():
        prices[token] = get_token_price(token)
    return prices

if __name__ == "__main__":
    # Test the price fetching
    print("🧪 Testing price fetching...")
    
    for token in TOKEN_ADDRESSES.keys():
        price = get_token_price(token)
        print(f"{token}: ${price:.4f}")
    
    print("\nAll prices:", get_all_prices())