from flask import Blueprint, render_template, request, redirect, url_for, flash
from .database.db_utils import insert_animal_profile, find_animal_profile
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .database.db_utils import insert_hooman
import re
from .database.db_utils import find_user_by_username

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
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if user exists
        user = find_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            # User exists and password is correct
            # Here you can set up the user session or any other login mechanism
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_bp.index'))
        else:
            # Invalid credentials
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main_bp.login'))

    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate data
        if not username or not email or not password:
            flash('Please fill out all fields.')
            return redirect(url_for('main_bp.signup'))

        # Check for valid email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.')
            return redirect(url_for('main_bp.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)  # Method removed

        # Prepare hooman data
        hooman_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }

        # Store in database as hooman
        insert_hooman(hooman_data)

        # Redirect to login or show success message
        flash('Account created successfully! Please login.')
        return redirect(url_for('main_bp.login'))

    return render_template('signup.html')

@main_bp.route('/check_username/<username>')
def check_username(username):
    user = find_user_by_username(username)
    if user:
        return f"User with username {username} exists."
    else:
        return f"No user found with username {username}."
    