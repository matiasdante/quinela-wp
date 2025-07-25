import requests
import logging
import schedule
import time
from datetime import datetime, date
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
from backend.database import QuinielaDatabase
from config import Config, PROVINCIAS

class QuinielaScraper:
    def __init__(self):
        self.db = QuinielaDatabase()
        self.base_url = Config.SCRAPING_URL
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def scrape_current_results(self) -> Dict[str, List[Tuple[str, str]]]:
        """
        Scrape current lottery results from the website
        
        Returns:
            Dictionary with provincia as key and list of (sorteo, numero) tuples as value
        """
        try:
            response = requests.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            resultados_quiniela = {}
            
            for id_div, nombre_provincia in PROVINCIAS:
                resultados = self._extract_provincia_results(soup, id_div, nombre_provincia)
                resultados_quiniela[nombre_provincia] = resultados
            
            self.logger.info(f"Successfully scraped results for {len(resultados_quiniela)} provinces")
            return resultados_quiniela
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching data from {self.base_url}: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {e}")
            return {}
    
    def _extract_provincia_results(self, soup: BeautifulSoup, id_div: str, nombre_provincia: str) -> List[Tuple[str, str]]:
        """Extract results for a specific province"""
        try:
            div = soup.find(id=id_div)
            resultados = []
            
            if div:
                items = div.find_all('div', class_='col-xs-5')
                for item in items:
                    sorteo = item.find('a', class_='enlaces-quinielas-2021')
                    numero = item.find('a', class_='enlaces-numeros')
                    
                    if sorteo and numero:
                        sorteo_text = sorteo.text.strip()
                        numero_text = numero.text.strip()
                        
                        # Validate and clean the data
                        if sorteo_text and numero_text:
                            resultados.append((sorteo_text, numero_text))
                
                self.logger.debug(f"Extracted {len(resultados)} results for {nombre_provincia}")
                return resultados
            else:
                self.logger.warning(f"No div found with id {id_div} for {nombre_provincia}")
                return "No se encontraron resultados"
                
        except Exception as e:
            self.logger.error(f"Error extracting results for {nombre_provincia}: {e}")
            return "Error al extraer resultados"
    
    def scrape_and_store(self) -> bool:
        """
        Scrape current results and store them in the database
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Starting scheduled scraping...")
            results = self.scrape_current_results()
            
            if results:
                inserted_count = self.db.insert_results(results)
                self.logger.info(f"Scraping completed: {inserted_count} records inserted")
                return True
            else:
                self.logger.warning("No results obtained from scraping")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in scrape_and_store: {e}")
            return False
    
    def scrape_historical_data(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> bool:
        """
        Scrape historical data (if the website supports it)
        This is a placeholder for future implementation when historical URLs are available
        """
        self.logger.info("Historical data scraping not yet implemented")
        return False
    
    def start_scheduler(self):
        """Start the automated scraping scheduler"""
        self.logger.info(f"Starting scraper scheduler - will run every {Config.SCRAPING_INTERVAL_HOURS} hours")
        
        # Schedule regular scraping
        schedule.every(Config.SCRAPING_INTERVAL_HOURS).hours.do(self.scrape_and_store)
        
        # Also schedule at specific times for better coverage
        schedule.every().day.at("12:00").do(self.scrape_and_store)
        schedule.every().day.at("18:00").do(self.scrape_and_store)
        schedule.every().day.at("21:00").do(self.scrape_and_store)
        
        # Run once immediately
        self.scrape_and_store()
        
        # Keep the scheduler running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scraper scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"Scheduler error: {e}")
    
    def manual_scrape(self) -> Dict:
        """
        Perform a manual scrape and return results with metadata
        
        Returns:
            Dictionary with results and metadata
        """
        start_time = datetime.now()
        results = self.scrape_current_results()
        
        if results:
            inserted_count = self.db.insert_results(results)
            success = True
            message = f"Successfully scraped and stored {inserted_count} results"
        else:
            inserted_count = 0
            success = False
            message = "No results were obtained from scraping"
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        return {
            'success': success,
            'message': message,
            'results': results,
            'inserted_count': inserted_count,
            'scrape_time': start_time.isoformat(),
            'duration_seconds': duration,
            'provinces_scraped': len([p for p in results.values() if not isinstance(p, str)])
        }
    
    def get_scraper_stats(self) -> Dict:
        """Get statistics about the scraper performance"""
        db_stats = self.db.get_database_stats()
        
        return {
            'database_stats': db_stats,
            'scraping_config': {
                'base_url': self.base_url,
                'interval_hours': Config.SCRAPING_INTERVAL_HOURS,
                'provinces_monitored': len(PROVINCIAS)
            },
            'provinces': [nombre for _, nombre in PROVINCIAS]
        }

def run_scraper_service():
    """Standalone function to run the scraper service"""
    scraper = QuinielaScraper()
    scraper.start_scheduler()

if __name__ == "__main__":
    run_scraper_service()