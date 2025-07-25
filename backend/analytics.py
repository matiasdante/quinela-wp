import logging
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
import statistics
from backend.database import QuinielaDatabase
from config import Config

class QuinielaAnalytics:
    def __init__(self):
        self.db = QuinielaDatabase()
        self.logger = logging.getLogger(__name__)
    
    def get_monthly_frequency_analysis(self, provincia: Optional[str] = None) -> Dict:
        """
        Analyze number frequency for the current month
        
        Returns:
            Dictionary with frequency analysis data
        """
        try:
            # Get current month data
            today = date.today()
            first_day = today.replace(day=1)
            
            results = self.db.get_results_by_date_range(first_day, today, provincia)
            
            if not results:
                return {
                    'month': today.strftime('%Y-%m'),
                    'provincia': provincia or 'Todas',
                    'total_draws': 0,
                    'most_frequent': [],
                    'statistics': {}
                }
            
            # Count number frequencies
            number_counts = Counter()
            for result in results:
                number_counts[result['numero']] += 1
            
            total_draws = len(results)
            
            # Calculate percentages and create frequency list
            most_frequent = []
            for numero, count in number_counts.most_common(20):
                percentage = (count / total_draws) * 100
                most_frequent.append({
                    'numero': numero,
                    'frequency': count,
                    'percentage': round(percentage, 2)
                })
            
            # Calculate statistics
            frequencies = list(number_counts.values())
            stats = {
                'total_unique_numbers': len(number_counts),
                'avg_frequency': round(statistics.mean(frequencies), 2) if frequencies else 0,
                'median_frequency': round(statistics.median(frequencies), 2) if frequencies else 0,
                'max_frequency': max(frequencies) if frequencies else 0,
                'min_frequency': min(frequencies) if frequencies else 0
            }
            
            return {
                'month': today.strftime('%Y-%m'),
                'provincia': provincia or 'Todas',
                'total_draws': total_draws,
                'most_frequent': most_frequent,
                'statistics': stats
            }
            
        except Exception as e:
            self.logger.error(f"Error in monthly frequency analysis: {e}")
            return {'error': str(e)}
    
    def get_hot_cold_numbers(self, days_back: int = 30, provincia: Optional[str] = None) -> Dict:
        """
        Identify hot (frequent) and cold (rare) numbers
        
        Args:
            days_back: Number of days to analyze
            provincia: Province to analyze (None for all)
        
        Returns:
            Dictionary with hot and cold numbers
        """
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=days_back)
            
            results = self.db.get_results_by_date_range(start_date, end_date, provincia)
            
            if not results:
                return {
                    'period': f'{start_date} to {end_date}',
                    'provincia': provincia or 'Todas',
                    'hot_numbers': [],
                    'cold_numbers': [],
                    'analysis': {}
                }
            
            # Count frequencies
            number_counts = Counter()
            for result in results:
                number_counts[result['numero']] += 1
            
            # Calculate thresholds
            frequencies = list(number_counts.values())
            if not frequencies:
                return {'error': 'No frequency data available'}
            
            avg_frequency = statistics.mean(frequencies)
            std_dev = statistics.stdev(frequencies) if len(frequencies) > 1 else 0
            
            hot_threshold = avg_frequency + (std_dev * 0.5)
            cold_threshold = avg_frequency - (std_dev * 0.5)
            
            # Classify numbers
            hot_numbers = []
            cold_numbers = []
            
            for numero, count in number_counts.items():
                percentage = (count / len(results)) * 100
                
                if count >= hot_threshold:
                    hot_numbers.append({
                        'numero': numero,
                        'frequency': count,
                        'percentage': round(percentage, 2)
                    })
                elif count <= cold_threshold:
                    cold_numbers.append({
                        'numero': numero,
                        'frequency': count,
                        'percentage': round(percentage, 2)
                    })
            
            # Sort by frequency
            hot_numbers.sort(key=lambda x: x['frequency'], reverse=True)
            cold_numbers.sort(key=lambda x: x['frequency'])
            
            return {
                'period': f'{start_date} to {end_date}',
                'provincia': provincia or 'Todas',
                'hot_numbers': hot_numbers[:10],  # Top 10 hot
                'cold_numbers': cold_numbers[:10],  # Top 10 cold
                'analysis': {
                    'total_numbers': len(number_counts),
                    'avg_frequency': round(avg_frequency, 2),
                    'hot_threshold': round(hot_threshold, 2),
                    'cold_threshold': round(cold_threshold, 2),
                    'total_draws': len(results)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in hot/cold analysis: {e}")
            return {'error': str(e)}
    
    def get_weekly_pattern_analysis(self, weeks_back: int = 8, provincia: Optional[str] = None) -> Dict:
        """
        Analyze patterns by day of the week
        
        Args:
            weeks_back: Number of weeks to analyze
            provincia: Province to analyze (None for all)
        
        Returns:
            Dictionary with weekly pattern analysis
        """
        try:
            end_date = date.today()
            start_date = end_date - timedelta(weeks=weeks_back)
            
            results = self.db.get_results_by_date_range(start_date, end_date, provincia)
            
            if not results:
                return {
                    'period': f'{start_date} to {end_date}',
                    'provincia': provincia or 'Todas',
                    'by_day': {},
                    'recommendations': []
                }
            
            # Group by day of week
            day_patterns = defaultdict(lambda: defaultdict(int))
            day_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            
            for result in results:
                result_date = datetime.strptime(result['date'], '%Y-%m-%d').date()
                day_of_week = result_date.weekday()  # 0 = Monday
                day_patterns[day_of_week][result['numero']] += 1
            
            # Analyze patterns for each day
            weekly_analysis = {}
            for day_idx in range(7):
                day_name = day_names[day_idx]
                numbers = day_patterns[day_idx]
                
                if numbers:
                    total_for_day = sum(numbers.values())
                    top_numbers = sorted(numbers.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    weekly_analysis[day_name] = {
                        'total_draws': total_for_day,
                        'top_numbers': [
                            {
                                'numero': num,
                                'frequency': freq,
                                'percentage': round((freq / total_for_day) * 100, 2)
                            }
                            for num, freq in top_numbers
                        ]
                    }
                else:
                    weekly_analysis[day_name] = {
                        'total_draws': 0,
                        'top_numbers': []
                    }
            
            # Generate recommendations for today
            today_day = date.today().weekday()
            today_name = day_names[today_day]
            
            recommendations = []
            if today_day in day_patterns:
                top_today = sorted(day_patterns[today_day].items(), key=lambda x: x[1], reverse=True)[:3]
                for numero, freq in top_today:
                    recommendations.append({
                        'numero': numero,
                        'reason': f'Frecuente los {today_name}s',
                        'frequency': freq
                    })
            
            return {
                'period': f'{start_date} to {end_date}',
                'provincia': provincia or 'Todas',
                'by_day': weekly_analysis,
                'today_recommendations': recommendations,
                'analysis_summary': {
                    'weeks_analyzed': weeks_back,
                    'total_draws': len(results)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in weekly pattern analysis: {e}")
            return {'error': str(e)}
    
    def generate_smart_recommendations(self, provincia: Optional[str] = None) -> Dict:
        """
        Generate intelligent number recommendations based on multiple analyses
        
        Returns:
            Dictionary with recommendations and reasoning
        """
        try:
            recommendations = []
            
            # Get hot numbers (last 30 days)
            hot_cold = self.get_hot_cold_numbers(30, provincia)
            if 'hot_numbers' in hot_cold:
                for hot in hot_cold['hot_numbers'][:3]:
                    recommendations.append({
                        'numero': hot['numero'],
                        'type': 'hot',
                        'reason': 'Número caliente (muy frecuente últimos 30 días)',
                        'confidence': min(hot['percentage'] * 2, 100),
                        'frequency': hot['frequency']
                    })
            
            # Get weekly pattern recommendations
            weekly = self.get_weekly_pattern_analysis(8, provincia)
            if 'today_recommendations' in weekly:
                for rec in weekly['today_recommendations'][:2]:
                    recommendations.append({
                        'numero': rec['numero'],
                        'type': 'pattern',
                        'reason': rec['reason'],
                        'confidence': min(rec['frequency'] * 10, 100),
                        'frequency': rec['frequency']
                    })
            
            # Get contrarian picks (some cold numbers that might be due)
            if 'cold_numbers' in hot_cold:
                for cold in hot_cold['cold_numbers'][:2]:
                    if cold['frequency'] > 0:  # Only if it has appeared at least once
                        recommendations.append({
                            'numero': cold['numero'],
                            'type': 'contrarian',
                            'reason': 'Número frío que podría salir (estrategia contraria)',
                            'confidence': max(20, 50 - cold['percentage']),
                            'frequency': cold['frequency']
                        })
            
            # Sort by confidence
            recommendations.sort(key=lambda x: x['confidence'], reverse=True)
            
            return {
                'provincia': provincia or 'Todas',
                'generated_at': datetime.now().isoformat(),
                'recommendations': recommendations[:8],  # Top 8 recommendations
                'disclaimer': 'Estas recomendaciones se basan en análisis estadístico de datos históricos y no garantizan resultados.',
                'analysis_basis': {
                    'hot_numbers_days': 30,
                    'pattern_analysis_weeks': 8,
                    'includes_contrarian': True
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return {'error': str(e)}
    
    def get_province_comparison(self) -> Dict:
        """Compare statistics across different provinces"""
        try:
            provinces = self.db.get_provinces()
            comparison = {}
            
            for provincia in provinces:
                monthly_data = self.get_monthly_frequency_analysis(provincia)
                hot_cold = self.get_hot_cold_numbers(30, provincia)
                
                comparison[provincia] = {
                    'monthly_draws': monthly_data.get('total_draws', 0),
                    'unique_numbers': monthly_data.get('statistics', {}).get('total_unique_numbers', 0),
                    'hot_numbers_count': len(hot_cold.get('hot_numbers', [])),
                    'cold_numbers_count': len(hot_cold.get('cold_numbers', [])),
                    'top_number': monthly_data.get('most_frequent', [{}])[0] if monthly_data.get('most_frequent') else None
                }
            
            return {
                'generated_at': datetime.now().isoformat(),
                'provinces': comparison,
                'summary': {
                    'total_provinces': len(provinces),
                    'most_active': max(comparison.items(), key=lambda x: x[1]['monthly_draws'])[0] if comparison else None
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in province comparison: {e}")
            return {'error': str(e)}
    
    def detect_patterns(self, provincia: Optional[str] = None) -> Dict:
        """
        Detect interesting patterns in the data
        
        Returns:
            Dictionary with detected patterns and alerts
        """
        try:
            patterns = []
            alerts = []
            
            # Check for consecutive numbers
            recent_results = self.db.get_results_by_date_range(
                date.today() - timedelta(days=7),
                date.today(),
                provincia
            )
            
            if recent_results:
                recent_numbers = [r['numero'] for r in recent_results[-10:]]  # Last 10 draws
                
                # Look for consecutive numbers
                for i in range(len(recent_numbers) - 1):
                    try:
                        current = int(recent_numbers[i])
                        next_num = int(recent_numbers[i + 1])
                        if abs(current - next_num) == 1:
                            patterns.append({
                                'type': 'consecutive',
                                'description': f'Números consecutivos detectados: {current}, {next_num}',
                                'confidence': 'medium'
                            })
                    except ValueError:
                        continue
                
                # Check for repeated numbers in recent draws
                number_counts = Counter(recent_numbers)
                for numero, count in number_counts.items():
                    if count >= 3:
                        alerts.append({
                            'type': 'high_frequency',
                            'message': f'Número {numero} apareció {count} veces en los últimos 10 sorteos',
                            'severity': 'high' if count >= 4 else 'medium'
                        })
            
            # Check for long absence patterns
            all_time_results = self.db.get_results_by_date_range(
                date.today() - timedelta(days=60),
                date.today(),
                provincia
            )
            
            if all_time_results:
                all_numbers = set(r['numero'] for r in all_time_results)
                recent_numbers_set = set(r['numero'] for r in recent_results)
                
                missing_numbers = []
                for numero in all_numbers:
                    if numero not in recent_numbers_set:
                        # Check how long it's been missing
                        last_seen = None
                        for result in reversed(all_time_results):
                            if result['numero'] == numero:
                                last_seen = result['date']
                                break
                        
                        if last_seen:
                            last_date = datetime.strptime(last_seen, '%Y-%m-%d').date()
                            days_absent = (date.today() - last_date).days
                            
                            if days_absent >= 14:
                                patterns.append({
                                    'type': 'long_absence',
                                    'description': f'Número {numero} ausente por {days_absent} días',
                                    'confidence': 'low' if days_absent < 30 else 'medium'
                                })
            
            return {
                'provincia': provincia or 'Todas',
                'generated_at': datetime.now().isoformat(),
                'patterns': patterns,
                'alerts': alerts,
                'analysis_period': '60 días'
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting patterns: {e}")
            return {'error': str(e)}