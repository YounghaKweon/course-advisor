Course Advisor Bot 2.0

A conversational AI bot that helps students find university courses using the Gemini API.

Project Files

course_tools.py: The functions for searching course data.

course_advisor_agent.py: The main script to run the bot.

test_course_tools.py: Automated tests for the search functions.

Sections.json: The course catalog data.

.env: Your secret API key configuration file.

conversations_gemini.jsonl: A log file of your chats with the bot.

Quick Start Guide

1. Set Up the Environment

First, create and activate a Python virtual environment in your project folder.

# Create the environment
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate


2. Install Libraries

With your environment active, install the required packages.

pip install pandas google-generativeai python-dotenv pytest


3. Add Your API Key

Create a file named .env in the project folder and add your Google Gemini API key to it like this:

GOOGLE_API_KEY="your-api-key-here"


4. Run the Bot

To start chatting with the Course Advisor Bot, run this command:

python course_advisor_agent.py


5. Run Tests

To verify that the search functions are working correctly, run the automated test suite:

pytest -v
