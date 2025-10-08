# Vector DB Project

A vector database project for storing and querying podcast transcripts with semantic search capabilities using TimescaleDB and pgvector.

## Overview

This project creates a vector database containing podcast transcripts from the Lex Fridman Podcast dataset. It supports semantic search using 128-dimensional embeddings to find similar content across podcast segments and episodes.

## Database Schema

- **podcast**: Stores unique podcast episodes with ID and title
- **segment**: Stores individual podcast segments with timestamps, transcripts, and vector embeddings

## Files

- `db_build.py` - Creates database tables and enables vector extension
- `db_insert.py` - Populates database with podcast data from JSONL files
- `db_query.py` - Performs vector similarity queries and analysis
- `utils.py` - Helper functions for fast database insertion
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Set your `DATABASE_URL` connection string

3. Create database tables:
   ```bash
   python db_build.py
   ```

4. Insert data:
   ```bash
   python db_insert.py
   ```

## Usage

Run vector similarity queries:
```bash
python db_query.py
```

This will execute various similarity searches including:
- Finding similar segments to specific segments
- Finding dissimilar segments 
- Finding similar podcast episodes using embedding averaging
- Cross-episode similarity analysis

## Features

- **Vector Similarity Search**: Uses L2 distance for semantic similarity
- **Fast Bulk Insertion**: Optimized data loading using PostgreSQL COPY
- **Semantic Clustering**: Groups related content across different episodes
- **Flexible Querying**: Supports segment-level and episode-level similarity

## Requirements

- Python 3.8+
- TimescaleDB with pgvector extension
- Required Python packages (see requirements.txt)