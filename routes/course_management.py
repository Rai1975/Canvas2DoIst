# routes/course_management.py
from flask import Blueprint, jsonify
import csv
import requests
from config import CANVAS_API_TOKEN, CANVAS_BASE_URL

course_management_bp = Blueprint('course_management', __name__)
COURSE_DECISIONS_CSV = 'decisions.csv'

# Load course decisions from CSV
def load_course_decisions():
    decisions = {}
    try:
        with open(COURSE_DECISIONS_CSV, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                course_id, decision = row
                decisions[course_id] = decision
    except FileNotFoundError:
        pass  # If CSV doesn't exist, just return an empty dictionary

    return decisions

# Save course decision to CSV
def save_course_decision(course_id, decision):
    with open(COURSE_DECISIONS_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([course_id, decision])

# Fetch courses from Canvas and ask the user if they want to keep them
@course_management_bp.route('/show-all-courses', methods=['GET'])
def fetch_canvas_courses():
    import requests

    url = f"{CANVAS_BASE_URL}/api/v1/courses"
    headers = {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}"
    }

    courses = []
    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            courses.extend(response.json())
            link_header = response.headers.get('Link', None)
            if link_header:
                links = link_header.split(',')
                url = None
                for link in links:
                    if 'rel="next"' in link:
                        url = link[link.find('<')+1:link.find('>')]
                        break
            else:
                url = None
        else:
            break

    # Load course decisions from CSV
    course_decisions = load_course_decisions()
    active_courses = []

    # Loop through the courses and ask if the user wants to keep each one
    for course in courses:
        course_id = str(course['id'])
        course_name = course.get('name')

        if not course_name:
            continue

        if course_id in course_decisions:
            decision = course_decisions[course_id]
        else:
            print(f"Do you want to keep the course '{course_name}'? (yes/no)")
            decision = input().strip().lower()
            save_course_decision(course_id, decision)

        if decision == 'yes':
            active_courses.append(course)

    return jsonify(active_courses)
