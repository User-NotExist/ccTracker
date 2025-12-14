# CryptoCurrency Tracker (CC-Tracker)
A cryptocurrency price tracker built with Python and Tkinter.

[Youtube Link](https://youtu.be/q46alDK3QR0)
[image](./picture/msrdc_o8iBZo5yqS.png)

## Features
- Real-time price updates for various cryptocurrencies.
- Detailed reports of price history (24h) in candlestick.
- Recent trade listing and order book.
- Toggleable GUI.
- Configuration file to customize experience.

## Requirements
- Python 3.12+
- Tkinter

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/User-NotExist/ccTracker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ccTracker
    ```
3. **OPTIONAL:** Use virtual environment to not brick your system packages (in case something goes wrong):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the main script to start the application:
```bash
python3 main.py
```

When you run the application for the first time, a configuration file (`config.json`) will be created in the project folder.

## Configuration

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `CRYPTO_LIST` | `string[]` | `["BTCUSDT", "ADAUSDT", "SOLUSDT", "DOGEUSDT", "TRXUSDT"]` | List of cryptocurrency trading pairs to display. Must be valid Binance symbols (e.g., `"ETHUSDT"`, `"BNBUSDT"`). |
| `STARTING_RESOLUTION` | `string` | `"1600x900"` | Initial window size in `WIDTHxHEIGHT` format (e.g., `"1920x1080"`, `"1280x720"`). |
| `WINDOW_TITLE` | `string` | `"Crypto Dashboard"` | Application window title. |
| `SHOW_TICKER` | `boolean` | `true` | Show/hide the ticker panel on the left side. |
| `SHOW_ORDER_BOOK` | `boolean` | `true` | Show/hide the order book component. |
| `SHOW_CANDLESTICK` | `boolean` | `true` | Show/hide the candlestick chart. |
| `SHOW_RECENT_TRADE` | `boolean` | `true` | Show/hide the recent trades list. |
| `SHOW_BEST_TRADE` | `boolean` | `true` | Show/hide the best bid/ask display. |
| `LAST_SELECTED_CRYPTO` | `string` | `"BTCUSDT"` | Last selected cryptocurrency symbol. Automatically saved when switching. Must exist in `CRYPTO_LIST`. |
