## This script is used to query the database
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONNECTION = os.getenv("DATABASE_URL")

def get_segment_embedding(segment_id):
    """Get the embedding vector for a specific segment"""
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT embedding FROM segment WHERE id = %s
    """, (segment_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return result[0]
    return None

def q1_most_similar_segments():
    """Q1: Find 5 most similar segments to segment "267:476" """
    print("Q1: Five most similar segments to segment '267:476'")
    print("=" * 60)
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    # Get the embedding for the target segment
    target_embedding = get_segment_embedding("267:476")
    
    if not target_embedding:
        print("Target segment not found")
        return
    
    cursor.execute("""
        SELECT 
            p.title as podcast_name,
            s.id as segment_id,
            s.content as segment_text,
            s.start_time,
            s.end_time,
            s.embedding <-> %s as distance
        FROM segment s
        JOIN podcast p ON s.podcast_id = p.id
        WHERE s.id != %s
        ORDER BY s.embedding <-> %s
        LIMIT 5
    """, (target_embedding, "267:476", target_embedding))
    
    results = cursor.fetchall()
    
    for i, (podcast_name, segment_id, segment_text, start_time, end_time, distance) in enumerate(results, 1):
        print(f"{i}. Segment ID: {segment_id}")
        print(f"   Podcast: {podcast_name}")
        print(f"   Text: {segment_text[:100]}...")
        print(f"   Time: {start_time:.2f}s - {end_time:.2f}s")
        print(f"   Distance: {distance:.6f}")
        print()
    
    cursor.close()
    conn.close()

def q2_most_dissimilar_segments():
    """Q2: Find 5 most dissimilar segments to segment "267:476" """
    print("Q2: Five most dissimilar segments to segment '267:476'")
    print("=" * 60)
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    # Get the embedding for the target segment
    target_embedding = get_segment_embedding("267:476")
    
    if not target_embedding:
        print("Target segment not found")
        return
    
    cursor.execute("""
        SELECT 
            p.title as podcast_name,
            s.id as segment_id,
            s.content as segment_text,
            s.start_time,
            s.end_time,
            s.embedding <-> %s as distance
        FROM segment s
        JOIN podcast p ON s.podcast_id = p.id
        WHERE s.id != %s
        ORDER BY s.embedding <-> %s DESC
        LIMIT 5
    """, (target_embedding, "267:476", target_embedding))
    
    results = cursor.fetchall()
    
    for i, (podcast_name, segment_id, segment_text, start_time, end_time, distance) in enumerate(results, 1):
        print(f"{i}. Segment ID: {segment_id}")
        print(f"   Podcast: {podcast_name}")
        print(f"   Text: {segment_text[:100]}...")
        print(f"   Time: {start_time:.2f}s - {end_time:.2f}s")
        print(f"   Distance: {distance:.6f}")
        print()
    
    cursor.close()
    conn.close()

def q3_similar_to_48_511():
    """Q3: Find 5 most similar segments to segment '48:511' """
    print("Q3: Five most similar segments to segment '48:511'")
    print("=" * 60)
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    # Get the embedding for the target segment
    target_embedding = get_segment_embedding("48:511")
    
    if not target_embedding:
        print("Target segment not found")
        return
    
    cursor.execute("""
        SELECT 
            p.title as podcast_name,
            s.id as segment_id,
            s.content as segment_text,
            s.start_time,
            s.end_time,
            s.embedding <-> %s as distance
        FROM segment s
        JOIN podcast p ON s.podcast_id = p.id
        WHERE s.id != %s
        ORDER BY s.embedding <-> %s
        LIMIT 5
    """, (target_embedding, "48:511", target_embedding))
    
    results = cursor.fetchall()
    
    for i, (podcast_name, segment_id, segment_text, start_time, end_time, distance) in enumerate(results, 1):
        print(f"{i}. Segment ID: {segment_id}")
        print(f"   Podcast: {podcast_name}")
        print(f"   Text: {segment_text[:100]}...")
        print(f"   Time: {start_time:.2f}s - {end_time:.2f}s")
        print(f"   Distance: {distance:.6f}")
        print()
    
    cursor.close()
    conn.close()

def q4_similar_to_51_56():
    """Q4: Find 5 most similar segments to segment '51:56' """
    print("Q4: Five most similar segments to segment '51:56'")
    print("=" * 60)
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    # Get the embedding for the target segment
    target_embedding = get_segment_embedding("51:56")
    
    if not target_embedding:
        print("Target segment not found")
        return
    
    cursor.execute("""
        SELECT 
            p.title as podcast_name,
            s.id as segment_id,
            s.content as segment_text,
            s.start_time,
            s.end_time,
            s.embedding <-> %s as distance
        FROM segment s
        JOIN podcast p ON s.podcast_id = p.id
        WHERE s.id != %s
        ORDER BY s.embedding <-> %s
        LIMIT 5
    """, (target_embedding, "51:56", target_embedding))
    
    results = cursor.fetchall()
    
    for i, (podcast_name, segment_id, segment_text, start_time, end_time, distance) in enumerate(results, 1):
        print(f"{i}. Segment ID: {segment_id}")
        print(f"   Podcast: {podcast_name}")
        print(f"   Text: {segment_text[:100]}...")
        print(f"   Time: {start_time:.2f}s - {end_time:.2f}s")
        print(f"   Distance: {distance:.6f}")
        print()
    
    cursor.close()
    conn.close()

def get_podcast_id_from_segment(segment_id):
    """Get the podcast_id for a given segment"""
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT podcast_id FROM segment WHERE id = %s
    """, (segment_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return result[0]
    return None

def q5_similar_podcasts_by_segment():
    """Q5: Find similar podcast episodes by averaging embeddings"""
    print("Q5: Most similar podcast episodes (by segment embedding averaging)")
    print("=" * 70)
    
    segments = ["267:476", "48:511", "51:56"]
    
    for segment_id in segments:
        print(f"\nQ5{chr(97 + segments.index(segment_id))}: Similar podcasts to segment '{segment_id}'")
        print("-" * 50)
        
        # Get the podcast_id for this segment to exclude it
        source_podcast_id = get_podcast_id_from_segment(segment_id)
        target_embedding = get_segment_embedding(segment_id)
        
        if not target_embedding or not source_podcast_id:
            print("Target segment or podcast not found")
            continue
        
        conn = psycopg2.connect(CONNECTION)
        cursor = conn.cursor()
        
        # Find similar podcasts by comparing against average embeddings
        cursor.execute("""
            WITH podcast_avg_embeddings AS (
                SELECT 
                    p.id as podcast_id,
                    p.title,
                    AVG(s.embedding) as avg_embedding
                FROM podcast p
                JOIN segment s ON p.id = s.podcast_id
                WHERE p.id != %s
                GROUP BY p.id, p.title
            )
            SELECT 
                title,
                avg_embedding <-> %s as distance
            FROM podcast_avg_embeddings
            ORDER BY avg_embedding <-> %s
            LIMIT 5
        """, (source_podcast_id, target_embedding, target_embedding))
        
        results = cursor.fetchall()
        
        for i, (podcast_title, distance) in enumerate(results, 1):
            print(f"{i}. {podcast_title}")
            print(f"   Distance: {distance:.6f}")
            print()
        
        cursor.close()
        conn.close()

def q6_similar_to_balaji_podcast():
    """Q6: Find similar podcasts to Balaji Srinivasan episode"""
    print("Q6: Most similar podcasts to Balaji Srinivasan episode (VeH7qKZr0WI)")
    print("=" * 70)
    
    target_podcast_id = "VeH7qKZr0WI"
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    
    # Find similar podcasts by comparing average embeddings
    cursor.execute("""
        WITH target_avg AS (
            SELECT AVG(embedding) as avg_embedding
            FROM segment 
            WHERE podcast_id = %s
        ),
        podcast_avg_embeddings AS (
            SELECT 
                p.id as podcast_id,
                p.title,
                AVG(s.embedding) as avg_embedding
            FROM podcast p
            JOIN segment s ON p.id = s.podcast_id
            WHERE p.id != %s
            GROUP BY p.id, p.title
        )
        SELECT 
            title,
            avg_embedding <-> (SELECT avg_embedding FROM target_avg) as distance
        FROM podcast_avg_embeddings
        ORDER BY avg_embedding <-> (SELECT avg_embedding FROM target_avg)
        LIMIT 5
    """, (target_podcast_id, target_podcast_id))
    
    results = cursor.fetchall()
    
    for i, (podcast_title, distance) in enumerate(results, 1):
        print(f"{i}. {podcast_title}")
        print(f"   Distance: {distance:.6f}")
        print()
    
    cursor.close()
    conn.close()

def main():
    """Run all queries"""
    try:
        print("Running Vector Database Queries")
        print("=" * 50)
        print()
        
        q1_most_similar_segments()
        print("\n" + "=" * 80 + "\n")
        
        q2_most_dissimilar_segments()
        print("\n" + "=" * 80 + "\n")
        
        q3_similar_to_48_511()
        print("\n" + "=" * 80 + "\n")
        
        q4_similar_to_51_56()
        print("\n" + "=" * 80 + "\n")
        
        q5_similar_podcasts_by_segment()
        print("\n" + "=" * 80 + "\n")
        
        q6_similar_to_balaji_podcast()
        
    except Exception as e:
        print(f"Error running queries: {e}")

if __name__ == "__main__":
    main()

