import os
import psycopg2 # type: ignore
from psycopg2.extras import execute_values # type: ignore


def get_connection():
    """_summary_
    """
    conn = psycopg2.connect(
        host = os.getenv('DB_HOST','localhost'),
        port = os.getenv('DB_PORT','5432'),
        database = os.getenv('DB_NAME','youtube_analyzer'),
        user = os.getenv('DB_USER', 'postgres'),
        password = os.getenv('DB_PASSWORD', 'postgres')
    )
    return conn

def insert_videos(videos):
    """_summary_

    Args:
        videos (_type_): _description_
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO videos (title, duration, url, published_date, description) VALUES %s"
    
    values = [
        (
            video.get('title'),
            video.get('duration'),
            video.get('url'),
            video.get('published_date'),
            video.get('description')
        )
        for video in videos
    ]
    
    execute_values(cursor, query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Inserted {len(videos)} records in DB")
    
    
    
