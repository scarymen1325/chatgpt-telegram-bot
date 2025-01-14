from typing import Dict
import aiohttp

class CryptoPlugin:
    """
    A plugin to fetch the current rate of various cryptocurrencies using CoinGecko API.
    """
    def get_source_name(self) -> str:
        return "CoinGecko"

    def get_spec(self) -> list[Dict]:
        return [{
            "name": "get_crypto_rate",
            "description": "Get the current rate of various cryptocurrencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "asset": {"type": "string", "description": "Asset of the cryptocurrency (e.g., bitcoin, ethereum)"}
                },
                "required": ["asset"],
            },
        }]

    async def execute(self, function_name: str, helper: object, **kwargs) -> Dict:
        """
        Fetch the cryptocurrency rate using CoinGecko API.

        Args:
            function_name (str): The name of the function being executed.
            helper (object): Helper object for plugin integration.
            **kwargs: Additional parameters (e.g., 'asset').

        Returns:
            Dict: JSON response with success or error message.
        """
        asset = kwargs.get('asset')
        if not asset:
            return {
                "status": "error",
                "message": "Asset parameter is required."
            }

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={asset.lower()}&vs_currencies=usd"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        return {
                            "status": "error",
                            "message": f"HTTP Error {response.status}: Unable to fetch data."
                        }
                    data = await response.json()
                    return {
                        "status": "success",
                        "data": {"asset": asset, "price_usd": data.get(asset.lower(), {}).get("usd")}
                    }
            except aiohttp.ClientError as e:
                return {
                    "status": "error",
                    "message": f"Network request failed: {str(e)}"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}"
                }
