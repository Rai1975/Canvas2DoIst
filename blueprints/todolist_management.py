# blueprints/todoist_management.py
from flask import Blueprint, jsonify
import requests

todoist_management_bp = Blueprint('todoist_management', __name__)

# Add tasks to Todoist
def add_task_to_todoist(task):
    from main import TODOIST_API_TOKEN

    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}",
        "Content-Type": "application/json"
    }

    task_content = f"{task['title']} in {task['course_name']}" if task['course_name'] else task['title']

    data = {
        "content": task_content,
        "due_datetime": task['due_date']
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code == 200

# Flask route to sync assignments
@todoist_management_bp.route('/sync-assignments', methods=['GET'])
def sync_assignments():
    from blueprints.assignment_management import fetch_all_assignments

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