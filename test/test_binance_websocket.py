import unittest
from unittest.mock import MagicMock, patch
from utils.binance_websocket import BinanceWebSocket

class TestBinanceWebSocket(unittest.TestCase):
    def test_websocket_receives_message(self):
        ws = BinanceWebSocket("btcusdt", "ticker")
        ws.message_received = MagicMock()
        ws._on_message(None, '{"data": "test message"}')
        ws.message_received.assert_called_once_with('{"data": "test message"}')

    def test_websocket_handles_error(self):
        ws = BinanceWebSocket("btcusdt", "ticker")
        ws.error_received = MagicMock()
        ws._on_error(None, "Test error")
        ws.error_received.assert_called_once_with("Test error")

    def test_websocket_closes_correctly(self):
        ws = BinanceWebSocket("btcusdt", "ticker")
        ws.disconnected = MagicMock()
        ws._on_close(None, 1000, "Normal closure")
        ws.disconnected.assert_called_once()

    def test_websocket_url_is_correct(self):
        ws = BinanceWebSocket("btcusdt", "ticker")
        self.assertEqual(ws.get_url(), "wss://stream.binance.com:9443/ws/btcusdt@ticker")

    def test_websocket_does_not_reconnect_if_active(self):
        ws = BinanceWebSocket("btcusdt", "ticker")
        ws.thread = MagicMock(is_alive=MagicMock(return_value=True))
        with patch("websocket.WebSocketApp.run_forever", return_value=None):
            ws.connect()
        ws.thread.is_alive.assert_called_once()


if __name__ == "__main__":
    unittest.main()