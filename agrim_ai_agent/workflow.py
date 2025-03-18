"""
Workflow Module for Customized Email Communication

This module defines the workflow for composing and sending engaging and well-structured
emails to leads. The emails are customized using LLM-generated drafts based on the lead's
requirements and enriched with data from past projects that match those requirements.

Modules:
    - compose_engaging_email: Compose personalized email content using LLM-based generation.
    - process_lead: Orchestrate the email communication workflow for a given lead.

Usage Example:
    >>> sample_lead = {
    ...     'name': 'John',
    ...     'email': 'john@example.com',
    ...     'requirements': {
    ...         'objective': 'Customer Engagement',
    ...         'industry': 'Retail'
    ...     }
    ... }
    >>> process_lead(sample_lead)
"""

import datetime
import logging
from agrim_ai_agent.project_matcher import match_projects
from agrim_ai_agent.mailer import send_email
from agrim_ai_agent.llm import generate_draft_email, update_draft_email

def compose_engaging_email(lead_name: str, lead_email: str, lead_requirements: dict) -> tuple:
    """
    Compose a customized email draft for the given lead using LLM-based generation.
    Combines new lead details with past project data to produce a well-structured and engaging email draft.

    Args:
        lead_name (str): The name of the lead.
        lead_email (str): The email address of the lead.
        lead_requirements (dict): A dictionary containing the lead's requirements,
            e.g., {'objective': 'Customer Engagement', 'industry': 'Retail'}.

    Returns:
        tuple: A tuple containing the email subject (str) and the email body (str).

    The generated draft is expected to begin with a subject line followed by the body.
    If parsing fails, a default subject is applied.
    """
    projects = match_projects(lead_requirements)
    
    # Prepare lead details for LLM generation; default company if not provided.
    new_lead = {
        "name": lead_name,
        "company": lead_requirements.get("company", "Valued Client"),
        "requirements": lead_requirements
    }
    
    # Generate draft email using LLM
    draft = generate_draft_email(new_lead, projects)
    
    # Expecting the draft to have a subject on the first line and the body afterwards.
    lines = draft.split("\n", 1)
    if len(lines) == 2:
        subject = lines[0].strip()
        body = lines[1].strip()
    else:
        subject = "Your Customized AI Solutions"
        body = draft.strip()
    return subject, body

def get_human_feedback(subject: str, body: str) -> bool:
    """
    Display the draft email and prompt for human approval.

    Args:
        subject (str): The email subject.
        body (str): The email body.

    Returns:
        bool: True if the human approves sending the email, False otherwise.
    """
    print("---- Draft Email ----")
    print(f"Subject: {subject}\n")
    print(f"Body:\n{body}")
    print("---------------------")
    feedback = input("Do you approve sending this email? (y/n): ")
    return feedback.strip().lower() == 'y'

def process_lead(lead_info: dict) -> None:
    """
    Process the lead information and send the approved email.

    Args:
        lead_info (dict): A dictionary containing lead information with keys:
            - name: Lead's name
            - email: Lead's email address
            - requirements: Lead requirements dict
            - subject: Email subject
            - body: Email body

    Returns:
        None
    """
    try:
        if not all(k in lead_info for k in ['email', 'subject', 'body']):
            raise ValueError("Missing required email information (email, subject, or body)")
            
        send_email(
            to=lead_info['email'],
            subject=lead_info['subject'],
            body=lead_info['body']
        )
        logging.info(f"Email sent to {lead_info['email']}")
    except Exception as e:
        logging.error(f"Failed to send email to {lead_info.get('email', 'unknown')}: {str(e)}")
        raise

def process_lead_by_id(lead_id: int) -> None:
    """
    Process a lead by retrieving its information from the leads table in the database
    and executing the email workflow.

    Args:
        lead_id (int): The unique identifier of the lead in the database.

    Returns:
        None
    """
    from agrim_ai_agent.database import fetch_lead_by_id  # assuming a function to fetch a lead exists
    lead_info = fetch_lead_by_id(lead_id)
    if lead_info:
        process_lead(lead_info)
    else:
        logging.error(f"Lead with id {lead_id} not found.")
        print(f"Lead with id {lead_id} not found.")

# Sample usage for testing the workflow module.
if __name__ == '__main__':
    sample_lead = {
        'name': 'John',
        'email': 'john@example.com',
        'requirements': {
            'objective': 'Customer Engagement',
            'industry': 'Retail'
        }
    }
    process_lead(sample_lead)
