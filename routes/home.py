# routes/home.py
from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)
@home_bp.route('/')
def home():
    return "Flask server is running!"
