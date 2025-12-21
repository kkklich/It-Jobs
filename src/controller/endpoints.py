from flask import jsonify
from services.scraper import scrape_justjoinit_tech_counts, save_to_db
from db.database import get_db_stats, get_tech_history
from datetime import datetime

def api_scrape():
    """load data from website endpoint"""
    tech_data = scrape_justjoinit_tech_counts()
    if tech_data:
        save_to_db(tech_data)
        return jsonify({
            'status': 'success',
            'message': 'Scraped and saved successfully',
            'data': dict(sorted(tech_data.items(), key=lambda x: x[1], reverse=True)),
            'count': len(tech_data)
        })
    return jsonify({'status': 'error', 'message': 'Failed to scrape'}), 500

def api_stats():
    """Get stats"""
    try:
        db_data = get_db_stats()
        return jsonify({
            'data': db_data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def api_tech_history(tech_name):
    """Get history for specific technology"""
    try:
        history = get_tech_history(tech_name)
        return jsonify({'technology': tech_name, 'history': history})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

