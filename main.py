# python
# `main.py`
from tkinter import Tk
from tkinter.ttk import Label, Button
from components.dropdown import CryptoDropdown
from components.ticker import TickerFrame
from config import Config


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x800")
        self.crypto = None
        self.ticker_frame = None
        self.create_widgets()

    def create_widgets(self):
        self.dropdown = CryptoDropdown(self.root, Config.CRYPTO_LIST, on_selection=self._on_crypto_selected)
        self.dropdown.pack(pady=10)
        self.selection_label = Label(self.root, text="Active symbol: --")
        self.selection_label.pack(pady=10)

        self.ticker_frame = TickerFrame(self.root)
        self.ticker_frame.pack(pady=10, padx=30, anchor="nw", side="left")

        self._on_crypto_selected(None, self.dropdown.current_symbol, self.dropdown.crypto)

    def _on_crypto_selected(self, old_symbol, new_symbol, crypto):
        if self.crypto and old_symbol != new_symbol:
            self.crypto.close_all()
        self.crypto = crypto
        self.crypto.connect_all()
        self.ticker_frame.bind_crypto(self.crypto)
        self.selection_label.config(text=f"Active symbol: {new_symbol}")

    def on_closing(self):
        if self.crypto:
            self.crypto.close_all()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    dashboard = Dashboard(root)
    root.protocol("WM_DELETE_WINDOW", dashboard.on_closing)
    root.mainloop()
