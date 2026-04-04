import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from src.config import DB_CONFIG

def scrape_justjoinit_tech_counts(url='https://justjoin.it/job-offers/all-locations'):
    """Scrape JustJoin.it technology job counts"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        tech_counts = {}
        category_links = soup.find_all('a', class_='offer_list_category_link')

        for link in category_links:
            badge = link.find('span', class_=lambda x: x and 'MuiBadge-badge' in x)
            if badge:
                count_text = badge.get_text(strip=True)
                numbers = re.findall(r'\d+', count_text)
                if numbers:
                    count = int(numbers[0])

                    tech_span = link.find('div', class_=lambda x: x and 'mui-d11uud' in x)
                    if tech_span:
                        tech_name_elem = tech_span.find('span')
                        tech_name = tech_name_elem.get_text(strip=True) if tech_name_elem else 'Unknown'
                    else:
                        href = link.get('href', '').split('/')[-1]
                        tech_name = href.replace('-', ' ').lower()

                    tech_name = tech_name.capitalize()
                    if count > 0 and tech_name:
                        tech_counts[tech_name] = count

        return tech_counts
    except Exception as e:
        print(f"❌ Scrape error: {e}")
        return {}


def save_to_db(tech_data):
    """Save scraped data to MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        company_name = "JustJoinIt"
        now = datetime.now()

        insert_query = """
        INSERT INTO justjoinit_jobs (dateTime, CompanyName, technologyName, techCounts)
        VALUES (%s, %s, %s, %s)
        """

        for tech_name, count in tech_data.items():
            data = (now, company_name, tech_name, count)
            cursor.execute(insert_query, data)

        connection.commit()
        print(f"✅ Saved {len(tech_data)} technologies to DB")
        return True

    except Error as e:
        print(f"❌ DB Insert Error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

