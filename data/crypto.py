from utils.event import Event
from utils.binance_websocket import BinanceWebSocket
from utils.binance_rest import BinanceRest

class Crypto:
    def __init__(self, symbol: str):
        """Initialize the Crypto instance, setting the trading pair symbol."""
        self.symbol = symbol

        self.ws_ticker = BinanceWebSocket(symbol, 'ticker')
        self.ws_trade = BinanceWebSocket(symbol, 'trade')
        self.ws_kline_1m = BinanceWebSocket(symbol, 'kline_1m')
        self.ws_depth = BinanceWebSocket(symbol, 'depth')
        self.ws_aggregate_trade = BinanceWebSocket(symbol, 'aggTrade')

        self.rest_helper = BinanceRest()

    def connect_all(self):
        """Establish WebSocket connections for all data streams."""
        self.ws_trade.connect()
        self.ws_kline_1m.connect()
        self.ws_depth.connect()
        self.ws_aggregate_trade.connect()

    def close_all(self):
        """Close all WebSocket connections."""
        self.ws_trade.close()
        self.ws_kline_1m.close()
        self.ws_depth.close()
        self.ws_aggregate_trade.close()