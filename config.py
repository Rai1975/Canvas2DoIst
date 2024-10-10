# config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API tokens from environment variables
CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
CANVAS_BASE_URL = os.getenv('CANVAS_BASE_URL')
