## This script is used to create the tables in the database

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

CONNECTION = "postgres://tsdbadmin:bnk1i1unmn9k0xg7@kl48wuew8y.en3bm5at9b.tsdb.cloud.timescale.com:34003/tsdb?sslmode=require"

# need to run this to enable vector data type
CREATE_EXTENSION = "CREATE EXTENSION vector"

# Create podcast table
CREATE_PODCAST_TABLE = """
CREATE TABLE IF NOT EXISTS podcast (
    id VARCHAR(255) PRIMARY KEY,
    title TEXT NOT NULL
);
"""

# Create segment table with vector embedding
CREATE_SEGMENT_TABLE = """
CREATE TABLE IF NOT EXISTS segment (
    id VARCHAR(255) PRIMARY KEY,
    start_time FLOAT,
    end_time FLOAT,
    content TEXT NOT NULL,
    embedding VECTOR(128),
    podcast_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (podcast_id) REFERENCES podcast(id)
);
"""

conn = psycopg2.connect(CONNECTION)

try:
    cursor = conn.cursor()
    
    # Enable vector extension
    print("Creating vector extension...")
    cursor.execute(CREATE_EXTENSION)
    
    # Create podcast table
    print("Creating podcast table...")
    cursor.execute(CREATE_PODCAST_TABLE)
    
    # Create segment table
    print("Creating segment table...")
    cursor.execute(CREATE_SEGMENT_TABLE)
    
    # Commit the changes
    conn.commit()
    print("Tables created successfully!")
    
except Exception as e:
    print(f"Error creating tables: {e}")
    conn.rollback()
    
finally:
    cursor.close()
    conn.close()


