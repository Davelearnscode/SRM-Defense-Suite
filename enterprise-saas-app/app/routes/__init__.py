from flask import Blueprint

# Create a blueprint for the routes
main = Blueprint('main', __name__)

# Import routes here to register them with the blueprint
from . import example_routes  # Replace with actual route files as needed