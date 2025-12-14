# python
# components/toggle_panel.py
from tkinter import BooleanVar
from tkinter.ttk import Frame, Label, Checkbutton

from config import Config


class TogglePanel:
    def __init__(self, master, callbacks=None):
        self.frame = Frame(master)
        self.callbacks = callbacks or {}

        self.show_ticker = BooleanVar(value=Config.SHOW_TICKER)
        self.show_order_book = BooleanVar(value=Config.SHOW_ORDER_BOOK)
        self.show_candlestick = BooleanVar(value=Config.SHOW_CANDLESTICK)
        self.show_recent_trade = BooleanVar(value=Config.SHOW_RECENT_TRADE)
        self.show_best_trade = BooleanVar(value=Config.SHOW_BEST_TRADE)

        self._build()

    def _build(self):
        # Header
        Label(self.frame, text="Toggle Components:", font="Arial 12 bold")\
            .pack(anchor="w", pady=(0, 8), padx=6, fill="x")

        # Checkbuttons packed to fill horizontally so the indicator stays aligned
        Checkbutton(self.frame, text="Tickers", variable=self.show_ticker,
                    command=lambda: self._on_toggle("SHOW_TICKER", self.show_ticker, "ticker"))\
            .pack(anchor="w", pady=2, padx=8, fill="x")
        Checkbutton(self.frame, text="Order Book", variable=self.show_order_book,
                    command=lambda: self._on_toggle("SHOW_ORDER_BOOK", self.show_order_book, "order_book"))\
            .pack(anchor="w", pady=2, padx=8, fill="x")
        Checkbutton(self.frame, text="Candlestick", variable=self.show_candlestick,
                    command=lambda: self._on_toggle("SHOW_CANDLESTICK", self.show_candlestick, "candlestick"))\
            .pack(anchor="w", pady=2, padx=8, fill="x")
        Checkbutton(self.frame, text="Recent Trade", variable=self.show_recent_trade,
                    command=lambda: self._on_toggle("SHOW_RECENT_TRADE", self.show_recent_trade, "recent_trade"))\
            .pack(anchor="w", pady=2, padx=8, fill="x")
        Checkbutton(self.frame, text="Best Trade", variable=self.show_best_trade,
                    command=lambda: self._on_toggle("SHOW_BEST_TRADE", self.show_best_trade, "best_trade"))\
            .pack(anchor="w", pady=2, padx=8, fill="x")

    def _on_toggle(self, config_key, var, cb_key):
        Config.update(config_key, var.get())
        cb = self.callbacks.get(cb_key)
        if callable(cb):
            cb()

    def pack(self, **kwargs):
        # Defaults anchor the panel at the bottom and stretch horizontally.
        defaults = {"side": "bottom", "anchor": "s", "fill": "x"}
        defaults.update(kwargs)
        self.frame.pack(**defaults)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)