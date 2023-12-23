from app import create_app, db
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize the Flask application
app = create_app()

# Set up logging
if not app.debug and not app.testing:
    # Create a file handler object
    file_handler = RotatingFileHandler('instance/app.log', maxBytes=10240, backupCount=10)

    # Set the logging format
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    # Set the logging level
    file_handler.setLevel(logging.INFO)

    # Add the handler to the app's logger
    app.logger.addHandler(file_handler)

    # Log that the app is starting up
    app.logger.info('Application startup')

# Run the application
if __name__ == '__main__':
    # Note: The following line should only be used in development
    # In production, use a production-grade server like Gunicorn
    app.run(host='0.0.0.0', port=5000)
