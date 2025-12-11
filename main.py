from tkinter import Tk, messagebox
from tkinter.ttk import Label, Button
from components.dropdown import CryptoDropdown
from components.ticker import TickerFrame
from components.order_book import OrderBook
from config import Config
import logging


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x800")
        self.crypto = None
        self.ticker_frame = None
        self.order_book = None
        self.create_widgets()

    def create_widgets(self):
        self.dropdown = CryptoDropdown(self.root, Config.CRYPTO_LIST)
        self.dropdown.pack(pady=10)
        self.selection_label = Label(self.root, text="Active symbol: --")
        self.selection_label.pack(pady=10)

        self.ticker_frame = TickerFrame(self.root)
        self.ticker_frame.pack(pady=10, padx=30, anchor="nw", side="left")

        self.order_book = OrderBook(self.root)
        self.order_book.pack(pady=10, padx=30, anchor="nw", side="left")

        self.dropdown.on_selection += self._on_crypto_selected
        self._on_crypto_selected(None, self.dropdown.current_symbol, self.dropdown.crypto)

    def _on_crypto_selected(self, old_symbol, new_symbol, crypto):
        if self.crypto and old_symbol != new_symbol:
            logging.info("Killing old crypto connections")
            self.crypto.close_all()

        logging.info(f"Switching to new symbol: {new_symbol}")
        self.crypto = crypto
        self.crypto.connect_all()
        self.ticker_frame.bind_crypto(self.crypto)
        self.order_book.bind_crypto(self.crypto)
        self.selection_label.config(text=f"Active symbol: {new_symbol}")

    def on_closing(self):
        logging.info("Closing Dashboard")
        self.dropdown.on_selection -= self._on_crypto_selected

        if self.crypto:
            self.crypto.close_all()
        self.root.destroy()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -%(levelname)s -on line: %(lineno)d -%(message)s')
    logger = logging.getLogger('name')
    logger.debug('hello')
    root = Tk()
    dashboard = Dashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()
