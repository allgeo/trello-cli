# Trello CLI
A command line interface (CLI) to easily interact with a Trello board via the Trello API.

## Prerequisites
- Python 3.9 or above
- Trello API key and token (refer to `.env.example`)

## Assumptions
- The Trello board and lists already exist

## Development Setup
1. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Trello API key and token in the `.env` file
4. Run the CLI to test all Trello API calls:
   ```
   python src/cli.py
   ```
5. Run unit tests:
   ```
   pytest tests/test_api.py
   ```

## Usage Instructions
1. Ensure you have completed the Development Setup steps above
2. Activate the virtual environment if not already active:
   ```
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Run the CLI:
   ```
   python src/cli.py
   ```
4. Follow the CLI prompts to create a Trello card

## Improvements for Future
- Implement ability to create Trello boards and lists if they don't exist
- Add support for advanced fields such as due dates and markdown formatting
- Set up GitHub CI/CD pipeline
- Implement code quality tools (Tox, flake8)
- Gracefully handle errors and edge cases
