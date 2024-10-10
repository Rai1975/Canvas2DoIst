# routes/todoist_management.py
from flask import Blueprint, jsonify
import requests
from config import TODOIST_API_TOKEN

todoist_management_bp = Blueprint('todoist_management', __name__)

# Retrieve tasks from Todoist (to avoid duplication)
def fetch_todoist_tasks():
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return []

# Add tasks to Todoist
def add_task_to_todoist(task):
    existing_tasks = fetch_todoist_tasks()

    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}",
        "Content-Type": "application/json"
    }

    task_content = f"{task['title']} in {task['course_name']}" if task['course_name'] else task['title']

    # Check if task already exists in
    for existing_task in existing_tasks:
        if existing_task['content'] == task_content:
            # Task already exists, skip adding it
            print(f"Task '{task_content}' already exists in Todoist. Skipping.")
            return False

    data = {
        "content": task_content,
        "due_datetime": task['due_date']
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code == 200

# Flask route to sync assignments
@todoist_management_bp.route('/sync-assignments', methods=['GET'])
def sync_assignments():
    from routes.assignment_management import fetch_all_assignments

    canvas_tasks = fetch_all_assignments().get_json()
    added_tasks = []

    for task in canvas_tasks:
        success = add_task_to_todoist(task)
        if success:
            added_tasks.append(f"{task['title']} (Course: {task['course_name']})")

    return jsonify({
        "status": "success",
        "message": f"{len(added_tasks)} assignments added to Todoist.",
        "tasks": added_tasks
    })