# components/advanced_ticker.py
import json
import time
from tkinter.ttk import Frame, Label, Button
from utils.event import Event

class AdvancedTickerFrame(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=12, **kwargs)
        self.last_update = 0
        self.update_interval = 0.2 # seconds
        self.configure(borderwidth=1, relief="groove")
        self.columnconfigure(0, weight=1)

        self.label = Label(self, text="Unknow Coin", font="Arial 18 bold", anchor="center", justify="center")
        self.label.grid(row=0, columnspan=3, sticky="ew", pady=(0, 8))

        self.price_var = Label(self, text="Price: --", font="Arial 16 bold", anchor="center", justify="center")
        self.price_var.grid(row=1, columnspan=3, sticky="ew", pady=(0, 4))

        self.change_var = Label(self, text="Change: --", font=("Arial", 10), anchor="center", justify="center")
        self.change_var.grid(row=2, column=0, sticky="w")

        self.split = Label(self, text="|", font=("Arial", 13), anchor="center", justify="center")
        self.split.grid(row=2, column=1)

        self.percent_var = Label(self, text="Percent: --%", font=("Arial", 10), anchor="center", justify="center")
        self.percent_var.grid(row=2, column=2, sticky="e")

        self.button = Button(self, text="Select", command=lambda: self.button_clicked())
        self.button.grid(row=3, columnspan=3, sticky="ew", pady=(4, 0))

        self.current_event_handler = None
        self.crypto = None
        self.button_pressed = Event()

    def enable_select_button(self):
        self.button.config(text="Select")
        self.button.config(state="normal")

    def disable_select_button(self):
        self.button.config(text="Selected")
        self.button.config(state="disabled")

    def bind_crypto(self, crypto):
        self.crypto = crypto
        self.label.config(text=crypto.symbol)
        self.crypto.ws_ticker.connect()
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
        price = float(data.get("c"))
        change = float(data.get("p"))
        percent = float(data.get("P"))
        self.master.after(0, lambda: self.__update_labels(price, change, percent))

    def __update_labels(self, price, change, percent):
        color = "green" if change >= 0 else "red"
        self.price_var.configure(foreground=color)
        self.change_var.configure(foreground=color)
        self.percent_var.configure(foreground=color)
        self.price_var.config(text=f"Price: {price or '--'}")
        self.change_var.config(text=f"Change: {change or '--'}")
        self.percent_var.config(text=f"Percent: {percent or '--'}%")

    def button_clicked(self):
        if self.crypto:
            self.button_pressed(self.crypto)
