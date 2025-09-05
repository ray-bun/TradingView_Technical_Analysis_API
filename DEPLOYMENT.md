# Deployment Guide for TradingView Technical Analysis API

## Coolify Deployment

### Prerequisites
- Coolify instance running
- Git repository accessible by Coolify

### Deployment Steps

1. **Add Your Repository to Coolify**
   - In Coolify dashboard, go to "Resources" > "New"
   - Select "Public Repository" or connect your Git provider
   - Enter repository URL: `https://github.com/yourusername/TradingView_Technical_Analysis_API`

2. **Configure Build Settings**
   - Build Pack: Docker
   - Dockerfile Path: `./Dockerfile`
   - Port: `8000`

3. **Environment Variables** (Optional)
   ```
   FLASK_ENV=production
   DEBUG=false
   PORT=8000
   ```

4. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Your API will be available at your Coolify domain

### Health Check
- Health check endpoint: `/health`
- Returns: `{"status": "healthy", "service": "TradingView Technical Analysis API", "version": "2.0.0"}`

## Docker Deployment

### Build and Run Locally
```bash
# Build the image
docker build -t tradingview-api .

# Run the container
docker run -d -p 8000:8000 --name tradingview-api tradingview-api

# Check health
curl http://localhost:8000/health
```

### Using Docker Compose
```bash
# Start the service
docker-compose up -d

# Stop the service
docker-compose down
```

## API Usage

### Base URL
- Local: `http://localhost:8000`
- Production: Your deployed domain

### Endpoints

#### Health Check
```
GET /health
```

#### Technical Analysis
```
GET /<symbol>/<screener>/<exchange>/<interval>

Examples:
- GET /BTCUSDT/crypto/BINANCE/1d
- GET /AAPL/america/NASDAQ/4h
- GET /EURUSD/forex/FX_IDC/1h
```

### Supported Parameters
- **Intervals**: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1w, 1month
- **Exchanges**: BINANCE, NASDAQ, NYSE, FX_IDC, etc.
- **Screeners**: crypto, america, forex, indonesia, etc.

### Response Format
```json
{
  "data": {
    "RECOMMENDATION": "BUY",
    "BUY": 15,
    "SELL": 3,
    "NEUTRAL": 8
  },
  "symbol": "BTCUSDT",
  "screener": "crypto",
  "exchange": "BINANCE",
  "interval": "1d",
  "timestamp": "2025-01-15T10:30:00"
}
```

### Error Responses
```json
{
  "error": "Invalid time interval",
  "message": "Supported intervals: ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w', '1month']",
  "provided": "5min"
}
```

## Features

### Improvements Made
- ✅ **Modern Dependencies**: Updated all packages to latest secure versions
- ✅ **Error Handling**: Comprehensive error handling with proper HTTP status codes
- ✅ **Logging**: Structured logging for monitoring and debugging
- ✅ **Health Check**: Built-in health check endpoint for monitoring
- ✅ **Security**: Non-root user in Docker, security best practices
- ✅ **Performance**: Optimized Gunicorn configuration
- ✅ **Validation**: Input validation and meaningful error messages
- ✅ **Metadata**: Response includes request metadata and timestamps
- ✅ **Docker Optimized**: Multi-stage build with minimal image size

### Production Features
- Non-root user execution
- Proper signal handling
- Health monitoring
- Request logging
- Error tracking
- Graceful shutdowns
- Resource optimization

## Monitoring

The application includes structured logging and health checks for monitoring:

- **Health Endpoint**: `/health`
- **Logs**: Structured JSON logs with timestamps
- **Metrics**: Request/response logging for monitoring

## Troubleshooting

### Common Issues

1. **Invalid Parameters**
   - Check symbol format (e.g., "BTCUSDT", not "BTC/USDT")
   - Verify exchange and screener combination
   - Use supported intervals only

2. **Service Unavailable**
   - Check if TradingView servers are accessible
   - Verify network connectivity
   - Check application logs

3. **Docker Build Issues**
   - Ensure Docker daemon is running
   - Check Dockerfile syntax
   - Verify requirements.txt format

### Logs
Check application logs for detailed error information:
```bash
# Docker logs
docker logs tradingview-api

# Docker Compose logs
docker-compose logs -f
```