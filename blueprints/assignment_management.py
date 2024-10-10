# blueprints/assignment_management.py
from flask import Blueprint, jsonify
from datetime import datetime

assignment_management_bp = Blueprint('assignment_management', __name__)

# Fetch assignments for a specific course
def fetch_course_assignments(course_id):
    from main import CANVAS_API_TOKEN, CANVAS_BASE_URL
    import requests

    url = f"{CANVAS_BASE_URL}/api/v1/courses/{course_id}/assignments"
    headers = {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        assignments = response.json()
        return assignments
    else:
        return []

# Fetch all assignments from all courses
@assignment_management_bp.route('/show-assignments', methods=['GET'])
def fetch_all_assignments():
    from blueprints.course_management import fetch_canvas_courses

    courses = fetch_canvas_courses().get_json()
    tasks = []
    now = datetime.utcnow()

    for course in courses:
        course_name = course['name']
        course_id = course['id']

        assignments = fetch_course_assignments(course_id)

        for assignment in assignments:
            due_date_str = assignment.get('due_at')
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%SZ")

                if due_date > now:
                    tasks.append({
                        'title': assignment['name'],
                        'due_date': due_date_str,
                        'course_name': course_name
                    })

    return jsonify(tasks)