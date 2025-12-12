from tkinter import Tk
from tkinter.ttk import Label, Button, Frame
from components.graph import CandlestickChart
from components.advanced_ticker import AdvancedTickerFrame
from components.order_book import OrderBook
from components.recent_trade import RecentTrade
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
        self.ticker_labeled = {}
        self.ticker_container = None
        self.order_book = None
        self.candlestick_chart = None
        self.center_container = None
        self.right_container = None
        self.recent_trade = None

        self.create_crypto_list()

        self.frame = Frame(self.root)

        self.create_widgets()

    def create_crypto_list(self):
        for i in Config.CRYPTO_LIST:
            if i in self.crypto_dic:
                continue

            self.crypto_dic[i] = Crypto(i)

    def create_widgets(self):
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(pady=1)

        self.selection_label = Label(self.root, text="Active symbol: --")
        self.selection_label.pack(pady=10)

        self.ticker_container = Frame(self.root)
        self.ticker_container.configure(borderwidth=2, relief="solid")

        top_label = Label(self.ticker_container)
        top_label.config(text="Select a cryptocurrency:", font="Arial 14 bold")
        top_label.pack(pady=5)

        for value in self.crypto_dic.values():
            ticker = AdvancedTickerFrame(self.ticker_container)
            ticker.pack(pady=5)
            ticker.bind_crypto(value)
            ticker.button_pressed += self._on_crypto_selected

            self.ticker_labeled[value.symbol] = ticker

        self.ticker_container.pack(pady=10, padx=30, anchor="nw", side="left")

        self.center_container = Frame(self.root)
        self.center_container.pack(pady=10, padx=30, anchor="nw", side="left", fill="both", expand=True)

        self.order_book = OrderBook(self.center_container)
        self.order_book.pack(pady=10, fill="x")

        self.candlestick_chart = CandlestickChart(self.center_container)
        self.candlestick_chart.pack(pady=10, fill="both", expand=True)

        self.right_container = Frame(self.root)
        self.right_container.pack(pady=10, padx=30, anchor="ne", side="right")

        self.recent_trade = RecentTrade(self.right_container)
        self.recent_trade.pack(pady=10)

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
        self.selection_label.config(text=f"Active symbol: {new_symbol}")
        self.ticker_labeled[new_symbol].configure(relief="sunken")
        self.ticker_labeled[new_symbol].disable_select_button()

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
    root = Tk()
    dashboard = Dashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()
