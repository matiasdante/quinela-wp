from flask import Flask, jsonify, request, render_template_string
from datetime import datetime, date, timedelta
import logging
import os
from backend.scraper import QuinielaScraper
from backend.analytics import QuinielaAnalytics
from backend.database import QuinielaDatabase
from config import Config

class QuinielaAPI:
    def __init__(self, app: Flask):
        self.app = app
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
        
        # Legacy route (maintain backward compatibility)
        @self.app.route('/')
        def mostrar_resultados():
            return self.render_dashboard()
        
        # Dashboard route
        @self.app.route('/dashboard')
        def dashboard():
            return self.render_dashboard()
        
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
            """Trigger manual scraping"""
            try:
                result = self.scraper.manual_scrape()
                return jsonify(result)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analytics/monthly')
        def get_monthly_analytics():
            """Get monthly frequency analysis"""
            provincia = request.args.get('provincia')
            try:
                data = self.analytics.get_monthly_frequency_analysis(provincia)
                return jsonify({
                    'success': True,
                    'data': data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analytics/hot-cold')
        def get_hot_cold():
            """Get hot and cold numbers analysis"""
            provincia = request.args.get('provincia')
            days = request.args.get('days', 30, type=int)
            try:
                data = self.analytics.get_hot_cold_numbers(days, provincia)
                return jsonify({
                    'success': True,
                    'data': data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/analytics/weekly-patterns')
        def get_weekly_patterns():
            """Get weekly pattern analysis"""
            provincia = request.args.get('provincia')
            weeks = request.args.get('weeks', 8, type=int)
            try:
                data = self.analytics.get_weekly_pattern_analysis(weeks, provincia)
                return jsonify({
                    'success': True,
                    'data': data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/recommendations')
        def get_recommendations():
            """Get intelligent number recommendations"""
            provincia = request.args.get('provincia')
            try:
                data = self.analytics.generate_smart_recommendations(provincia)
                return jsonify({
                    'success': True,
                    'data': data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/patterns')
        def get_patterns():
            """Get detected patterns and alerts"""
            provincia = request.args.get('provincia')
            try:
                data = self.analytics.detect_patterns(provincia)
                return jsonify({
                    'success': True,
                    'data': data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/compare-provinces')
        def compare_provinces():
            """Compare statistics across provinces"""
            try:
                data = self.analytics.get_province_comparison()
                return jsonify({
                    'success': True,
                    'data': data
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/historical')
        def get_historical():
            """Get historical results"""
            try:
                start_date = request.args.get('start_date')
                end_date = request.args.get('end_date')
                provincia = request.args.get('provincia')
                
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                else:
                    start_date = date.today() - timedelta(days=30)
                
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                else:
                    end_date = date.today()
                
                results = self.db.get_results_by_date_range(start_date, end_date, provincia)
                return jsonify({
                    'success': True,
                    'data': {
                        'results': results,
                        'period': {
                            'start': start_date.isoformat(),
                            'end': end_date.isoformat()
                        },
                        'total_records': len(results)
                    }
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
    
    def render_dashboard(self):
        """Render the main dashboard"""
        try:
            # Get current results for compatibility
            current_results = self.scraper.scrape_current_results()
            
            # Get some basic analytics for the dashboard
            monthly_analysis = self.analytics.get_monthly_frequency_analysis()
            recommendations = self.analytics.generate_smart_recommendations()
            
            template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiniela Analytics Dashboard</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
            color: white; 
            padding: 30px; 
            text-align: center;
        }
        .header h1 { margin: 0; font-size: 2.5em; }
        .header p { margin: 10px 0 0; opacity: 0.9; }
        .content { padding: 30px; }
        .section { 
            margin-bottom: 30px; 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 20px;
            border-left: 4px solid #2a5298;
        }
        .section h2 { 
            color: #2a5298; 
            margin-top: 0; 
            display: flex; 
            align-items: center;
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
        }
        .card { 
            background: white; 
            border-radius: 8px; 
            padding: 20px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-top: 3px solid #2a5298;
        }
        .card h3 { margin-top: 0; color: #2a5298; }
        .results-list { list-style: none; padding: 0; }
        .results-list li { 
            padding: 8px 0; 
            border-bottom: 1px solid #eee; 
            display: flex; 
            justify-content: space-between;
        }
        .number { 
            background: #2a5298; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 4px; 
            font-weight: bold;
        }
        .percentage { 
            color: #666; 
            font-size: 0.9em;
        }
        .recommendation {
            background: linear-gradient(135deg, #ff6b6b, #ffa500);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .recommendation .type {
            font-size: 0.8em;
            opacity: 0.9;
            text-transform: uppercase;
        }
        .api-links {
            background: #e9ecef;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .api-links a {
            color: #2a5298;
            text-decoration: none;
            margin-right: 15px;
            font-weight: 500;
        }
        .api-links a:hover {
            text-decoration: underline;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        .stat {
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #2a5298;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎲 Quiniela Analytics</h1>
            <p>Sistema Avanzado de Análisis de Datos - Resultados y Predicciones Inteligentes</p>
        </div>
        
        <div class="content">
            <!-- Current Results Section -->
            <div class="section">
                <h2>📊 Resultados Actuales</h2>
                <div class="grid">
                    {% for provincia, resultados in current_results.items() %}
                    <div class="card">
                        <h3>{{ provincia }}</h3>
                        {% if resultados != "No se encontraron resultados" and resultados is not string %}
                        <ul class="results-list">
                            {% for sorteo, numero in resultados %}
                            <li>
                                <span>{{ sorteo }}</span>
                                <span class="number">{{ numero }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                        {% else %}
                        <p>{{ resultados }}</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Analytics Section -->
            {% if monthly_analysis.get('most_frequent') %}
            <div class="section">
                <h2>📈 Análisis del Mes</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">{{ monthly_analysis.total_draws }}</div>
                        <div class="stat-label">Sorteos</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{{ monthly_analysis.statistics.total_unique_numbers }}</div>
                        <div class="stat-label">Números Únicos</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{{ monthly_analysis.statistics.avg_frequency }}</div>
                        <div class="stat-label">Frecuencia Promedio</div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>Números Más Frecuentes del Mes</h3>
                    <ul class="results-list">
                        {% for item in monthly_analysis.most_frequent[:10] %}
                        <li>
                            <span class="number">{{ item.numero }}</span>
                            <span class="percentage">{{ item.frequency }} veces ({{ item.percentage }}%)</span>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            {% endif %}

            <!-- Recommendations Section -->
            {% if recommendations.get('recommendations') %}
            <div class="section">
                <h2>🎯 Recomendaciones Inteligentes</h2>
                {% for rec in recommendations.recommendations[:5] %}
                <div class="recommendation">
                    <div class="type">{{ rec.type }}</div>
                    <strong>Número {{ rec.numero }}</strong>
                    <div>{{ rec.reason }}</div>
                    <div style="font-size: 0.9em; margin-top: 5px;">
                        Confianza: {{ rec.confidence }}% | Frecuencia: {{ rec.frequency }}
                    </div>
                </div>
                {% endfor %}
                <p style="font-size: 0.9em; color: #666; margin-top: 15px;">
                    {{ recommendations.disclaimer }}
                </p>
            </div>
            {% endif %}

            <!-- API Documentation -->
            <div class="section">
                <h2>🔗 API Endpoints</h2>
                <div class="api-links">
                    <strong>Datos en Tiempo Real:</strong><br>
                    <a href="/api/current">Resultados Actuales</a>
                    <a href="/api/analytics/monthly">Análisis Mensual</a>
                    <a href="/api/analytics/hot-cold">Números Calientes/Fríos</a>
                    <a href="/api/recommendations">Recomendaciones</a>
                    <a href="/api/patterns">Patrones Detectados</a>
                    <a href="/api/stats">Estadísticas</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
            """
            
            return render_template_string(
                template, 
                current_results=current_results,
                monthly_analysis=monthly_analysis,
                recommendations=recommendations
            )
            
        except Exception as e:
            logging.error(f"Error rendering dashboard: {e}")
            return f"Error loading dashboard: {str(e)}", 500