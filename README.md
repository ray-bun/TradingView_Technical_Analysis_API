# TradingView_Technical_Analysis
A fast and easy way to analyze Cryptocurrencies Technical analysis gauges display real-time ratings for the selected timeframes. The summary for Bitcoin / TetherUS is based on the most popular technical indicators — Moving Averages, Oscillators and Pivots. Results are available at a quick glance.

# Installation
Set up Python virtual environment
```
python -m venv ENV
```
Switch into the virtual environment
```
source ENV/bin/activate
```
Install packages
```
pip install -r requirements.txt
```
Start API
```
python api.py 
```
# Usage
Sample URL below is how we fetch BTCUSDT pair from Binance on a 1 Day chart.
```
http://localhost:5000/<SYMBOL>/<SCREENER>/<EXCHANGE>/<INTERVAL>
EXAMPLE:
http://localhost:5000/BTCUSDT/crypto/BINANCE/1d

```
API Response Sample:
```
{"RECOMMENDATION": "NEUTRAL", "BUY": 9, "SELL": 8, "NEUTRAL": 9}
```
The result should be the same as shown here: https://www.tradingview.com/symbols/BTCUSDT/technicals/
![Alt text](media/TV_TA.png?raw=true "TA_TA")

You can use the link below to test your pair: https://tradingview.brianthe.dev/

# Full Credit @brian-the-dev
https://github.com/brian-the-dev/python-tradingview-ta
