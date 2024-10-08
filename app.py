from flask import Flask, jsonify
from datetime import datetime
import requests
import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API tokens from environment variables
CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
CANVAS_BASE_URL = os.getenv('CANVAS_BASE_URL')
COURSE_DECISIONS_CSV = 'decisions.csv'

app = Flask(__name__)

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

    # Load course decisions from CSV
    course_decisions = load_course_decisions()
    active_courses = []

    # Loop through the courses and ask if the user wants to keep each one
    for course in courses:
        course_id = str(course['id'])
        course_name = course.get('name')

        # Skip courses without a name
        if not course_name:
            continue

        # Check if we've already saved a decision for this course
        if course_id in course_decisions:
            decision = course_decisions[course_id]
        else:
            # Ask the user if they want to keep this course (yes/no)
            print(f"Do you want to keep the course '{course_name}'? (yes/no)")
            decision = input().strip().lower()

            # Save the decision to the CSV so we don't ask again
            save_course_decision(course_id, decision)

        # If the decision is 'yes', keep this course
        if decision == 'yes':
            active_courses.append(course)

    return jsonify(active_courses)


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
    courses = fetch_canvas_courses().get_json()
    tasks = []
    now = datetime.utcnow()

    for course in courses:
        course_name = course['name']
        course_id = course['id']

        # Fetch assignments for this course
        assignments = fetch_course_assignments(course_id)

        for assignment in assignments:
            due_date_str = assignment.get('due_at')
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M:%SZ")
                
                # Only include assignments that are not past due
                if due_date > now:
                    tasks.append({
                        'title': assignment['name'],
                        'due_date': due_date_str,
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
    task_content = f"{task['title']} in {task['course_name']}" if task['course_name'] else task['title']

    data = {
        "content": task_content,
        "due_datetime": task['due_date']
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code == 200

# Flask route to sync assignments
@app.route('/sync-assignments', methods=['GET'])
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
