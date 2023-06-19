#!/bin/bash

# Store the process ID (PID) of the Flask application
FLASK_PID_FILE="/var/run/flask.pid"

# Function to stop the Flask application
stop_flask() {
    # Read the process ID from the file
    if [ -f "$FLASK_PID_FILE" ]; then
        FLASK_PID=$(cat "$FLASK_PID_FILE")
        # Terminate the Flask application process
        kill "$FLASK_PID"
        # Remove the PID file
        rm "$FLASK_PID_FILE"
        echo "Flask application stopped."
    else
        echo "Flask application is not running."
    fi
}

# Call the function to stop the Flask application
stop_flask
