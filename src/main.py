from flask import Flask
from flask_cors import CORS
from controller.endpoints import api_scrape, api_stats, api_tech_history
from db.database import create_db_tables

app = Flask(__name__)
CORS(app)

# # API Routes
@app.route('/api/stats', methods=['GET'])
def stats_endpoint():
    return api_stats()

@app.route('/api/history/<tech_name>', methods=['GET'])
def history_endpoint(tech_name):
    return api_tech_history(tech_name)

@app.route('/api/loadJobs', methods=['GET'])
def load_jobs():
    return api_scrape()

if __name__ == '__main__':
    create_db_tables()

    print("🚀 API running on http://localhost:5000")
    print("📈 Endpoints: /api/scrape, /api/stats, /api/history/<tech>")
    app.run(host='0.0.0.0', port=5000, debug=False)