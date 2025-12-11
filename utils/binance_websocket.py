from utils.event import Event
import websocket
import threading
import logging

class BinanceWebSocket:
    BASE_URL = 'wss://stream.binance.com:9443/ws/'

    def __init__(self, symbol: str, stream_type: str):
        """Initialize the BinanceWebSocket instance.

        Args:
            symbol (str): The trading pair symbol (e.g., 'btcusdt').
            stream_type (str): The type of stream (e.g., 'trade', 'kline_1m').
        """
        self.symbol = symbol.lower()
        self.stream_type = stream_type
        self.url = f"{self.BASE_URL}{self.symbol}@{self.stream_type}"

        self.connected = Event()
        self.message_received = Event()
        self.error_occurred = Event()
        self.disconnected = Event()

        self.ws = None
        self.thread = None
        self.active = False

    def connect(self):
        """Establish the WebSocket connection and start listening for messages."""
        if self.thread and self.thread.is_alive():
            return

        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
                )

        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def get_url(self) -> str:
        """Get the WebSocket URL for the specified symbol and stream type.

        Returns:
            str: The WebSocket URL.
        """
        return self.url

    def close(self):
        """Close the WebSocket connection."""
        if self.ws is not None:
            self.ws.close()

    def _on_open(self, ws):
        print(f"WebSocket connection {self.symbol}@{self.stream_type} opened.")
        self.active = True
        self.connected()

    def _on_message(self, ws, message):
        self.message_received(message)

    def _on_error(self, ws, error):
        print(f"WebSocket error: {error}")
        self.error_occurred(error)

    def _on_close(self, ws, status, msg):
        print(f"WebSocket connection {self.symbol}@{self.stream_type} closed.")
        self.active = False
        self.ws = None
        self.disconnected()
