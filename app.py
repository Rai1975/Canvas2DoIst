from flask import Flask
import config  # Load environment variables
from routes.course_management import course_management_bp
from routes.assignment_management import assignment_management_bp
from routes.todoist_management import todoist_management_bp
from routes.home import home_bp


app = Flask(__name__)

# Register routes
app.register_blueprint(course_management_bp)
app.register_blueprint(assignment_management_bp)
app.register_blueprint(todoist_management_bp)
app.register_blueprint(home_bp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
