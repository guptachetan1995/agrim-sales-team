"""
llm.py

This module integrates with the Groq LLM API to generate and update custom email drafts.
It leverages the Groq client for producing responses based on prompts generated from new lead data and historical projects.
It also supports processing human feedback to refine the email draft.

The module implements a GroqLLM class that uses the Groq client for LLM operations. The module exposes two functions:
    generate_draft_email(new_lead: dict, past_projects: list) -> str
        Generates an initial email draft using new lead details and past project information.
    update_draft_email(current_draft: str, feedback: str) -> str
        Updates the email draft based on human feedback.

Usage Examples:
    >>> from agrim_ai_agent import llm
    >>> draft = llm.generate_draft_email(new_lead, past_projects)
    >>> updated_draft = llm.update_draft_email(draft, feedback)
"""

from dotenv import load_dotenv
load_dotenv()
from groq import Groq
from time import sleep
from typing import List, Dict

# Dummy TTS implementation to simulate text-to-speech functionality.
class DummyTTS:
    def __init__(self, use_tts: bool = True):
        self.use_tts = use_tts
        self.queue = []
    def enqueue_text(self, text: str) -> None:
        self.queue.append(text)
    def process_text(self) -> None:
        # In a real implementation, process the text (e.g., convert to speech)
        self.queue = []

class GroqLLM:
    def __init__(self, use_tts: bool = True):
        """
        Initializes the GroqLLM client.

        Args:
            use_tts (bool): Flag to enable text-to-speech output.
        """
        self.client = Groq()
        self.tts = DummyTTS(use_tts=use_tts)
        self.messages: List[Dict[str, str]] = []

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response using the Groq LLM API based on the provided prompt.
        Streams the response, enqueues text for TTS processing, and returns the full response.

        Args:
            prompt (str): The prompt text to generate a response for.

        Returns:
            str: The full generated response.
        """
        # Append the user prompt to the message sequence.
        self.messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=2048,
            messages=self.messages,
            stream=True
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                self.tts.enqueue_text(content)
        self.messages.append({"role": "assistant", "content": full_response})
        self.tts.process_text()
        return full_response

def generate_draft_email(new_lead: dict, past_projects: list) -> str:
    """
    Generates a custom email draft for a new lead using historical project data via GroqLLM.

    Args:
        new_lead (dict): Information about the new lead (e.g., name, company, requirements).
        past_projects (list of dict): List of past AI project records, each with project details.

    Returns:
        str: The generated email draft.

    Example:
        >>> draft = generate_draft_email(
        ...     {"name": "John Doe", "company": "Acme Corp", "requirements": "Need AI solution"},
        ...     [{"project_name": "ChatBot", "details": "Implemented a conversational AI."}]
        ... )
    """
    prompt = f"Generate a custom email draft for a new lead.\n"
    prompt += f"Lead Details: Name: {new_lead.get('name', '')}, Company: {new_lead.get('company', '')}, Requirements: {new_lead.get('requirements', '')}.\n"
    prompt += "Include references to past successful AI projects: "
    for project in past_projects:
        prompt += f"{project.get('project_name', 'Unnamed Project')} - {project.get('details', '')}; "
    prompt += "\nExplain why our services are best suited to help the client."
    
    llm_client = GroqLLM(use_tts=False)
    return llm_client.generate_response(prompt)

def update_draft_email(current_draft: str, feedback: str) -> str:
    """
    Updates an existing email draft based on human feedback using GroqLLM.

    Args:
        current_draft (str): The current email draft content.
        feedback (str): Natural language feedback to refine the draft.

    Returns:
        str: The updated email draft.

    Example:
        >>> updated_draft = update_draft_email("Initial draft...", "Make the tone more friendly")
    """
    prompt = f"Current email draft: {current_draft}\n"
    prompt += f"Update the email draft with the following feedback: {feedback}"
    
    llm_client = GroqLLM(use_tts=False)
    return llm_client.generate_response(prompt)
