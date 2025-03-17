# Agrim AI Agentic Sales Team

This project implements an agentic sales team for Agrim AI. The agent processes new leads, leverages past AI project data, and uses the Groq LLM API to generate custom email drafts enhanced by historical project success. A human-in-loop feedback mechanism refines the draft until approval, and the final email is sent to the client.

## Architecture

- **agrim_ai_agent/**: Core modules
  - **database.py**: Interacts with the leads and past projects database.
  - **llm.py**: Integrates with the Groq LLM API to generate and refine email drafts.
  - **feedback.py**: Processes human feedback to update draft emails.
  - **mailer.py**: Sends emails to clients.
  - **workflow.py**: Coordinates the overall workflow.
- **tests/**: Contains unit tests for the agentic workflow.
- **README.md**: Project overview and documentation.
- **requirements.txt**: Project dependencies.

## Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Configure database connection and Groq LLM API credentials in environment variables or configuration file as needed.

## Usage

Run the main workflow:

```
python -m agrim_ai_agent.workflow
```

During execution, the system will:
1. Read new leads and past projects.
2. Draft a custom email using the Groq LLM API.
3. Enter a human-in-loop phase to refine the draft.
4. Send the final approved email to the client.

## Testing

Unit tests reside in the `tests/` directory. Run them via:

```
python -m unittest discover -s tests
