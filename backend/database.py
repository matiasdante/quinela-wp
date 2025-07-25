import sqlite3
import os
import logging
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from config import Config

class QuinielaDatabase:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    provincia TEXT NOT NULL,
                    sorteo TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(date, provincia, sorteo)
                )
            ''')
            
            # Create analytics cache table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT UNIQUE NOT NULL,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                )
            ''')
            
            # Create indices for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_date ON results(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_provincia ON results(provincia)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_numero ON results(numero)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_expires ON analytics_cache(expires_at)')
            
            conn.commit()
            logging.info("Database initialized successfully")
    
    def insert_results(self, results_data: Dict[str, List[Tuple[str, str]]], result_date: Optional[date] = None) -> int:
        """
        Insert lottery results into the database
        
        Args:
            results_data: Dictionary with provincia as key and list of (sorteo, numero) tuples as value
            result_date: Date of the results (defaults to today)
        
        Returns:
            Number of records inserted
        """
        if result_date is None:
            result_date = date.today()
        
        inserted_count = 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for provincia, resultados in results_data.items():
                if isinstance(resultados, str):  # Skip "No se encontraron resultados"
                    continue
                
                for sorteo, numero in resultados:
                    try:
                        cursor.execute('''
                            INSERT OR REPLACE INTO results (date, provincia, sorteo, numero)
                            VALUES (?, ?, ?, ?)
                        ''', (result_date, provincia, sorteo, numero))
                        inserted_count += 1
                    except sqlite3.Error as e:
                        logging.error(f"Error inserting result for {provincia}: {e}")
            
            conn.commit()
        
        logging.info(f"Inserted {inserted_count} results for {result_date}")
        return inserted_count
    
    def get_results_by_date_range(self, start_date: date, end_date: date, provincia: Optional[str] = None) -> List[Dict]:
        """Get results within a date range, optionally filtered by provincia"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT date, provincia, sorteo, numero, created_at
                FROM results
                WHERE date BETWEEN ? AND ?
            '''
            params = [start_date, end_date]
            
            if provincia:
                query += ' AND provincia = ?'
                params.append(provincia)
            
            query += ' ORDER BY date DESC, provincia, sorteo'
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_most_frequent_numbers(self, days_back: int = 30, provincia: Optional[str] = None) -> List[Dict]:
        """Get the most frequent numbers in the last N days"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT numero, COUNT(*) as frequency,
                       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM results 
                                                WHERE date >= date('now', '-{} days')
                                                {}), 2) as percentage
                FROM results
                WHERE date >= date('now', '-{} days')
                {}
                GROUP BY numero
                ORDER BY frequency DESC
                LIMIT 20
            '''.format(
                days_back,
                'AND provincia = ?' if provincia else '',
                days_back,
                'AND provincia = ?' if provincia else ''
            )
            
            params = [provincia] * 2 if provincia else []
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_frequency_by_month(self, provincia: Optional[str] = None) -> List[Dict]:
        """Get number frequency grouped by month"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT strftime('%Y-%m', date) as month, numero, COUNT(*) as frequency
                FROM results
                WHERE date >= date('now', '-12 months')
                {}
                GROUP BY strftime('%Y-%m', date), numero
                ORDER BY month DESC, frequency DESC
            '''.format('AND provincia = ?' if provincia else '')
            
            params = [provincia] if provincia else []
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_weekly_patterns(self, provincia: Optional[str] = None) -> List[Dict]:
        """Analyze weekly patterns in number appearances"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT 
                    strftime('%w', date) as day_of_week,
                    numero,
                    COUNT(*) as frequency
                FROM results
                WHERE date >= date('now', '-8 weeks')
                {}
                GROUP BY strftime('%w', date), numero
                ORDER BY day_of_week, frequency DESC
            '''.format('AND provincia = ?' if provincia else '')
            
            params = [provincia] if provincia else []
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_provinces(self) -> List[str]:
        """Get list of all provinces in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT provincia FROM results ORDER BY provincia')
            return [row[0] for row in cursor.fetchall()]
    
    def get_database_stats(self) -> Dict:
        """Get general database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            stats = {}
            
            # Total records
            cursor.execute('SELECT COUNT(*) as total FROM results')
            stats['total_records'] = cursor.fetchone()['total']
            
            # Date range
            cursor.execute('SELECT MIN(date) as first_date, MAX(date) as last_date FROM results')
            date_range = cursor.fetchone()
            stats['date_range'] = {
                'first_date': date_range['first_date'],
                'last_date': date_range['last_date']
            }
            
            # Records by province
            cursor.execute('''
                SELECT provincia, COUNT(*) as count 
                FROM results 
                GROUP BY provincia 
                ORDER BY count DESC
            ''')
            stats['by_province'] = [dict(row) for row in cursor.fetchall()]
            
            return stats
    
    def cleanup_old_cache(self):
        """Remove expired cache entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM analytics_cache WHERE expires_at < datetime("now")')
            deleted = cursor.rowcount
            conn.commit()
            
            if deleted > 0:
                logging.info(f"Cleaned up {deleted} expired cache entries")