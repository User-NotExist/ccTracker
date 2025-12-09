# python
import json
from tkinter import Tk, Frame, Label
from utils.binance_websocket import BinanceWebSocket

class Dashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard")
        self.master.geometry("400x300")

        self.frame = Frame(self.master)
        self.frame.pack(fill='both', expand=True)

        self.label = Label(self.frame, text="Welcome to the Dashboard", font=("Arial", 16))
        self.label.pack(pady=20)

        self.price_label = Label(self.frame, text="btcusdt@ticker: waiting...", font=("Arial", 14))
        self.price_label.pack(pady=10)

        self.status_label = Label(self.frame, text="Status: disconnected", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.ws = BinanceWebSocket("btcusdt", "ticker")
        self.ws.connected += self._handle_connected
        self.ws.message_received += self._handle_message
        self.ws.error_received += self._handle_error
        self.ws.disconnected += self._handle_disconnected
        self.ws.connect()

        self.master.protocol("WM_DELETE_WINDOW", self._on_close)

    def _handle_connected(self):
        self.master.after(0, lambda: self.status_label.config(text="Status: connected"))

    def _handle_message(self, message: str):
        try:
            data = json.loads(message)
            price = data.get("c") or data.get("p") or "n/a"
        except json.JSONDecodeError:
            price = "n/a"
        self.master.after(0, lambda: self.price_label.config(text=f"btcusdt@ticker: {price}"))

    def _handle_error(self, error):
        self.master.after(0, lambda: self.status_label.config(text=f"Status: error ({error})"))

    def _handle_disconnected(self):
        self.master.after(0, lambda: self.status_label.config(text="Status: disconnected"))

    def _on_close(self):
        self.ws.close()
        self.master.destroy()

if __name__ == "__main__":
        root = Tk()
        dashboard = Dashboard(root)
        root.mainloop()
