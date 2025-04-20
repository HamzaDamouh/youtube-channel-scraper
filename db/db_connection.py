import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )


def insert_channels(cursor, channels):
    """Bulk insert channels and return mapping channel_name→id"""
    query = "INSERT INTO channels (channel_name) VALUES %s ON CONFLICT (channel_name) DO NOTHING"
    values = [(ch,) for ch in channels]
    execute_values(cursor, query, values)
    cursor.execute("SELECT id, channel_name FROM channels WHERE channel_name = ANY(%s)", (channels,))
    return {name: cid for cid, name in cursor.fetchall()}


def insert_videos(videos):
    """Insert videos with channel lookup"""
    conn = get_connection()
    cur = conn.cursor()

    # Ensure channels exist
    channel_names = list({v['channel_name'] for v in videos})
    channel_map = insert_channels(cur, channel_names)

    # Prepare video rows
    rows = []
    for v in videos:
        rows.append(
            (channel_map[v['channel_name']], v['title'], v['duration'], v['url'], v['published_date'], v['description'])
        )

    sql = (
        "INSERT INTO videos (channel_id, title, duration, url, published_date, description) "
        "VALUES %s ON CONFLICT (url) DO NOTHING"
    )
    execute_values(cur, sql, rows)
    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted/updated {len(rows)} videos")