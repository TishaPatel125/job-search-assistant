import sqlite3
import json
import os
import logging
from src.schemas import JobPosting

logger = logging.getLogger(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'jobs.db')

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Job Postings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_postings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT NOT NULL,
        company_name TEXT NOT NULL,
        location TEXT,
        remote_status TEXT,
        experience_level TEXT,
        salary_range TEXT,
        full_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

def insert_job(posting: JobPosting):
    """Insert a JobPosting into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO job_postings 
    (job_title, company_name, location, remote_status, experience_level, salary_range, full_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        posting.job_title,
        posting.company_name,
        posting.location,
        posting.remote_status,
        posting.experience_level,
        posting.salary_range,
        posting.model_dump_json()
    ))
    
    conn.commit()
    conn.close()
    logger.info(f"Inserted job posting '{posting.job_title}' into database.")

def get_all_jobs():
    """Retrieve all job postings from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT full_json FROM job_postings ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    return [JobPosting.model_validate_json(row[0]) for row in rows]

if __name__ == "__main__":
    init_db()
