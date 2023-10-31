from flask import Blueprint, render_template, request, redirect, url_for
from .database.db_utils import insert_animal_profile, find_animal_profile

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    # Fetch latest animal profiles for the daily feed
    # This is a placeholder, you'll need to implement the actual query
    latest_animals = []
    return render_template('index.html', latest_animals=latest_animals)

@main_bp.route('/profile/<profile_id>')
def profile(profile_id):
    # Fetch animal profile by ID
    animal_profile = find_animal_profile(profile_id)
    return render_template('profile.html', animal_profile=animal_profile)

@main_bp.route('/admin/dashboard')
def admin_dashboard():
    # Admin dashboard logic here
    return render_template('admin_dashboard.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        pass
    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle signup logic
        # You might want to collect username, password, etc.
        # Remember to validate and store these details securely
        pass
    return render_template('signup.html')