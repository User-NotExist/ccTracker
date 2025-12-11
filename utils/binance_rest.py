import logging
import requests


class BinanceRest:
    BASE_URL = "https://api.binance.com"

    def __init__(self, base_url=None , timeout: float = 10.0):
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self._session = requests.Session()

    def _build_url(self, path: str):
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def request(self, method: str, path: str, **kwargs):
        url = self._build_url(path)
        try:
            response = self._session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            logging.error("Binance request failed: %s", exc)
            raise

if __name__ == "__main__":
    # Example usage
    binance = BinanceRest()
    # try get 50 latest orders for BTCUSDT
    orders = binance.request("GET", "/api/v3/depth", params={"symbol": "BTCUSDT", "limit": 50})
    print(orders)
    # check ratelimit status
    status = binance.request("GET", "/api/v3/exchangeInfo")
    print(status["rateLimits"])