import json
import time
from tkinter.ttk import Frame, Label


class BestTrade(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=8, **kwargs)
        self.configure(borderwidth=2, relief="solid")
        self.columnconfigure(0, weight=1)

        self.last_update = 0
        self.update_interval = 0.2  # seconds

        # Title
        Label(self, text="Best Bid/Ask", font="Arial 16 bold", anchor="center").grid(
            row=0, column=0, sticky="ew", pady=(0, 8)
        )

        # Best Bid section
        Label(self, text="Best Bid", font="Arial 12 bold", anchor="w").grid(
            row=1, column=0, sticky="w"
        )
        self.bid_price_label = Label(self, text="Price: --", font="Arial 11", foreground="green")
        self.bid_price_label.grid(row=2, column=0, sticky="w", padx=(10, 0))
        self.bid_volume_label = Label(self, text="Volume: --", font="Arial 11", foreground="green")
        self.bid_volume_label.grid(row=3, column=0, sticky="w", padx=(10, 0), pady=(0, 8))

        # Best Ask section
        Label(self, text="Best Ask", font="Arial 12 bold", anchor="w").grid(
            row=4, column=0, sticky="w"
        )
        self.ask_price_label = Label(self, text="Price: --", font="Arial 11", foreground="red")
        self.ask_price_label.grid(row=5, column=0, sticky="w", padx=(10, 0))
        self.ask_volume_label = Label(self, text="Volume: --", font="Arial 11", foreground="red")
        self.ask_volume_label.grid(row=6, column=0, sticky="w", padx=(10, 0))

        self.current_event_handler = None
        self.crypto = None

    def bind_crypto(self, crypto):
        self.crypto = crypto
        ticker_event = self.crypto.ws_ticker.message_received

        if self.current_event_handler is ticker_event:
            return

        if self.current_event_handler:
            self.current_event_handler -= self.__handle_message

        self.current_event_handler = ticker_event
        self.current_event_handler += self.__handle_message

    def __handle_message(self, message):
        if time.time() - self.last_update < self.update_interval:
            return

        self.last_update = time.time()
        data = json.loads(message)

        # Ticker data fields: b = best bid price, B = best bid qty, a = best ask price, A = best ask qty
        bid_price = data.get("b", "--")
        bid_volume = data.get("B", "--")
        ask_price = data.get("a", "--")
        ask_volume = data.get("A", "--")

        self.master.after(0, lambda: self.__update_labels(bid_price, bid_volume, ask_price, ask_volume))

    def __update_labels(self, bid_price, bid_volume, ask_price, ask_volume):
        self.bid_price_label.config(text=f"Price: {bid_price}")
        self.bid_volume_label.config(text=f"Volume: {bid_volume}")
        self.ask_price_label.config(text=f"Price: {ask_price}")
        self.ask_volume_label.config(text=f"Volume: {ask_volume}")
