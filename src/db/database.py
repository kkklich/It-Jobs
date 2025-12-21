import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime


def create_db_tables():
    """Create required table if not exists"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS justjoinit_jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            dateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
            CompanyName VARCHAR(100) NOT NULL,
            technologyName VARCHAR(100) NOT NULL,
            techCounts INT NOT NULL,
            INDEX idx_date (dateTime),
            INDEX idx_tech (technologyName)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Database table ready")
    except Error as e:
        print(f"❌ DB Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def get_db_stats_latest():
    """Get latest stats and top technologies"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT technologyName, techCounts, dateTime
            FROM justjoinit_jobs
            WHERE dateTime = (SELECT MAX(dateTime) FROM justjoinit_jobs)
            ORDER BY techCounts DESC
        """)
        latest = cursor.fetchall()

        cursor.execute("""
            SELECT technologyName, AVG(techCounts) as avg_count, COUNT(*) as samples
            FROM justjoinit_jobs
            GROUP BY technologyName
            ORDER BY avg_count DESC
            LIMIT 10
        """)
        top_tech = cursor.fetchall()

        cursor.close()
        connection.close()
        return latest, top_tech
    except Error as e:
        print(f"❌ DB Query Error: {e}")
        return [], []


def get_tech_history(tech_name):
    """Get history for specific technology"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT dateTime, techCounts
            FROM justjoinit_jobs
            WHERE technologyName = %s
            ORDER BY dateTime DESC
            LIMIT 30
        """, (tech_name,))

        history = cursor.fetchall()
        cursor.close()
        connection.close()
        return history
    except Error as e:
        print(f"❌ DB History Error: {e}")
        return []


def get_db_stats():
    """Get data for line chart: techCounts over time per technologyName"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(buffered=True, dictionary=True)

        # Get ALL data ordered by dateTime for line chart (technologyName, dateTime, techCounts)
        cursor.execute("""
            SELECT technologyName, dateTime, techCounts
            FROM justjoinit_jobs
            ORDER BY technologyName ASC, dateTime DESC
        """)
        chart_data = cursor.fetchall()

        print(chart_data)

        cursor.close()
        connection.close()
        return chart_data

    except Error as e:
        print(f"❌ DB Query Error: {e}")
        return []
