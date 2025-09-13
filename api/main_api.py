import logging
import os
from flask import Flask
from flask_cors import CORS
from backend.api import QuinielaAPI
from config import Config

# Setup logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

# Ensure logs directory exists
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=['*'])

# Initialize the enhanced Quiniela API
quinela_api = QuinielaAPI(app, api_only=True)

if __name__ == '__main__':
    logging.info("Starting Quiniela API Server...")
    app.run(
        host=Config.FLASK_HOST, 
        port=Config.FLASK_PORT, 
        debug=Config.FLASK_DEBUG
    )