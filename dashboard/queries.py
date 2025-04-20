import psycopg2
import pandas as pd
from db.db_connection import get_connection

def load_all_data():
    conn=get_connection()
    query="""
    SELECT c.channel_name, v.*
    FROM videos v
    JOIN channels c ON v.channel_id=c.id
    ORDER BY v.published_date DESC
    """
    df=pd.read_sql(query, conn)
    conn.close()
    return df