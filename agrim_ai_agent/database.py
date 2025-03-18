"""
database.py

This module provides functionality for interacting with the leads and past AI projects database.

Functions:
    get_new_leads() -> list[dict]: Retrieves new leads from the database.
    get_past_projects() -> list[dict]: Retrieves past AI projects delivered by the SaaS company.

Usage Examples:
    >>> from agrim_ai_agent import database
    >>> new_leads = database.get_new_leads()
    >>> past_projects = database.get_past_projects()
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Example connection string; update with appropriate credentials as needed.
DATABASE_URL = "sqlite:///agrim_ai_agent.db"  # For production, replace with a robust database

engine = create_engine(DATABASE_URL, echo=False)

def get_new_leads() -> list:
    """
    Retrieves new leads from the leads table.

    Returns:
        list[dict]: A list of dictionaries, each representing a new lead.
        Each lead includes name, email, and parsed requirements.
    """
    query = text("SELECT * FROM leads WHERE status = 'new'")
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            leads = []
            for row in result:
                lead_dict = dict(row._mapping)
                # Parse requirements string to dictionary if it exists
                if lead_dict.get('requirements'):
                    try:
                        import json
                        lead_dict['requirements'] = json.loads(lead_dict['requirements'])
                    except json.JSONDecodeError:
                        # If not valid JSON, create a simple requirements dict
                        lead_dict['requirements'] = {
                            'description': lead_dict['requirements']
                        }
                else:
                    lead_dict['requirements'] = {}
                leads.append(lead_dict)
            logger.info("Retrieved %d new lead(s).", len(leads))
            return leads
    except SQLAlchemyError as e:
        logger.error("Error fetching new leads: %s", e)
        return []

def get_past_projects() -> list:
    """
    Retrieves past AI projects delivered by the SaaS company from the past_projects table.

    Returns:
        list[dict]: A list of dictionaries, each representing a past project.
    """
    query = text("SELECT * FROM past_projects")
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
            projects = [dict(row._mapping) for row in result]
            logger.info("Retrieved %d past project(s).", len(projects))
            return projects
    except SQLAlchemyError as e:
        logger.error("Error fetching past projects: %s", e)
        return []
