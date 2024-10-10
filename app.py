from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API tokens from environment variables
CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
CANVAS_BASE_URL = os.getenv('CANVAS_BASE_URL')

# Initialize Flask application
app = Flask(__name__)

# Register Blueprints
from blueprints.course_management import course_management_bp
from blueprints.assignment_management import assignment_management_bp
from blueprints.todoist_management import todoist_management_bp

app.register_blueprint(course_management_bp)
app.register_blueprint(assignment_management_bp)
app.register_blueprint(todoist_management_bp)

if __name__ == '__main__':
    app.run(debug=True)