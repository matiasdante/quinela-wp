import logging
import os
from flask import Flask
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

# Initialize the enhanced Quiniela API
quinela_api = QuinielaAPI(app)

if __name__ == '__main__':
    logging.info("Starting Quiniela Analytics Server...")
    app.run(
        host=Config.FLASK_HOST, 
        port=Config.FLASK_PORT, 
        debug=Config.FLASK_DEBUG
    )

