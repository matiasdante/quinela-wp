from flask import Flask, jsonify, request
from datetime import datetime, date, timedelta
import logging
from typing import Dict, List, Optional
from backend.scraper import QuinielaScraper
from config import Config

class QuinielaAPI:
    def __init__(self, app: Flask, api_only=False):
        self.app = app
        self.api_only = api_only
        self.scraper = QuinielaScraper()
        
        # In-memory storage: list of records {date, provincia, sorteo, numero, created_at}
        self._results: List[Dict] = []
        
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
                # Store results in memory
                inserted = 0
                if results:
                    inserted = self._insert_results(results)

                return jsonify({
                    'success': True,
                    'message': f'Scraping completed successfully, inserted {inserted} records',
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
            return jsonify({
                'success': False,
                'error': 'Endpoint removed: analytics disabled'
            }), 410
        
        @self.app.route('/api/analytics/hot-cold')
        def get_hot_cold_analysis():
            """Get hot and cold numbers analysis"""
            return jsonify({
                'success': False,
                'error': 'Endpoint removed: analytics disabled'
            }), 410
        
        @self.app.route('/api/analytics/patterns')
        def get_pattern_analysis():
            """Get pattern analysis"""
            return jsonify({
                'success': False,
                'error': 'Endpoint removed: analytics disabled'
            }), 410
        
        @self.app.route('/api/recommendations')
        def get_recommendations():
            """Get smart recommendations"""
            return jsonify({
                'success': False,
                'error': 'Endpoint removed: recommendations disabled'
            }), 410
        
        @self.app.route('/api/history')
        def get_history():
            """Get historical data"""
            try:
                days = request.args.get('days', 30, type=int)
                provincia = request.args.get('provincia')
                sorteo = request.args.get('sorteo')

                start_date = date.today() - timedelta(days=days)
                history = self._get_results_by_date_range(start_date, date.today(), provincia)

                # If a specific sorteo filter was provided, filter results
                if sorteo:
                    history = [h for h in history if h.get('sorteo') == sorteo]

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
            return jsonify({
                'success': False,
                'error': 'Endpoint removed: analytics disabled'
            }), 410
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get general statistics"""
            try:
                db_stats = self._get_database_stats()
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
                provinces = self._get_provinces()
                return jsonify({
                    'success': True,
                    'data': provinces
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    # In-memory database methods
    def _insert_results(self, results_data: Dict[str, List], result_date: Optional[date] = None) -> int:
        """Insert results into in-memory storage"""
        if result_date is None:
            result_date = date.today()

        inserted = 0
        for provincia, resultados in results_data.items():
            if isinstance(resultados, str):
                continue
            for sorteo, numero in resultados:
                # Replace existing same (date, provincia, sorteo) if exists
                existing = next(
                    (r for r in self._results 
                     if r['date'] == result_date and r['provincia'] == provincia and r['sorteo'] == sorteo), 
                    None
                )
                record = {
                    'date': result_date,
                    'provincia': provincia,
                    'sorteo': sorteo,
                    'numero': numero,
                    'created_at': datetime.now().isoformat()
                }
                if existing:
                    existing.update(record)
                else:
                    self._results.append(record)
                inserted += 1

        logging.info(f"Inserted {inserted} results (in-memory) for {result_date}")
        return inserted

    def _get_results_by_date_range(self, start_date: date, end_date: date, provincia: Optional[str] = None) -> List[Dict]:
        """Get results from in-memory storage by date range"""
        res = [r for r in self._results if start_date <= r['date'] <= end_date]
        if provincia:
            res = [r for r in res if r['provincia'] == provincia]
        # Sort by date desc, provincia, sorteo
        res.sort(key=lambda x: (x['date'], x['provincia'], x['sorteo']), reverse=True)
        # Convert date to iso string for compatibility with API responses
        out = []
        for r in res:
            copy = r.copy()
            if isinstance(copy['date'], date):
                copy['date'] = copy['date'].isoformat()
            out.append(copy)
        return out

    def _get_provinces(self) -> List[str]:
        """Get list of unique provinces from in-memory storage"""
        return sorted(list({r['provincia'] for r in self._results}))

    def _get_database_stats(self) -> Dict:
        """Get statistics from in-memory storage"""
        stats = {}
        stats['total_records'] = len(self._results)
        if self._results:
            dates = [r['date'] for r in self._results]
            first = min(dates)
            last = max(dates)
            stats['date_range'] = {
                'first_date': first.isoformat() if isinstance(first, date) else str(first),
                'last_date': last.isoformat() if isinstance(last, date) else str(last)
            }
        else:
            stats['date_range'] = {'first_date': None, 'last_date': None}

        # Records by province
        by_prov = {}
        for r in self._results:
            by_prov[r['provincia']] = by_prov.get(r['provincia'], 0) + 1
        stats['by_province'] = [
            {'provincia': k, 'count': v} 
            for k, v in sorted(by_prov.items(), key=lambda x: x[1], reverse=True)
        ]
        return stats

    def clear_all(self):
        """Clear all in-memory data"""
        self._results.clear()