import os
import logging
from flask import Flask, jsonify
from flask_restful import Api, Resource
from tradingview_ta import TA_Handler, Interval, Exchange

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

# Initialize API
api = Api(app)

# Interval mapping for better maintainability
INTERVAL_MAPPING = {
    '1m': Interval.INTERVAL_1_MINUTE,
    '5m': Interval.INTERVAL_5_MINUTES,
    '15m': Interval.INTERVAL_15_MINUTES,
    '30m': Interval.INTERVAL_30_MINUTES,
    '1h': Interval.INTERVAL_1_HOUR,
    '2h': Interval.INTERVAL_2_HOURS,
    '4h': Interval.INTERVAL_4_HOURS,
    '1d': Interval.INTERVAL_1_DAY,
    '1w': Interval.INTERVAL_1_WEEK,
    '1month': Interval.INTERVAL_1_MONTH
}

class HealthCheck(Resource):
    """Health check endpoint for monitoring and load balancers"""
    def get(self):
        return {
            'status': 'healthy',
            'service': 'TradingView Technical Analysis API',
            'version': '2.0.0'
        }, 200

class TradingView(Resource):
    def get(self, symbol, screener, exchange, timeinterval):
        try:
            # Validate time interval
            if timeinterval not in INTERVAL_MAPPING:
                return {
                    'error': 'Invalid time interval',
                    'message': f'Supported intervals: {list(INTERVAL_MAPPING.keys())}',
                    'provided': timeinterval
                }, 400

            # Log the request
            logger.info(f"Processing request: {symbol}/{screener}/{exchange}/{timeinterval}")

            # Get time frame
            time_frame = INTERVAL_MAPPING[timeinterval]
            
            # Create TA Handler
            ta_handler = TA_Handler(
                symbol=symbol.upper(),
                screener=screener.lower(),
                exchange=exchange.upper(),
                interval=time_frame
            )
            
            # Get analysis
            analysis = ta_handler.get_analysis()
            
            if not analysis:
                return {
                    'error': 'Analysis not available',
                    'message': 'Unable to fetch analysis data for the given parameters'
                }, 404

            # Return the summary with additional metadata
            result = {
                'data': analysis.summary,
                'symbol': symbol.upper(),
                'screener': screener.lower(),
                'exchange': exchange.upper(),
                'interval': timeinterval,
                'timestamp': analysis.time.isoformat() if hasattr(analysis, 'time') and analysis.time else None
            }
            
            logger.info(f"Successfully processed: {symbol}/{screener}/{exchange}/{timeinterval}")
            return result, 200
            
        except ValueError as ve:
            logger.error(f"Value error for {symbol}/{screener}/{exchange}/{timeinterval}: {str(ve)}")
            return {
                'error': 'Invalid parameters',
                'message': str(ve)
            }, 400
            
        except Exception as e:
            logger.error(f"Error processing {symbol}/{screener}/{exchange}/{timeinterval}: {str(e)}")
            return {
                'error': 'Internal server error',
                'message': 'An error occurred while processing your request'
            }, 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An internal error occurred'
    }), 500

# Add resources to API
api.add_resource(HealthCheck, '/health')
api.add_resource(TradingView, "/<string:symbol>/<string:screener>/<string:exchange>/<string:timeinterval>")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
