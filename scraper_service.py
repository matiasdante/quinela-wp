#!/usr/bin/env python3
"""
Standalone Quiniela Scraper Service

This script runs the automated scraper service independently from the web application.
It can be used for scheduled data collection in production environments.

Usage:
    python scraper_service.py
    
    or with systemd:
    
    [Unit]
    Description=Quiniela Scraper Service
    After=network.target
    
    [Service]
    Type=simple
    User=quinela
    WorkingDirectory=/path/to/quinela-wp
    Environment=PYTHONPATH=/path/to/quinela-wp
    ExecStart=/usr/bin/python3 scraper_service.py
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
"""

import sys
import os
import signal
import logging
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.scraper import QuinielaScraper
from config import Config

class ScraperService:
    def __init__(self):
        self.scraper = QuinielaScraper()
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('scraper_service')
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def start(self):
        """Start the scraper service"""
        self.logger.info("Starting Quiniela Scraper Service...")
        self.logger.info(f"Configuration: Scraping every {Config.SCRAPING_INTERVAL_HOURS} hours")
        self.logger.info(f"Target URL: {Config.SCRAPING_URL}")
        
        self.running = True
        
        try:
            # Start the scheduler (this will run indefinitely)
            self.scraper.start_scheduler()
        except KeyboardInterrupt:
            self.logger.info("Service stopped by user")
        except Exception as e:
            self.logger.error(f"Service error: {e}")
            sys.exit(1)
        finally:
            self.logger.info("Quiniela Scraper Service stopped")

def main():
    """Main entry point"""
    service = ScraperService()
    service.start()

if __name__ == "__main__":
    main()