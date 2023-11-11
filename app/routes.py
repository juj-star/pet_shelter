from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import jsonify
from .database.db_utils import insert_animal_profile, find_animal_profile
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re
from .database.db_utils import *
from .models.hooman import Hooman
from flask import abort
from faker import Faker
from datetime import datetime
from bson import ObjectId, binary
import base64
from base64 import b64encode


main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    # Query MongoDB for available animal profiles
    available_animals_cursor = get_available_animals()
    # Convert the Cursor to a list
    available_animals_list = list(available_animals_cursor)

    # If you're storing images as binary data, convert them to Base64 strings
    for animal in available_animals_list:
        if 'pic' in animal and isinstance(animal['pic'], bytes):
            # Convert binary data to Base64 string for embedding in HTML
            animal['pic'] = base64.b64encode(animal['pic']).decode('utf-8')

    return render_template('index.html', latest_animals=available_animals_list)

@main_bp.route('/profile/<profile_id>')
def profile(profile_id):
    # Use the utility function to find the animal profile by its ID
    animal = find_animal_profile(profile_id)
    
    # If no animal is found with the given ID, you may want to redirect to a 404 page or back to the index
    if not animal:
        flash('Animal profile not found.', 'warning')
        return redirect(url_for('main_bp.index'))
    
    # Decode the binary image to base64 string for display
    if animal.get('pic'):
        animal['pic'] = b64encode(animal['pic']).decode('utf-8')
    
    # Render the animal_profile template with the animal data
    return render_template('animal_profile.html', animal=animal)

