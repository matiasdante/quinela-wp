import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/quinela.db')
    
    # Scraping configuration
    SCRAPING_URL = os.getenv('SCRAPING_URL', 'https://www.jugandoonline.com.ar/')
    SCRAPING_INTERVAL_HOURS = int(os.getenv('SCRAPING_INTERVAL_HOURS', '1'))
    
    # Flask configuration
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Analytics configuration
    ANALYSIS_DAYS_BACK = int(os.getenv('ANALYSIS_DAYS_BACK', '30'))
    MIN_FREQUENCY_THRESHOLD = float(os.getenv('MIN_FREQUENCY_THRESHOLD', '0.1'))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/quinela.log')

# Province mapping (from existing code)
PROVINCIAS = [
    ('MainContent_CabezasHoyCiudadDiv', 'Ciudad'),
    ('MainContent_CabezasHoyProvBsAsDiv', 'Provincia de Buenos Aires'),
    ('MainContent_CabezasHoyMontevideoDiv', 'Montevideo'),
    ('MainContent_CabezasHoyCordobaDiv', 'Córdoba'),
    ('MainContent_CabezasHoySantaFeDiv', 'Santa Fe'),
    ('MainContent_CabezasHoyEntreRiosDiv', 'Entre Ríos'),
    ('MainContent_CabezasHoyMendozaDiv', 'Mendoza')
]