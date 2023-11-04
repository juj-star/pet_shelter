from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .database.db_utils import insert_animal_profile, find_animal_profile
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .database.db_utils import insert_hooman
import re
from .database.db_utils import find_user_by_username
from .database.db_utils import find_hooman_by_id
from .database.db_utils import find_user_by_email
from .forms import AnimalProfileForm


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
            # Set up the user session
            session['user_id'] = str(user['_id'])  # Convert ObjectId to string
            session['username'] = user['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_bp.user_dashboard'))  # Redirect to the user dashboard
        else:
            # Invalid credentials
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main_bp.login'))

    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract all Hooman related information from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # Validate data
        if not all([username, email, password, name, phone, address]):
            flash('Please fill out all fields.', 'warning')
            return redirect(url_for('main_bp.signup'))

        # Check for valid email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', 'danger')
            return redirect(url_for('main_bp.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Prepare hooman data
        hooman_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'name': name,
            'phone': phone,
            'address': address,
            'adoption_history': []  # Assuming no adoption history upon signing up
        }

        # Check if username or email already exists
        existing_user = find_user_by_username(username) or find_user_by_email(email)  # Implement find_user_by_email
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('main_bp.signup'))

        # Store in database as hooman
        insert_hooman(hooman_data)

        # Redirect to login or show success message
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('main_bp.login'))

    return render_template('signup.html')

@main_bp.route('/check_username/<username>')
def check_username(username):
    user = find_user_by_username(username)
    if user:
        return f"User with username {username} exists."
    else:
        return f"No user found with username {username}."
    
@main_bp.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('main_bp.login'))

    user_id = session['user_id']
    # Assume you have a function named `find_hooman_by_id` to retrieve the user information.
    hooman = find_hooman_by_id(user_id)
    if hooman is None:
        flash('Hooman not found.', 'danger')
        return redirect(url_for('main_bp.index'))

    # Perform any additional processing needed for the hooman's data

    return render_template('user_dashboard.html', hooman=hooman)

@main_bp.route('/add_animal_profile', methods=['GET', 'POST'])
def add_animal_profile():
    form = AnimalProfileForm()  # Instantiate your form

    if form.validate_on_submit():  # Checks if the form has been submitted and is valid
        # Collect data from the form
        animal_data = {
            'type_id': form.type_id.data,
            'breed_id': form.breed_id.data,
            'disposition_id': form.disposition_id.data,
            'availability_id': form.availability_id.data,
            'description': form.description.data,
            # Add logic for handling picture upload if necessary
        }
        
        # Save the animal profile to the database
        insert_animal_profile(animal_data)

        flash('Animal profile added successfully!', 'success')
        return redirect(url_for('main_bp.index'))  # Redirect to the index page

    # If the request is GET or the form is not valid, render the add animal profile page with the form
    return render_template('add_animal_profile.html', form=form)