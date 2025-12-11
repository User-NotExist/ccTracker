# components/ticker.py
import json
import time
from tkinter.ttk import Frame, Label

class TickerFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=12, **kwargs)
        self.last_update = 0
        self.update_interval = 0.2 # seconds
        self.configure(borderwidth=1, relief="solid")
        self.columnconfigure(0, weight=1)

        self.price_var = Label(self, text="Price: --", font="Arial 18 bold", anchor="center", justify="center")
        self.price_var.grid(row=0, columnspan=3, sticky="ew", pady=(0, 4))

        self.change_var = Label(self, text="Change: --", font=("Arial", 10), anchor="center", justify="center")
        self.change_var.grid(row=1, column=0, sticky="w")

        self.split = Label(self, text="|", font=("Arial", 13), anchor="center", justify="center")
        self.split.grid(row=1, column=1)

        self.percent_var = Label(self, text="Percent: --%", font=("Arial", 10), anchor="center", justify="center")
        self.percent_var.grid(row=1, column=2, sticky="e")

        self.current_event_handler = None

    def bind_crypto(self, crypto):
        ticker_event = crypto.ws_ticker.message_received

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
        price = float(data.get("c"))
        change = float(data.get("p"))
        percent = float(data.get("P"))
        self.after(0, lambda: self.__update_labels(price, change, percent))

    def __update_labels(self, price, change, percent):
        color = "green" if change >= 0 else "red"
        self.price_var.configure(foreground=color)
        self.change_var.configure(foreground=color)
        self.percent_var.configure(foreground=color)
        self.price_var.config(text=f"Price: {price or '--'}")
        self.change_var.config(text=f"Change: {change or '--'}")
        self.percent_var.config(text=f"Percent: {percent or '--'}%")