@main_bp.route('/admin_dashboard')
def admin_only_view():
    user_id = session.get('user_id', None)
    if user_id is None:
        # User is not logged in
        flash('You must be logged in to view this page.', 'warning')
        return redirect(url_for('main_bp.login'))

    user = find_hooman_by_id(user_id)
    if user is None:
        # User not found in the database
        flash('User not found.', 'danger')
        return redirect(url_for('main_bp.login'))

    # Here we check the user object itself for an 'is_admin' property
    if not user.get('is_admin'):
        abort(403)  # Forbidden access
    
    # Fetch all user profiles from the database
    all_users = get_all_users()
    print("debug:")
    print(all_users)

    return render_template('admin_dashboard.html', users=all_users)

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
            # Set is_admin in session, check if is_admin key exists and is true
            session['is_admin'] = user.get('is_admin', False)

            if session['is_admin']:
                # If the user is admin, redirect to the admin dashboard
                flash('Logged in successfully as admin!', 'success')
                return redirect(url_for('main_bp.admin_only_view'))
            else:
                # Redirect to the user dashboard for non-admin users
                flash('Logged in successfully!', 'success')
                return redirect(url_for('main_bp.user_dashboard'))
        else:
            # Invalid credentials
            flash('Invalid username or password.', 'danger')

    # If GET request or login failed, render the login template
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

        # Check if username or email already exists in the database
        if find_user_by_username(username) is not None:
            flash('Username already exists.', 'danger')
            return redirect(url_for('main_bp.signup'))

        if find_user_by_email(email) is not None:
            flash('Email already exists.', 'danger')
            return redirect(url_for('main_bp.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Instantiate a new Hooman without the username and password
        hooman = Hooman(None, name, email, phone, address)
        
        # Convert Hooman instance to a document
        hooman_doc = hooman.to_document()
        
        # Add username and password to the document
        hooman_doc['username'] = username
        hooman_doc['password'] = hashed_password

        # Store the Hooman document in the database
        insert_hooman(hooman_doc)

        # Redirect to login with success message
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('main_bp.login'))

    # Render the signup template if GET request
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
    flash(f"Session: {session}", 'info')
    user_id = session['user_id']
    flash(f"User ID: {user_id}", 'info')
    # Assume you have a function named `find_hooman_by_id` to retrieve the user information.
    hooman = find_hooman_by_id(user_id)
    if hooman is None:
        flash('Hooman not found.', 'danger')
        return redirect(url_for('main_bp.index'))

    # Perform any additional processing needed for the hooman's data

    return render_template('user_dashboard.html', hooman=hooman)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/logout')
def logout():
    # Here you'd clear the session or remove the 'user_id'
    session.pop('user_id', None)
    session.pop('username', None)  # If you are storing this in session as well
    flash('You have been logged out.', 'success')
    return redirect(url_for('main_bp.index'))

@main_bp.route('/test_users')
def test_users():
    all_users = get_all_users()
    return str(all_users)  # For debugging, return the raw data as a string

fake = Faker()

@main_bp.route('/generate_test_users', methods=['GET'])
def generate_test_users():
    users_created = []
    for _ in range(10):
        name = fake.name()
        username = fake.user_name()  # Generate a fake username
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address()
        password = generate_password_hash('password')  # For testing purposes
        hooman = Hooman(None, name, email, phone, address)
        hooman_doc = hooman.to_document()
        hooman_doc['username'] = username  # Add the username to the document
        hooman_doc['password'] = password  # Include password in the document
        insert_hooman(hooman_doc)
        users_created.append(hooman_doc)
    return jsonify({"message": "Test users created", "users": users_created}), 201

@main_bp.route('/search_user', methods=['POST'])
def search_user():
    user_id = request.form.get('user_id')
    # Assume you have a function that searches for a user by ID
    user = find_hooman_by_id(user_id)
    if user:
        # Return the search results, perhaps rendering them on a different template or the same admin dashboard
        return render_template('admin_dashboard.html', users=[user])
    else:
        flash('No user found with that ID.', 'warning')
        return render_template('admin_dashboard.html')
    
@main_bp.route('/add_animal_profile', methods=['GET', 'POST'])
def add_animal_profile():
    if request.method == 'POST':
        try:
            # Extract form data
            type_name = request.form['type_name']
            breed_name = request.form['breed_name']
            dispositions = request.form.getlist('dispositions')  # This will be a list of checked dispositions
            pic = request.files['pic']
            availability = request.form['availability']
            description = request.form['description']

            # Convert the image to binary data
            pic_binary = binary.Binary(pic.read())

            # Construct the animal profile document
            animal_profile_document = {
                '_id': str(ObjectId()),  # Generate new ObjectId
                'type_name': type_name,
                'breed_name': breed_name,
                'dispositions': dispositions,
                'pic': pic_binary,  # Store the binary data of the picture
                'availability': availability,
                'description': description,
                'date_created': datetime.utcnow().isoformat()  # Record the current time as the creation time
            }

            # Insert the document into MongoDB
            insert_animal_profile(animal_profile_document)

            flash('Animal profile added successfully!', 'success')
            return redirect(url_for('main_bp.index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

    # If it's a GET request or there's an error, it will render the form again
    return render_template('add_animal_profile.html')

@main_bp.route('/adopt_animal/<profile_id>', methods=['POST'])
def adopt_animal(profile_id):
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to adopt an animal.', 'warning')
        return redirect(url_for('main_bp.login'))
    
    # Retrieve the animal profile
    animal = find_animal_profile(profile_id)
    if not animal:
        flash('Animal profile not found.', 'danger')
        return redirect(url_for('main_bp.index'))
    
    # Check if the animal is already available for adoption
    if animal['availability'] != 'Available':
        flash('This animal is not available for adoption.', 'warning')
        return redirect(url_for('main_bp.profile', profile_id=profile_id))

    # Set animal's availability to 'Pending'
    update_data = {'availability': 'Pending'}
    update_animal_profile(profile_id, update_data)
    
    # Add the animal to the user's adoption history
    hooman = find_hooman(user_id)
    if hooman:
        adoption_history = hooman.get('adoption_history', [])
        adoption_history.append(profile_id)
        update_hooman(user_id, {'adoption_history': adoption_history})
        flash('Adoption request submitted. Waiting for approval.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('main_bp.profile', profile_id=profile_id))

@main_bp.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('is_admin'):
        abort(403)  # Only allow admins to delete users

    result = delete_hooman(user_id)  # Assumes delete_hooman is a function you have created
    if result.deleted_count:
        flash('User deleted successfully.', 'success')
    else:
        flash('User could not be deleted.', 'danger')

    return redirect(url_for('main_bp.admin_only_view'))

@main_bp.route('/admin_animal_dashboard')
def admin_animal_dashboard():
    # Check if the user is an admin
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to view this page.', 'warning')
        return redirect(url_for('main_bp.login'))
    else:
        flash(f'User ID obtained from session: {user_id}', 'debug')  # Debugging message

    user = find_hooman_by_id(user_id)
    if user is None:
        flash('User not found in the database.', 'danger')
        return redirect(url_for('main_bp.index'))
    elif not user.get('is_admin'):
        flash('The user is not authorized as an admin.', 'danger')
        return redirect(url_for('main_bp.index'))
    else:
        flash('Admin user verified.', 'debug')  # Debugging message

    # Fetch animals grouped by their availability
    pending_animals_list = get_pending_animals()
    available_animals_list = get_available_animals()  # Assuming you have this function as well
    unavailable_animals_list = get_unavailable_animals()

    for animal_list in (pending_animals_list, available_animals_list, unavailable_animals_list):
        for animal in animal_list:
            if animal.get('pic'):
                # Ensure the image data is a string in Base64 format
                animal['pic'] = b64encode(animal['pic']).decode('utf-8')

    flash(f'Pending Animals: {len(pending_animals_list)} found.', 'debug')  # Debugging message
    flash(f'Available Animals: {len(available_animals_list)} found.', 'debug')  # Debugging message
    flash(f'Unavailable Animals: {len(unavailable_animals_list)} found.', 'debug')  # Debugging message

    # Pass the sorted lists to the template
    return render_template('admin_animal_dashboard.html', 
                           pending_animals=pending_animals_list,
                           available_animals=available_animals_list,
                           unavailable_animals=unavailable_animals_list)

@main_bp.route('/edit_animal/<animal_id>', methods=['GET', 'POST'])
def edit_animal(animal_id):
    # Admin check omitted for brevity, but should be included here
    animal = find_animal_profile(animal_id)
    if not animal:
        flash('Animal profile not found.', 'danger')
        return redirect(url_for('main_bp.admin_animal_dashboard'))

    if request.method == 'POST':
        # Process the form data and update the animal profile
        type_name = request.form['type_name']
        breed_name = request.form['breed_name']
        dispositions = request.form.getlist('dispositions')
        availability = request.form['availability']
        description = request.form['description']

        update_data = {
            'type_name': type_name,
            'breed_name': breed_name,
            'dispositions': dispositions,
            'availability': availability,
            'description': description
        }
        # Update the animal profile in the database
        update_animal_profile(animal_id, update_data)
        flash('Animal profile updated successfully.', 'success')
        return redirect(url_for('main_bp.admin_animal_dashboard'))

    # Render the edit page with the animal data pre-filled
    return render_template('edit_animal.html', animal=animal)

@main_bp.route('/delete_animal/<animal_id>', methods=['POST'])
def delete_animal(animal_id):
    # Admin check omitted for brevity, but should be included here
    result = delete_animal_profile(animal_id)
    if result.deleted_count > 0:
        flash('Animal profile deleted successfully.', 'success')
    else:
        flash('Could not delete animal profile.', 'danger')
    return redirect(url_for('main_bp.admin_animal_dashboard'))

@main_bp.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Admin check here
    if 'is_admin' not in session or not session['is_admin']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main_bp.login'))

    user = find_hooman_by_id(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main_bp.admin_only_view'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        is_admin = 'is_admin' in request.form

        # Update password if field is not empty
        password = request.form.get('password')
        hashed_password = generate_password_hash(password) if password else None

        update_data = {
            'username': username,
            'email': email,
            'name': name,
            'phone': phone,
            'address': address,
            'is_admin': is_admin,
        }

        # Only update the password if a new one was provided
        if hashed_password:
            update_data['password'] = hashed_password

        # Update the user profile in the database
        update_result = update_hooman(user_id, update_data)
        if update_result:
            flash('User profile updated successfully.', 'success')
        else:
            flash('Failed to update user profile.', 'danger')
        return redirect(url_for('main_bp.admin_only_view'))

    return render_template('edit_user.html', user=user)
