from celery import Celery
from celery.schedules import crontab
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from database import SessionLocal
import models

# Initialize Celery
celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'), backend=os.getenv('CELERY_RESULT_BACKEND'))

# Configure Celery Beat schedule
celery.conf.beat_schedule = {
    'fetch-news-daily': {
        'task': 'tasks.fetch_news',
        'schedule': crontab(hour=0, minute=0),  # Run at midnight every day
    },
}

@celery.task
def fetch_news():
    """Fetch news from a website and save to database"""
    try:
        # Example: Fetch news from a website
        response = requests.get('https://news.ycombinator.com/')
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the news items
        news_items = soup.find_all('tr', class_='athing')
        
        db = SessionLocal()
        try:
            for item in news_items[:10]:  # Get top 10 news
                title = item.find('span', class_='titleline').find('a').text
                link = item.find('span', class_='titleline').find('a')['href']
                
                # Create news item in database
                news_item = models.NewsItem(
                    title=title,
                    link=link,
                    fetched_at=datetime.utcnow()
                )
                db.add(news_item)
            
            db.commit()
        finally:
            db.close()
            
        return f"Successfully fetched {len(news_items)} news items"
    except Exception as e:
        return f"Error fetching news: {str(e)}" 