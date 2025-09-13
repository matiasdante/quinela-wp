from flask import Flask, jsonify, request
from datetime import datetime, date, timedelta
import logging
import os
from backend.scraper import QuinielaScraper
from backend.analytics import QuinielaAnalytics
from backend.database import QuinielaDatabase
from config import Config

class QuinielaAPI:
    def __init__(self, app: Flask, api_only=False):
        self.app = app
        self.api_only = api_only
        self.scraper = QuinielaScraper()
        self.analytics = QuinielaAnalytics()
        self.db = QuinielaDatabase()
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self._register_routes()
    
    def _register_routes(self):
        """Register all API routes"""
        
        # Health check
        @self.app.route('/api/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'Quiniela API'
            })
        
        # API Routes
        @self.app.route('/api/current')
        def get_current_results():
            """Get current lottery results"""
            try:
                results = self.scraper.scrape_current_results()
                return jsonify({
                    'success': True,
                    'data': results,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/scrape', methods=['POST'])
        def manual_scrape():
            """Manually trigger scraping"""
            try:
                results = self.scraper.scrape_current_results()
                # Store results in database
                for provincia, data in results.items():
                    if isinstance(data, list):
                        for sorteo, numero in data:
                            self.db.store_result(provincia, sorteo, numero)
                
                return jsonify({
                    'success': True,
                    'message': 'Scraping completed successfully',
                    'data': results,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analytics/monthly')
        def get_monthly_analysis():
            """Get monthly frequency analysis"""
            try:
                analysis = self.analytics.get_monthly_frequency_analysis()
                return jsonify({
                    'success': True,
                    'data': analysis,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analytics/hot-cold')
        def get_hot_cold_analysis():
            """Get hot and cold numbers analysis"""
            try:
                days = request.args.get('days', 30, type=int)
                analysis = self.analytics.get_hot_cold_numbers(days)
                return jsonify({
                    'success': True,
                    'data': analysis,
                    'period_days': days,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analytics/patterns')
        def get_pattern_analysis():
            """Get pattern analysis"""
            try:
                min_frequency = request.args.get('min_frequency', 0.1, type=float)
                patterns = self.analytics.detect_patterns(min_frequency_threshold=min_frequency)
                return jsonify({
                    'success': True,
                    'data': patterns,
                    'min_frequency_threshold': min_frequency,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/recommendations')
        def get_recommendations():
            """Get smart recommendations"""
            try:
                recommendations = self.analytics.generate_smart_recommendations()
                return jsonify({
                    'success': True,
                    'data': recommendations,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/history')
        def get_history():
            """Get historical data"""
            try:
                days = request.args.get('days', 30, type=int)
                provincia = request.args.get('provincia')
                sorteo = request.args.get('sorteo')
                
                history = self.db.get_historical_data(days, provincia, sorteo)
                return jsonify({
                    'success': True,
                    'data': history,
                    'filters': {
                        'days': days,
                        'provincia': provincia,
                        'sorteo': sorteo
                    },
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/frequency')
        def get_frequency_analysis():
            """Get frequency analysis for specific numbers"""
            try:
                days = request.args.get('days', 30, type=int)
                numero = request.args.get('numero', type=int)
                
                if numero:
                    frequency = self.analytics.get_number_frequency(numero, days)
                    return jsonify({
                        'success': True,
                        'data': {
                            'numero': numero,
                            'frequency': frequency,
                            'period_days': days
                        },
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    frequencies = self.analytics.get_all_frequencies(days)
                    return jsonify({
                        'success': True,
                        'data': frequencies,
                        'period_days': days,
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get general statistics"""
            try:
                db_stats = self.db.get_database_stats()
                scraper_stats = self.scraper.get_scraper_stats()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'database': db_stats,
                        'scraper': scraper_stats,
                        'timestamp': datetime.now().isoformat()
                    }
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/provinces')
        def get_provinces():
            """Get list of available provinces"""
            try:
                provinces = self.db.get_provinces()
                return jsonify({
                    'success': True,
                    'data': provinces
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500