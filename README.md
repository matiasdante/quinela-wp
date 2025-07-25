<h1 align="center">
  <br>
  <a href="https://github.com/matiasdante"><img src="https://www.loteria.gba.gov.ar/images/logos/01_LogoQuinielaMultiple.png" alt="DevOps Projects" width="200"></a>
  <br>
  Quiniela Analytics
  <br>
</h1>

<h4 align="center">Sistema Avanzado de Análisis de Datos para Quiniela - Predicciones Inteligentes y Dashboard Interactivo</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api">API</a> •
  <a href="#docker">Docker</a> •
  <a href="#credits">Credits</a> 
</p>

![Quiniela Analytics Dashboard](https://github.com/user-attachments/assets/dd7b6c36-b842-40e5-b5fa-67b85c673253)

## Features

### 🎯 Advanced Analytics
- **Statistical Analysis**: Frequency analysis of numbers by month, week, and custom periods
- **Hot/Cold Numbers**: Intelligent detection of trending and rare numbers
- **Pattern Recognition**: Weekly patterns and consecutive number detection
- **Smart Recommendations**: AI-powered predictions based on historical data

### 📊 Modern Dashboard
- **Responsive Design**: Beautiful, mobile-friendly interface
- **Real-time Data**: Live lottery results from multiple provinces
- **Interactive Visualizations**: Statistics cards and frequency charts
- **Multi-province Support**: Analysis across all Argentine provinces

### 🔄 Automated Data Collection
- **Automatic Scraping**: Scheduled data collection every hour
- **Historical Storage**: SQLite database for long-term data analysis
- **Error Handling**: Robust error management and logging
- **Data Validation**: Clean and validated lottery results

### 🚀 API-First Architecture
- **RESTful API**: Complete API for all functionality
- **JSON Responses**: Structured data for easy integration
- **Real-time Analytics**: Live statistical computations
- **Extensible**: Easy to add new analysis features

## Installation

### Prerequisites
- Python 3.11 or higher
- Git

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/matiasdante/quinela-wp.git
cd quinela-wp
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

4. **Run the application**:
```bash
python main.py
```

5. **Access the dashboard**:
Open [http://localhost:5000](http://localhost:5000) in your browser

## Usage

### Web Dashboard
The main dashboard provides:
- Current lottery results from all provinces
- Monthly frequency analysis
- Smart number recommendations
- Quick access to API endpoints

### Manual Data Collection
Trigger manual scraping:
```bash
curl -X POST http://localhost:5000/api/scrape
```

### Analytics Queries
Get analytics for specific provinces:
```bash
# Monthly analysis for Buenos Aires
curl "http://localhost:5000/api/analytics/monthly?provincia=Provincia de Buenos Aires"

# Hot/cold numbers for last 60 days
curl "http://localhost:5000/api/analytics/hot-cold?days=60"

# Smart recommendations
curl "http://localhost:5000/api/recommendations"
```

## API

### Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Main dashboard |
| `/api/current` | GET | Current lottery results |
| `/api/scrape` | POST | Manual scraping trigger |
| `/api/analytics/monthly` | GET | Monthly frequency analysis |
| `/api/analytics/hot-cold` | GET | Hot and cold numbers |
| `/api/analytics/weekly-patterns` | GET | Weekly pattern analysis |
| `/api/recommendations` | GET | Smart number recommendations |
| `/api/patterns` | GET | Detected patterns and alerts |
| `/api/historical` | GET | Historical results |
| `/api/stats` | GET | Database statistics |
| `/api/provinces` | GET | Available provinces |

### Query Parameters

- `provincia`: Filter by specific province
- `days`: Number of days for analysis (default: 30)
- `weeks`: Number of weeks for analysis (default: 8)
- `start_date`: Start date for historical queries (YYYY-MM-DD)
- `end_date`: End date for historical queries (YYYY-MM-DD)

### Example Response
```json
{
  "success": true,
  "data": {
    "month": "2025-07",
    "provincia": "Ciudad",
    "total_draws": 150,
    "most_frequent": [
      {
        "numero": "1234",
        "frequency": 8,
        "percentage": 5.33
      }
    ],
    "statistics": {
      "total_unique_numbers": 120,
      "avg_frequency": 1.25,
      "median_frequency": 1,
      "max_frequency": 8,
      "min_frequency": 1
    }
  }
}
```

## Docker

### Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The compose setup includes:
- **quinela-app**: Main web application
- **quinela-scraper**: Automated data collection service
- **nginx**: Reverse proxy for production

### Manual Docker Build
```bash
# Build image
docker build -t quinela-analytics .

# Run container
docker run -p 5000:5000 -v $(pwd)/data:/app/data quinela-analytics
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_PATH` | `data/quinela.db` | SQLite database location |
| `SCRAPING_URL` | `https://www.jugandoonline.com.ar/` | Source website |
| `SCRAPING_INTERVAL_HOURS` | `1` | Scraping frequency |
| `FLASK_HOST` | `0.0.0.0` | Flask host |
| `FLASK_PORT` | `5000` | Flask port |
| `FLASK_DEBUG` | `False` | Debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |

### Directory Structure
```
quinela-wp/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Container definition
├── backend/              # Core backend modules
│   ├── api.py           # Flask API routes
│   ├── database.py      # SQLite operations
│   ├── analytics.py     # Statistical analysis
│   └── scraper.py       # Data collection
├── data/                # SQLite database (auto-created)
├── logs/                # Application logs (auto-created)
└── frontend/            # Static assets (future expansion)
```

## Analytics Features

### Monthly Frequency Analysis
- Tracks number frequency for current month
- Calculates appearance percentages
- Provides statistical metrics (mean, median, max, min)

### Hot/Cold Number Detection
- Identifies trending numbers (hot)
- Finds underperforming numbers (cold)
- Uses statistical thresholds based on standard deviation

### Weekly Pattern Recognition
- Analyzes patterns by day of the week
- Provides day-specific recommendations
- Historical trend analysis

### Smart Recommendations
- Combines multiple analysis methods
- Confidence scoring for each recommendation
- Includes contrarian strategies
- Transparent reasoning for each prediction

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- **Original Creator**: [matiasdante](https://github.com/matiasdante)
- **Data Source**: [Jugando Online](https://www.jugandoonline.com.ar/)
- **Enhanced Analytics**: Advanced statistical analysis and modern web interface

---

<p align="center">
  <strong>Made with ❤️ for better lottery analysis</strong>
</p>
