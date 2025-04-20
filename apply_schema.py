#!/usr/bin/env python
import os
from dotenv import load_dotenv
from db.db_connection import get_connection

def main():
    # Load DB_* vars from .env
    load_dotenv()

    # Read the raw SQL
    with open('db/schema.sql', 'r', encoding='utf-8') as f:
        raw_sql = f.read()

    # Split into individual statements on semicolons
    statements = [stmt.strip() for stmt in raw_sql.split(';') if stmt.strip()]

    conn = get_connection()
    with conn.cursor() as cur:
        for stmt in statements:
            cur.execute(stmt)    # execute each CREATE TABLE separately
    conn.commit()
    conn.close()

    print("✅ Database schema applied successfully.")

if __name__ == "__main__":
    main()
