import json
from pathlib import Path


class Config:
    CRYPTO_LIST = ['BTCUSDT', 'ADAUSDT', 'SOLUSDT', 'DOGEUSDT', 'TRXUSDT']
    STARTING_RESOLUTION = '1600x900'
    WINDOW_TITLE = "Crypto Dashboard"

    # Toggle preferences
    SHOW_TICKER = True
    SHOW_ORDER_BOOK = True
    SHOW_CANDLESTICK = True
    SHOW_RECENT_TRADE = True
    SHOW_BEST_TRADE = True

    # Last selected crypto
    LAST_SELECTED_CRYPTO = 'BTCUSDT'

    CONFIG_FILE = Path("config.json")

    @classmethod
    def to_dict(cls):
        return {
            "CRYPTO_LIST": cls.CRYPTO_LIST,
            "STARTING_RESOLUTION": cls.STARTING_RESOLUTION,
            "WINDOW_TITLE": cls.WINDOW_TITLE,
            "SHOW_TICKER": cls.SHOW_TICKER,
            "SHOW_ORDER_BOOK": cls.SHOW_ORDER_BOOK,
            "SHOW_CANDLESTICK": cls.SHOW_CANDLESTICK,
            "SHOW_RECENT_TRADE": cls.SHOW_RECENT_TRADE,
            "SHOW_BEST_TRADE": cls.SHOW_BEST_TRADE,
            "LAST_SELECTED_CRYPTO": cls.LAST_SELECTED_CRYPTO
        }

    @classmethod
    def save(cls):
        cls.CONFIG_FILE.write_text(json.dumps(cls.to_dict(), indent=4))

    @classmethod
    def load(cls):
        if not cls.CONFIG_FILE.exists():
            cls.save()
            return

        data = json.loads(cls.CONFIG_FILE.read_text())

        cls.CRYPTO_LIST = data.get("CRYPTO_LIST", cls.CRYPTO_LIST)
        cls.STARTING_RESOLUTION = data.get("STARTING_RESOLUTION", cls.STARTING_RESOLUTION)
        cls.WINDOW_TITLE = data.get("WINDOW_TITLE", cls.WINDOW_TITLE)
        cls.SHOW_TICKER = data.get("SHOW_TICKER", cls.SHOW_TICKER)
        cls.SHOW_ORDER_BOOK = data.get("SHOW_ORDER_BOOK", cls.SHOW_ORDER_BOOK)
        cls.SHOW_CANDLESTICK = data.get("SHOW_CANDLESTICK", cls.SHOW_CANDLESTICK)
        cls.SHOW_RECENT_TRADE = data.get("SHOW_RECENT_TRADE", cls.SHOW_RECENT_TRADE)
        cls.SHOW_BEST_TRADE = data.get("SHOW_BEST_TRADE", cls.SHOW_BEST_TRADE)
        cls.LAST_SELECTED_CRYPTO = data.get("LAST_SELECTED_CRYPTO", cls.LAST_SELECTED_CRYPTO)

    @classmethod
    def update(cls, key, value):
        if hasattr(cls, key):
            setattr(cls, key, value)
            cls.save()
