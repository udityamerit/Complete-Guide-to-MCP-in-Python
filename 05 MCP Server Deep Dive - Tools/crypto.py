# /// script
# dependencies = [
#   "requests",
# ]
# ///

from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("Crypto")

@mcp.tool()
def get_cryptocurrency_price(crypto: str) -> str:
    """
    Gets the price of a cryptocurrency.

    Args:
        crypto: name of cryptocurrency
        (e.g. bitcoin, ethereum, dogecoin)
    """

    try:
        crypto = crypto.strip().lower()

        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": crypto,
            "vs_currencies": "usd,inr"
        }

        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        if crypto in data:

            usd_price = data[crypto]["usd"]
            inr_price = data[crypto]["inr"]

            return (
                f"The price of {crypto} is "
                f"${usd_price} USD "
                f"and ₹{inr_price} INR."
            )

        else:
            return f"Price for {crypto} not found."

    except Exception as e:
        return f"Error fetching price for {crypto}: {e}"


if __name__ == "__main__":
    mcp.run()