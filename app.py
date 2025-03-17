"""
Flask application to serve as backend API for the Agrim AI Agentic Sales UI.
Integrates with existing workflow and database functionality.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from agrim_ai_agent.database import get_new_leads
from agrim_ai_agent.workflow import compose_engaging_email, process_lead
from agrim_ai_agent.llm import update_draft_email
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/leads', methods=['GET'])
def get_leads():
    """Fetch all new leads from the database."""
    try:
        leads = get_new_leads()
        return jsonify(leads)
    except Exception as e:
        logger.error(f"Error fetching leads: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/draft-email', methods=['POST'])
def create_draft():
    """Generate an email draft for a specific lead."""
    try:
        lead_data = request.json
        logger.info(f"Received lead data: {lead_data}")
        
        if not lead_data:
            return jsonify({"error": "No lead data provided"}), 400
            
        if not all(k in lead_data for k in ['name', 'email']):
            return jsonify({"error": "Missing required lead information (name or email)"}), 400

        subject, body = compose_engaging_email(
            lead_name=lead_data.get('name'),
            lead_email=lead_data.get('email'),
            lead_requirements=lead_data.get('requirements', {})
        )
        
        if not subject or not body:
            return jsonify({"error": "Failed to generate subject or body"}), 500
            
        logger.info(f"Generated draft for {lead_data.get('email')}")
        return jsonify({
            "subject": subject,
            "body": body
        })
    except Exception as e:
        logger.error(f"Error generating draft: {str(e)}", exc_info=True)
        return jsonify({"error": f"Failed to generate draft: {str(e)}"}), 500

@app.route('/api/update-draft', methods=['POST'])
def update_draft_route():
    """Update email draft based on feedback."""
    try:
        data = request.json
        current_draft = f"{data.get('subject')}\n{data.get('body')}"
        feedback = data.get('feedback')
        
        if not current_draft or not feedback:
            return jsonify({"error": "Missing draft or feedback"}), 400
            
        updated_draft = update_draft_email(current_draft, feedback)
        
        # Split updated draft into subject and body
        lines = updated_draft.split("\n", 1)
        if len(lines) == 2:
            subject = lines[0].strip()
            body = lines[1].strip()
        else:
            subject = "Updated Email Draft"
            body = updated_draft.strip()
            
        return jsonify({
            "subject": subject,
            "body": body
        })
    except Exception as e:
        logger.error(f"Error updating draft: {str(e)}", exc_info=True)
        return jsonify({"error": f"Failed to update draft: {str(e)}"}), 500

@app.route('/api/send-email', methods=['POST'])
def send_email_route():
    """Process and send the final email."""
    try:
        data = request.json
        if not data.get('approved', False):
            return jsonify({"error": "Email must be approved before sending"}), 400
            
        lead_info = {
            'name': data.get('name'),
            'email': data.get('email'),
            'requirements': data.get('requirements', {}),
            'subject': data.get('subject'),
            'body': data.get('body')
        }
        process_lead(lead_info)
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
