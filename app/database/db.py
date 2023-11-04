from flask_pymongo import PyMongo

# Initialize PyMongo without the app object
mongo = PyMongo()

def init_db(app):
    # Configure the PyMongo instance for the Flask app
    mongo.init_app(app)
