"""
init_db.py

This script initializes the SQLite database by creating the necessary tables (leads and past_projects)
and inserting dummy data for testing purposes.

Usage:
    python init_db.py
"""

from sqlalchemy import create_engine, text

# Database connection string (using SQLite)
DATABASE_URL = "sqlite:///agrim_ai_agent.db"

engine = create_engine(DATABASE_URL, echo=True)

with engine.begin() as conn:
    # Create leads table if it doesn't exist
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT,
            requirements TEXT,
            status TEXT DEFAULT 'new'
        )
    """))
    
    # Create past_projects table if it doesn't exist
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS past_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            details TEXT,
            results TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    # Insert dummy data into leads table with JSON requirements
    conn.execute(text("""
        INSERT INTO leads (name, company, email, requirements, status)
        VALUES 
            ('John Doe', 'Acme Corp', 'john.doe@example.com', 
             '{"objective": "Customer Engagement", "industry": "Technology", "description": "Need an AI chatbot for customer support"}', 
             'new'),
            ('Jane Smith', 'Tech Inc', 'jane.smith@techinc.com',
             '{"objective": "Process Automation", "industry": "Manufacturing", "description": "Looking for ML solution for quality control"}',
             'new')
    """))
    
    # Insert dummy data into past_projects table
    conn.execute(text("""
        INSERT INTO past_projects (project_name, details, results)
        VALUES ('ChatBot', 'Implemented a conversational AI solution.', 'Increased customer engagement')
    """))

print("Database initialized with dummy data.")
