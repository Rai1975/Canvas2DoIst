from flask import Flask, jsonify
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API tokens from environment variables
CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
CANVAS_BASE_URL = os.getenv('CANVAS_BASE_URL')

app = Flask(__name__)

# Fetch courses from Canvas
@app.route('/show-all-courses', methods=['GET'])
def fetch_canvas_courses():
    url = f"{CANVAS_BASE_URL}/api/v1/courses"
    headers = {
        "Authorization": f"Bearer {CANVAS_API_TOKEN}"
    }
    
    courses = []
    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Append the current page of courses to the list
            courses.extend(response.json())

            # Check if there's a "next" page in the Link header
            link_header = response.headers.get('Link', None)
            if link_header:
                links = link_header.split(',')
                url = None
                for link in links:
                    if 'rel="next"' in link:
                        # Extract the next page URL from the link header
                        url = link[link.find('<')+1:link.find('>')]
                        break
            else:
                url = None  # No more pages
        else:
            break

    # Get current datetime
    now = datetime.utcnow()

    # Filter courses that have a name and are still active (end_at is in the future or None)
    # active_courses = [
    #     course for course in courses
    #     if course.get('name') and (course.get('end_at') is None or datetime.strptime(course['end_at'], "%Y-%m-%dT%H:%M:%SZ") > now)
    # ]

    return courses


# Fetch assignments for a specific course
def fetch_course_assignments(course_id):
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
@app.route('/show-assignments', methods=['GET'])
def fetch_all_assignments():
    courses = fetch_canvas_courses()
    tasks = []

    for course in courses:
        course_name = course['name']
        course_id = course['id']

        # Fetch assignments for this course
        assignments = fetch_course_assignments(course_id)

        for assignment in assignments:
            tasks.append({
                'title': assignment['name'],
                'due_date': assignment['due_at'],
                'course_name': course_name
            })

    return tasks

# Add tasks to Todoist
def add_task_to_todoist(task):
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Task content includes course name
    task_content = f"{task['title']} #{task['course_name']} in {task['course_name']}" if task['course_name'] else task['title']

    data = {
        "content": task_content,
        "due_datetime": task['due_date']
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code == 200

# Flask route to sync assignments
@app.route('/sync-assignments', methods=['POST'])
def sync_assignments():
    # Fetch assignments from Canvas
    canvas_tasks = fetch_all_assignments()
    added_tasks = []

    # Add each assignment as a task to Todoist
    for task in canvas_tasks:
        success = add_task_to_todoist(task)
        if success:
            added_tasks.append(f"{task['title']} (Course: {task['course_name']})")

    return jsonify({
        "status": "success",
        "message": f"{len(added_tasks)} assignments added to Todoist.",
        "tasks": added_tasks
    })

if __name__ == '__main__':
    app.run(debug=True)
