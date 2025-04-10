import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from db.db_connection import get_connection

def fetch_all_videos():
    
    conn = get_connection()
    query = "SELECT * FROM videos ORDER BY published_date DESC"
    
    df = pd.read_sql(query, conn)
    
    conn.close()
    
    return df

