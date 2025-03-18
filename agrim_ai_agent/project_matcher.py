"""
Module for matching past projects based on lead requirements.

This module uses LLM-enhanced retrieval (RAG) to find the best matching past projects.
"""

import sqlite3
from agrim_ai_agent.llm import GroqLLM

def match_projects(lead_requirements: str):
    """
    Matches past projects based on the given lead requirements.

    Args:
        lead_requirements (str): The requirements of the lead.

    Returns:
        list: A list of matching past projects.
    """
    # Connect to the database
    conn = sqlite3.connect('agrim_ai_agent.db')
    cursor = conn.cursor()

    # Query the database for past projects
    cursor.execute("SELECT project_name as name, details as description, results as result FROM past_projects")
    past_projects = cursor.fetchall()

    # Convert the query result to a list of dictionaries
    past_projects_list = [
        {"name": row[0], "description": row[1], "result": row[2]}
        for row in past_projects
    ]

    # Use the LLM to match projects against the lead requirements
    llm_client = GroqLLM(use_tts=False)
    prompt = f"Match the following past projects to the lead requirements: {lead_requirements}\n"
    for project in past_projects_list:
        prompt += f"{project['name']}: {project['description']} (Outcome: {project['result']})\n"
    prompt += "Return the best matching projects."

    response = llm_client.generate_response(prompt)

    # Parse the response to extract matching projects
    matching_projects = []
    for project in past_projects_list:
        if project['name'] in response:
            matching_projects.append(project)

    # Close the database connection
    conn.close()

    return matching_projects
