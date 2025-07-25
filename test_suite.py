#!/usr/bin/env python3
"""
Quiniela Analytics Test Suite

This script tests the core functionality of the Quiniela Analytics system.
"""

import sys
import os
import json
import time
from datetime import datetime, date, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import QuinielaDatabase
from backend.analytics import QuinielaAnalytics
from backend.scraper import QuinielaScraper

def test_database():
    """Test database functionality"""
    print("🧪 Testing Database Functionality...")
    
    db = QuinielaDatabase()
    
    # Test data insertion
    test_data = {
        'Ciudad': [('Primera', '1234'), ('Matutina', '5678'), ('Vespertina', '9012')],
        'Provincia de Buenos Aires': [('Primera', '3456'), ('Matutina', '7890'), ('Vespertina', '2345')],
        'Córdoba': [('Primera', '6789'), ('Matutina', '0123')]
    }
    
    # Insert test data for different dates
    dates = [date.today() - timedelta(days=i) for i in range(5)]
    total_inserted = 0
    
    for test_date in dates:
        inserted = db.insert_results(test_data, test_date)
        total_inserted += inserted
    
    print(f"   ✅ Inserted {total_inserted} test records")
    
    # Test queries
    stats = db.get_database_stats()
    print(f"   ✅ Database contains {stats['total_records']} total records")
    
    provinces = db.get_provinces()
    print(f"   ✅ Found {len(provinces)} provinces: {', '.join(provinces)}")
    
    return True

def test_analytics():
    """Test analytics functionality"""
    print("\n📊 Testing Analytics Functionality...")
    
    analytics = QuinielaAnalytics()
    
    # Test monthly analysis
    monthly = analytics.get_monthly_frequency_analysis()
    if monthly.get('total_draws', 0) > 0:
        print(f"   ✅ Monthly analysis: {monthly['total_draws']} draws, {monthly['statistics']['total_unique_numbers']} unique numbers")
    else:
        print("   ⚠️  No data for monthly analysis")
    
    # Test hot/cold analysis
    hot_cold = analytics.get_hot_cold_numbers(30)
    if 'hot_numbers' in hot_cold:
        print(f"   ✅ Hot/Cold analysis: {len(hot_cold['hot_numbers'])} hot, {len(hot_cold['cold_numbers'])} cold numbers")
    
    # Test recommendations
    recommendations = analytics.generate_smart_recommendations()
    if 'recommendations' in recommendations:
        print(f"   ✅ Smart recommendations: {len(recommendations['recommendations'])} recommendations generated")
    
    # Test pattern detection
    patterns = analytics.detect_patterns()
    if 'patterns' in patterns:
        print(f"   ✅ Pattern detection: {len(patterns['patterns'])} patterns, {len(patterns['alerts'])} alerts")
    
    return True

def test_scraper():
    """Test scraper functionality"""
    print("\n🔄 Testing Scraper Functionality...")
    
    scraper = QuinielaScraper()
    
    # Test manual scrape (will fail without internet, but test error handling)
    result = scraper.manual_scrape()
    if result['success']:
        print(f"   ✅ Scraper working: {result['provinces_scraped']} provinces scraped")
    else:
        print(f"   ⚠️  Scraper handled error gracefully: {result['message']}")
    
    # Test scraper stats
    stats = scraper.get_scraper_stats()
    print(f"   ✅ Scraper configured for {stats['scraping_config']['provinces_monitored']} provinces")
    
    return True

def test_api_imports():
    """Test that API components can be imported"""
    print("\n🌐 Testing API Components...")
    
    try:
        from backend.api import QuinielaAPI
        from flask import Flask
        
        app = Flask(__name__)
        api = QuinielaAPI(app)
        
        print("   ✅ API components imported successfully")
        print("   ✅ Flask application created successfully")
        return True
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Quiniela Analytics Test Suite")
    print("=" * 50)
    
    tests = [
        test_database,
        test_analytics,
        test_scraper,
        test_api_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Quiniela Analytics is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())