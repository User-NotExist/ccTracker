from utils.event import Event
import websocket
import threading
import logging

class BinanceWebSocket:
    """
    A class to manage WebSocket connections to the Binance API for a specific trading pair and stream type.

    Attributes:
        BASE_URL (str): The base URL for Binance WebSocket streams.
        symbol (str): The trading pair symbol (e.g., 'btcusdt').
        stream_type (str): The type of stream (e.g., 'trade', 'kline_1m').
        url (str): The full WebSocket URL for the specified symbol and stream type.
        connected (Event): Event triggered when the WebSocket connection is established.
        message_received (Event): Event triggered when a message is received from the WebSocket.
        error_occurred (Event): Event triggered when an error occurs in the WebSocket connection.
        disconnected (Event): Event triggered when the WebSocket connection is closed.
        ws (websocket.WebSocketApp): The WebSocket client instance.
        thread (threading.Thread): The thread running the WebSocket connection.
        active (bool): Indicates whether the WebSocket connection is active.
    """

    BASE_URL = 'wss://stream.binance.com:9443/ws/'

    def __init__(self, symbol: str, stream_type: str):
        """
        Initialize the BinanceWebSocket instance.

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
        """
        Establish the WebSocket connection and start listening for messages.

        If a connection thread is already active, this method does nothing.
        """
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
        """
        Get the WebSocket URL for the specified symbol and stream type.

        Returns:
            str: The WebSocket URL.
        """
        return self.url

    def close(self):
        """
        Close the WebSocket connection.

        If the WebSocket client instance is not None, it will be closed.
        """
        if self.ws is not None:
            self.ws.close()

    def _on_open(self, ws):
        """
        Callback for when the WebSocket connection is opened.

        Args:
            ws (websocket.WebSocketApp): The WebSocket client instance.
        """
        print(f"WebSocket connection {self.symbol}@{self.stream_type} opened.")
        self.active = True
        self.connected()

    def _on_message(self, ws, message):
        """
        Callback for when a message is received from the WebSocket.

        Args:
            ws (websocket.WebSocketApp): The WebSocket client instance.
            message (str): The message received from the WebSocket.
        """
        self.message_received(message)

    def _on_error(self, ws, error):
        """
        Callback for when an error occurs in the WebSocket connection.

        Args:
            ws (websocket.WebSocketApp): The WebSocket client instance.
            error (Exception): The error that occurred.
        """
        print(f"WebSocket error: {error}")
        self.error_occurred(error)

    def _on_close(self, ws, status, msg):
        """
        Callback for when the WebSocket connection is closed.

        Args:
            ws (websocket.WebSocketApp): The WebSocket client instance.
            status (int): The status code of the closure.
            msg (str): The reason for the closure.
        """
        print(f"WebSocket connection {self.symbol}@{self.stream_type} closed.")
        self.active = False
        self.ws = None
        self.disconnected()
