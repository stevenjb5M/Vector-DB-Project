## This script is used to insert data into the database
import os
import json
import glob
from dotenv import load_dotenv
from datasets import load_dataset
import pandas as pd

from utils import fast_pg_insert

load_dotenv()

CONNECTION = os.getenv("DATABASE_URL")

def load_batch_request_data():
    """Load all batch request data from JSONL files"""
    documents_path = "/Users/stevenbrown/Downloads/documents/"
    all_segments = []
    
    print("Loading batch request files...")
    batch_files = glob.glob(os.path.join(documents_path, "batch_request_*.jsonl"))
    
    for file_path in batch_files:
        print(f"Processing {os.path.basename(file_path)}...")
        with open(file_path, 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                segment_info = {
                    'custom_id': data['custom_id'],
                    'content': data['body']['input'],
                    'title': data['body']['metadata']['title'],
                    'podcast_id': data['body']['metadata']['podcast_id'],
                    'start_time': data['body']['metadata']['start_time'],
                    'stop_time': data['body']['metadata']['stop_time']
                }
                all_segments.append(segment_info)
    
    return pd.DataFrame(all_segments)

def load_embedding_data():
    """Load all embedding data from JSONL files"""
    embeddings_path = "/Users/stevenbrown/Downloads/embedding/"
    all_embeddings = []
    
    print("Loading embedding files...")
    embedding_files = glob.glob(os.path.join(embeddings_path, "*.jsonl"))
    
    for file_path in embedding_files:
        print(f"Processing {os.path.basename(file_path)}...")
        with open(file_path, 'r') as f:
            for line in f:
                data = json.loads(line.strip())
                if data.get('response') and data['response'].get('body'):
                    embedding_info = {
                        'custom_id': data['custom_id'],
                        'embedding': data['response']['body']['data'][0]['embedding']
                    }
                    all_embeddings.append(embedding_info)
    
    return pd.DataFrame(all_embeddings)

def create_podcast_dataframe(segments_df):
    """Create unique podcast entries from segments data"""
    print("Creating podcast dataframe...")
    podcasts = segments_df[['podcast_id', 'title']].drop_duplicates()
    podcasts = podcasts.rename(columns={'podcast_id': 'id'})
    return podcasts

def create_segment_dataframe(segments_df, embeddings_df):
    """Merge segment data with embeddings and prepare for database insertion"""
    print("Creating segment dataframe...")
    
    merged_df = segments_df.merge(embeddings_df, on='custom_id', how='inner')
    
    segment_df = pd.DataFrame({
        'id': merged_df['custom_id'],
        'start_time': merged_df['start_time'],
        'end_time': merged_df['stop_time'],
        'content': merged_df['content'],
        'embedding': merged_df['embedding'].apply(lambda x: '[' + ','.join(map(str, x)) + ']'),  # Format as PostgreSQL array
        'podcast_id': merged_df['podcast_id']
    })
    
    return segment_df

def main():
    print("Starting data insertion process...")
    
    segments_df = load_batch_request_data()
    embeddings_df = load_embedding_data()
    
    print(f"Loaded {len(segments_df)} segments and {len(embeddings_df)} embeddings")
    
    podcasts_df = create_podcast_dataframe(segments_df)
    print(f"Found {len(podcasts_df)} unique podcasts")
    
    segments_final_df = create_segment_dataframe(segments_df, embeddings_df)
    print(f"Created {len(segments_final_df)} segment records for insertion")
    
    print("Inserting podcasts into database...")
    fast_pg_insert(
        df=podcasts_df,
        connection=CONNECTION,
        table_name='podcast',
        columns=['id', 'title']
    )
    print(f"Inserted {len(podcasts_df)} podcasts")
    
    print("Inserting segments into database...")
    fast_pg_insert(
        df=segments_final_df,
        connection=CONNECTION,
        table_name='segment',
        columns=['id', 'start_time', 'end_time', 'content', 'embedding', 'podcast_id']
    )
    print(f"Inserted {len(segments_final_df)} segments")
    
    print("Data insertion completed successfully!")

if __name__ == "__main__":
    main()