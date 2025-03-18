"""
mailer.py

This module provides email sending functionality for the Agrim AI agentic sales team.
It sends emails to clients using SMTP with configurations provided through environment variables.

Functions:
    send_email(to: str, subject: str, body: str) -> None
        Sends an email to the specified recipient.

Usage Examples:
    >>> from agrim_ai_agent import mailer
    >>> mailer.send_email("client@example.com", "Welcome", "Thank you for contacting Agrim AI!")
"""

import os
import logging
import smtplib
from email.message import EmailMessage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# SMTP configuration retrieved from environment variables.
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "your_email@example.com")
SMTP_PASS = os.environ.get("SMTP_PASS", "password")

def send_email(to: str, subject: str, body: str) -> None:
    """
    Sends an email with the specified subject and body to the given recipient.

    Args:
        to (str): Recipient email address.
        subject (str): Subject of the email.
        body (str): Body text of the email.

    Raises:
        Exception: If an error occurs during the email sending process.

    Example:
        >>> send_email("client@example.com", "Welcome to Agrim AI", "We are excited to work with you.")
    """
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            logger.info("Email sent successfully to %s.", to)
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to, e)
        raise
