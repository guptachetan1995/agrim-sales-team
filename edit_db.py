"""
edit_db.py

This script provides functions to add or update multiple entries in the leads and past_projects tables.

Usage:
    python edit_db.py
"""

from sqlalchemy import create_engine, text

# Database connection string (using SQLite)
DATABASE_URL = "sqlite:///agrim_ai_agent.db"

engine = create_engine(DATABASE_URL, echo=True)

def add_or_update_leads(entries):
    """
    Add or update multiple entries in the leads table.

    Args:
        entries (list of dict): List of dictionaries containing lead data.
    """
    with engine.begin() as conn:
        for entry in entries:
            conn.execute(text("""
                INSERT INTO leads (id, name, company, email, requirements, status)
                VALUES (:id, :name, :company, :email, :requirements, :status)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    company = excluded.company,
                    email = excluded.email,
                    requirements = excluded.requirements,
                    status = excluded.status
            """), entry)

def add_or_update_past_projects(entries):
    """
    Add or update multiple entries in the past_projects table.

    Args:
        entries (list of dict): List of dictionaries containing past project data.
    """
    with engine.begin() as conn:
        for entry in entries:
            conn.execute(text("""
                INSERT INTO past_projects (id, project_name, details, results, created_at)
                VALUES (:id, :project_name, :details, :results, :created_at)
                ON CONFLICT(id) DO UPDATE SET
                    project_name = excluded.project_name,
                    details = excluded.details,
                    results = excluded.results,
                    created_at = excluded.created_at
            """), entry)

if __name__ == "__main__":
    # Example usage
    leads_entries = [
        {'id': 1, 'name': 'John Doe', 'company': 'Acme Corp', 'email': 'john.doe@example.com', 'requirements': 'Need an AI solution', 'status': 'new'},
        {'id': 2, 'name': 'Jane Smith', 'company': 'Beta Inc', 'email': 'jane.smith@example.com', 'requirements': 'Looking for data analysis', 'status': 'in progress'}
    ]

    past_projects_entries = [
        {'id': 1, 'project_name': 'ChatBot', 'details': 'Implemented a conversational AI solution.', 'results': 'Increased customer engagement', 'created_at': '2025-03-07 18:09:32'},
        {'id': 2, 'project_name': 'Data Analysis', 'details': 'Performed extensive data analysis.', 'results': 'Improved decision making', 'created_at': '2025-03-07 18:09:32'}
    ]

    add_or_update_leads(leads_entries)
    add_or_update_past_projects(past_projects_entries)

    print("Entries added or updated successfully.")
