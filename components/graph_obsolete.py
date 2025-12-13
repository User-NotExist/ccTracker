# components/graph.py
import tkinter as tk
from tkinter.ttk import Frame, Label
#import mplfinance as mpf
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from datetime import datetime
import logging


class CandlestickChart(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.crypto = None
        self.data = []
        self.max_candles = 100

        self.configure(borderwidth=2, relief="solid")

        self.title_label = Label(self, text="Candlestick Chart", font="Arial 12 bold")
        self.title_label.pack(pady=5)

        # Create matplotlib figure with two subplots (price + volume)
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax_price = self.fig.add_subplot(2, 1, 1)
        self.ax_volume = self.fig.add_subplot(2, 1, 2, sharex=self.ax_price)

        self.fig.subplots_adjust(hspace=0.1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.current_event_handler = None

        self._init_chart()

    def _init_chart(self):
        """Initialize empty chart."""
        self.ax_price.set_ylabel("Price")
        self.ax_price.set_title("Waiting for data...")
        self.ax_volume.set_ylabel("Volume")
        self.ax_volume.set_xlabel("Time")
        self.canvas.draw()

    def bind_crypto(self, crypto):
        """Bind to a crypto instance and subscribe to kline data."""
        #logging.info("Binding messages to candlestick chart for %s", crypto.symbol)
        self.crypto = crypto
        kline_event = self.crypto.ws_kline_1m.message_received

        if self.current_event_handler is kline_event:
            return

        if self.current_event_handler:
            self.current_event_handler -= self._on_kline_message
            self.data = []  # Clear previous data
            logging.info("Unbound previous kline event handler.")

        self.current_event_handler = kline_event
        self.current_event_handler += self._on_kline_message
        logging.info("Subscribed to kline messages for %s", crypto.symbol)

    def _retrive_initial_data(self):
        """Retrieve initial historical kline data."""
        try:
            klines = self.crypto.rest_helper.requests("GET", "/api/v3/klines")
            self.data = []
            for kline in klines:
                candle = {
                    'time': datetime.fromtimestamp(kline[0] / 1000),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5]),
                    'closed': True
                }
                self.data.append(candle)
            self._update_chart()
        except Exception as e:
            logging.error("Error retrieving historical kline data: %s", e)

    def _on_kline_message(self, message):
        """Handle incoming kline/candlestick data."""
        # Schedule processing on the main thread
        #logging.info("Received kline message: %s", message)
        self.after(0, self._process_kline_message, message)

    def _process_kline_message(self, message):
        """Process kline message on main thread."""
        #logging.info("Processing kline/candlestick message: %s", message)
        try:
            data = json.loads(message)
            kline = data.get('k', {})

            candle = {
                'time': datetime.fromtimestamp(kline['t'] / 1000),
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
                'volume': float(kline['v']),
                'closed': kline['x']
            }

            # Update or append candle
            if self.data and self.data[-1]['time'] == candle['time']:
                self.data[-1] = candle
            else:
                self.data.append(candle)
                if len(self.data) > self.max_candles:
                    self.data.pop(0)

            self._update_chart()
        except Exception as e:
            logging.error("Error processing kline message: %s", e)

    def _update_chart(self):
        """Redraw the candlestick chart with volume."""
        if len(self.data) < 2:
            return

        df = pd.DataFrame(self.data)
        df.set_index('time', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']]
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        self.ax_price.clear()
        self.ax_volume.clear()

        # Draw candlesticks
        for i in range(len(df)):
            color = 'green' if df['Close'].iloc[i] >= df['Open'].iloc[i] else 'red'
            # Candle body
            self.ax_price.bar(i, df['Close'].iloc[i] - df['Open'].iloc[i],
                              bottom=df['Open'].iloc[i], color=color, width=0.8)
            # Wicks
            self.ax_price.vlines(i, df['Low'].iloc[i], df['High'].iloc[i], color=color, linewidth=1)
            # Volume bars
            self.ax_volume.bar(i, df['Volume'].iloc[i], color=color, width=0.8)

        self.ax_price.set_ylabel("Price")
        self.ax_price.set_title(f"{self.crypto.symbol.upper()} - 1h Candles")
        self.ax_volume.set_ylabel("Volume")
        self.ax_volume.set_xlabel("Time")

        self.fig.tight_layout()
        self.canvas.draw()
