# routes/assignment_management.py
from flask import Blueprint, jsonify
from datetime import datetime
import requests
from config import CANVAS_API_TOKEN, CANVAS_BASE_URL

assignment_management_bp = Blueprint('assignment_management', __name__)

# Fetch assignments for a specific course
def fetch_course_assignments(course_id):
    url = f"{CANVAS_BASE_URL}/api/v1/courses/{course_id}/assignments"
    headers = {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}"
    }
    assignments = []

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            assignments.extend(response.json())  # Add assignments from the current page

            # Get the "Link" header for pagination
            link_header = response.headers.get('Link')
            url = None  # Reset URL; we'll set it to the "next" link if available
            count = 1

            if link_header:
                # Parse the Link header to find the "next" page URL
                links = link_header.split(",")
                for link in links:
                    parts = link.split("; ")
                    if len(parts) == 2 and parts[1] == 'rel="next"':
                        url = parts[0][1:-1]  # Extract URL without angle brackets

        else:
            print(f"Error fetching assignments: {response.status_code}")
            url = None  # Exit if there's an error

    return assignments

# Fetch all assignments from all courses
@assignment_management_bp.route('/show-assignments', methods=['GET'])
def fetch_all_assignments():
    from routes.course_management import fetch_canvas_courses

    courses = fetch_canvas_courses().get_json()
    tasks = []
    now = datetime.utcnow()
    print("Now", now)

    for course in courses:
        course_name = course['name']
        course_id = course['id']

        assignments = fetch_course_assignments(course_id)

        for assignment in assignments:
            due_date_str = assignment.get('due_at')
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%SZ")
                print(f"{assignment.get('name')}, {due_date_str}")

                if due_date > now:
                    tasks.append({
                        'title': assignment['name'],
                        'due_date': due_date_str,
                        'course_name': course_name
                    })

    return jsonify(tasks)