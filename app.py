import os
from flask import Flask, jsonify  # Import Flask and jsonify to create an application instance and send JSON responses.
from flask_restful import Api  # Import Api to handle RESTful API resources.
import flask_jwt_extended  # Import necessary JWT functions and classes.

# Import the necessary modules for security and resources
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, UserLogin

# Create the Flask application instance
app = Flask(__name__)

# Application Configuration
app.config['DEBUG'] = True  # Enable debug mode for development.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  # Set the database URL.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications for performance.
app.config['PROPAGATE_EXCEPTIONS'] = True  # Enable propagation of exceptions for better error handling.
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Set a secret key for JWT (should be kept secret).

# Create an API object to manage the resources and JWTManager for handling JWT
api = Api(app)
jwt = flask_jwt_extended.JWTManager(app)

# Add resource endpoints to the API
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/auth')  # New authentication endpoint

# Error Handler for Unauthorized Access
@app.errorhandler(401)
def auth_error(err):
    return jsonify({'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401

# JWT Identity Callback Function
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']  # Extract the user identity from the token payload.
    return identity  # Return the user identity.

# Main Application Entry Point
if __name__ == '__main__':
    from db import db  # Import the db instance (SQLAlchemy)

    db.init_app(app)  # Initialize the database with the application

    if app.config['DEBUG']:
       with app.app_context():
        db.create_all()
    app.run(port=5000)  # Run the application on port 5000
