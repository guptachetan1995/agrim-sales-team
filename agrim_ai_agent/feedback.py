"""
feedback.py

This module processes human feedback in natural language and refines email drafts accordingly.
It leverages the Groq LLM API via the llm module to update the draft email based on feedback.

Functions:
    process_feedback(current_draft: str, feedback: str) -> str
        Processes the human feedback and returns the updated email draft.

Usage Examples:
    >>> from agrim_ai_agent import feedback
    >>> updated_draft = feedback.process_feedback("Initial draft...", "Make the language more formal")
"""

import logging
from agrim_ai_agent import llm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def process_feedback(current_draft: str, feedback: str) -> str:
    """
    Processes human feedback to refine an email draft using the Groq LLM API.

    Args:
        current_draft (str): The current version of the email draft.
        feedback (str): Natural language feedback provided by a human reviewer.

    Returns:
        str: The updated email draft after applying the feedback.

    Raises:
        Exception: Propagates exceptions from the llm.update_draft_email call if the API request fails.

    Example:
        >>> updated_draft = process_feedback("Hello, we offer...", "Add a friendly tone")
    """
    try:
        updated_draft = llm.update_draft_email(current_draft, feedback)
        logger.info("Email draft updated with provided feedback.")
        return updated_draft
    except Exception as e:
        logger.error("Failed to update email draft: %s", e)
        raise
