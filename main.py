from tkinter import Tk, BooleanVar
from tkinter.ttk import Label, Button, Frame, Checkbutton

from components.graph import CandlestickChart
from components.advanced_ticker import AdvancedTickerFrame
from components.order_book import OrderBook
from components.recent_trade import RecentTrade
from components.best_trade import BestTrade

from utils.network_connection_test import check_network

from data.crypto import Crypto
from config import Config
import logging


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1600x900")
        self.crypto_dic = {}
        self.active_crypto = None
        Config.load()

        self.ticker_container = None
        self.center_container = None
        self.right_container = None

        self.ticker_labeled = {}
        self.order_book = None
        self.candlestick_chart = None
        self.recent_trade = None
        self.best_trade = None

        # Toggle variables
        self.show_ticker = BooleanVar(value=Config.SHOW_TICKER)
        self.show_order_book = BooleanVar(value=Config.SHOW_ORDER_BOOK)
        self.show_candlestick = BooleanVar(value=Config.SHOW_CANDLESTICK)
        self.show_recent_trade = BooleanVar(value=Config.SHOW_RECENT_TRADE)
        self.show_best_trade = BooleanVar(value=Config.SHOW_BEST_TRADE)

        self.create_crypto_list()

        self.frame = Frame(self.root)

        self.create_widgets()

    def create_toggle_panel(self):
        toggle_frame = Frame(self.root)
        toggle_frame.pack(pady=5, anchor="nw", padx=10)

        Label(toggle_frame, text="Toggle Components:", font="Arial 12 bold").pack(side="left", padx=(0, 10))

        Checkbutton(toggle_frame, text="Tickers", variable=self.show_ticker,
                    command=self._toggle_ticker).pack(side="left", padx=5)
        Checkbutton(toggle_frame, text="Order Book", variable=self.show_order_book,
                    command=self._toggle_order_book).pack(side="left", padx=5)
        Checkbutton(toggle_frame, text="Candlestick", variable=self.show_candlestick,
                    command=self._toggle_candlestick).pack(side="left", padx=5)
        Checkbutton(toggle_frame, text="Recent Trade", variable=self.show_recent_trade,
                    command=self._toggle_recent_trade).pack(side="left", padx=5)
        Checkbutton(toggle_frame, text="Best Trade", variable=self.show_best_trade,
                    command=self._toggle_best_trade).pack(side="left", padx=5)

    # Update toggle methods to save preferences:
    def _toggle_ticker(self):
        Config.update("SHOW_TICKER", self.show_ticker.get())
        if self.show_ticker.get():
            self.ticker_container.pack(pady=10, padx=30, anchor="nw", side="left", fill="x",
                                       before=self.center_container)
        else:
            self.ticker_container.pack_forget()

    def _toggle_order_book(self):
        Config.update("SHOW_ORDER_BOOK", self.show_order_book.get())
        if self.show_order_book.get():
            self.order_book.pack(pady=10, fill="x")
        else:
            self.order_book.pack_forget()

    def _toggle_candlestick(self):
        Config.update("SHOW_CANDLESTICK", self.show_candlestick.get())
        if self.show_candlestick.get():
            self.candlestick_chart.pack(pady=10, fill="both", expand=True)
        else:
            self.candlestick_chart.pack_forget()

    def _toggle_recent_trade(self):
        Config.update("SHOW_RECENT_TRADE", self.show_recent_trade.get())
        if self.show_recent_trade.get():
            self.recent_trade.pack(pady=10)
        else:
            self.recent_trade.pack_forget()

    def _toggle_best_trade(self):
        Config.update("SHOW_BEST_TRADE", self.show_best_trade.get())
        if self.show_best_trade.get():
            self.best_trade.pack(pady=10)
        else:
            self.best_trade.pack_forget()

    def create_crypto_list(self):
        for i in Config.CRYPTO_LIST:
            if i in self.crypto_dic:
                continue

            self.crypto_dic[i] = Crypto(i)

    def create_widgets(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(pady=1)

        self.create_toggle_panel()

        self.selection_label = Label(self.root, text="Active symbol: --")

        self.ticker_container = Frame(self.root)
        self.ticker_container.configure(borderwidth=2, relief="flat")

        top_label = Label(self.ticker_container)
        top_label.config(text="Select a cryptocurrency:", font="Arial 14 bold")
        top_label.pack(pady=5)

        for value in self.crypto_dic.values():
            ticker = AdvancedTickerFrame(self.ticker_container)
            ticker.pack(pady=5, fill="x")
            ticker.bind_crypto(value)
            ticker.button_pressed += self._on_crypto_selected

            self.ticker_labeled[value.symbol] = ticker

        self.ticker_container.pack(pady=10, padx=30, anchor="nw", side="left", fill="both")

        self.center_container = Frame(self.root)
        self.center_container.pack(pady=10, padx=30, anchor="nw", side="left", fill="both", expand=True)

        self.order_book = OrderBook(self.center_container)
        self.order_book.pack(pady=10, fill="x")

        self.candlestick_chart = CandlestickChart(self.center_container)
        self.candlestick_chart.pack(pady=10, fill="both", expand=True)

        self.right_container = Frame(self.root)
        self.right_container.pack(pady=10, padx=30, anchor="ne", side="right", fill="y")

        self.best_trade = BestTrade(self.right_container)
        self.best_trade.pack(pady=10, fill="x")

        self.recent_trade = RecentTrade(self.right_container)
        self.recent_trade.pack(pady=10)

        last_crypto = Config.LAST_SELECTED_CRYPTO
        if last_crypto in self.crypto_dic:
            self._on_crypto_selected(self.crypto_dic[last_crypto])
        else:
            self._on_crypto_selected(list(self.crypto_dic.values())[0])

    def _on_crypto_selected(self, crypto):
        old_symbol = self.active_crypto.symbol if self.active_crypto else None
        new_symbol = crypto.symbol

        if self.active_crypto and old_symbol != new_symbol:
            logging.info("Killing old crypto connections")
            self.active_crypto.close_all()
            self.ticker_labeled[old_symbol].enable_select_button()
            self.ticker_labeled[old_symbol].configure(relief="raised")

        logging.info(f"Switching to new symbol: {new_symbol}")
        self.active_crypto = crypto
        self.active_crypto.connect_all()
        self.order_book.bind_crypto(self.active_crypto)
        self.candlestick_chart.bind_crypto(self.active_crypto)
        self.recent_trade.bind_crypto(self.active_crypto)
        self.best_trade.bind_crypto(self.active_crypto)
        self.selection_label.config(text=f"Active symbol: {new_symbol}")
        self.ticker_labeled[new_symbol].configure(relief="sunken")
        self.ticker_labeled[new_symbol].disable_select_button()

        # Save last selected crypto
        Config.update("LAST_SELECTED_CRYPTO", new_symbol)

    def on_closing(self):
        logging.info("Closing Dashboard")
        for ticker in self.ticker_labeled.values():
            ticker.disable_select_button()
            ticker.button_pressed -= self._on_crypto_selected

        for symbol, crypto in self.crypto_dic.items():
            logging.info(f"Closing connections for {symbol}")
            crypto.close_all()
            crypto.ws_ticker.close()

        self.root.destroy()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s -%(levelname)s - %(message)s')

    if not check_network():
        logging.error("No network connection. Please check your internet connection and try again.")
        exit(1)

    root = Tk()
    #root.config(bg="#0A122A")
    dashboard = Dashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()
