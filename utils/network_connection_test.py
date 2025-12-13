import logging
from tkinter import Tk, messagebox
from utils.binance_rest import BinanceRest


class NetworkConnectionTest:
    def __init__(self, timeout: float = 5.0):
        self.binance = BinanceRest(timeout=timeout)

    def ping_binance(self) -> bool:
        """Test connection to Binance server."""
        try:
            response = self.binance.request("GET", "/api/v3/ping")
            return response == {}
        except Exception as e:
            logging.error(f"Binance connection failed: {e}")
            return False

    def check_connection_with_popup(self, parent=None) -> bool:
        """Check connection and show error popup if failed."""
        if not self.ping_binance():
            if parent is None:
                root = Tk()
                root.withdraw()
                parent = root

            messagebox.showerror(
                "Connection Error",
                "Unable to connect to Binance server.\n\n"
                "Please check your internet connection and try again."
            )

            if isinstance(parent, Tk) and parent.winfo_exists():
                parent.destroy()

            return False
        return True


def check_network() -> bool:
    """Convenience function to check network connection."""
    test = NetworkConnectionTest()
    return test.check_connection_with_popup()