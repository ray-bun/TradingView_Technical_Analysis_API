from flask import Flask
from flask_restful import  Api, Resource
from tradingview_ta import TA_Handler, Interval, Exchange


app = Flask(__name__)
api = Api(app)

class TradingView(Resource):
    def get(self,symbol,screener,exchange,timeinterval):
        if (timeinterval == '1m'):
            time_frame = Interval.INTERVAL_1_MINUTE
        elif (timeinterval == '5m'):
            time_frame = Interval.INTERVAL_5_MINUTES
        elif (timeinterval == '15m'):
            time_frame = Interval.INTERVAL_15_MINUTES
        elif (timeinterval == '30m'):
            time_frame = Interval.INTERVAL_30_MINUTES
        elif (timeinterval == '1h'):
            time_frame = Interval.INTERVAL_1_HOUR
        elif (timeinterval == '2h'):
            time_frame = Interval.INTERVAL_2_HOUR
        elif (timeinterval == '4h'):
            time_frame = Interval.INTERVAL_4_HOURS
        elif (timeinterval == '1d'):
            time_frame = Interval.INTERVAL_1_DAY
        elif (timeinterval == '1w'):
            time_frame = Interval.INTERVAL_1_WEEK
        elif (timeinterval == '1month'):
            time_frame = Interval.INTERVAL_1_MONTH
      
        data = TA_Handler(
                symbol=symbol,
                screener=screener,
                exchange=exchange,
                interval=time_frame)
            
        return data.get_analysis().summary


    


api.add_resource(TradingView, "/<string:symbol>/<string:screener>/<string:exchange>/<string:timeinterval>")
if __name__ == "__main__":
    app.run(debug=False)
