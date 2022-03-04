from flask import Flask, app, json, jsonify
from flask_restful import  Api, Resource
from tradingview_ta import TA_Handler, Interval, Exchange

app = Flask(__name__)

@app.route("/")
def TradingView():
    return jsonify({"hello": "hello"})

if __name__ == "__main__":
    app.run(debug=True)