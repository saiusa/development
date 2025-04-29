#!/bin/bash

# Path to your virtual environment's activate script
echo "Activating virtual environment..."
source .././virt/bin/activate

# Notify user that the environment has been activated
echo "Virtual environment activated."

# Optionally, you can add any commands you want to run after activation
echo "Starting Gunicorn server..."

# Start Gunicorn in the same shell (so the virtual environment remains active)
exec gunicorn --reload --bind 0.0.0.0:8001 app.wsgi:application

# This will not be reached because `exec` replaces the current process
echo "Gunicorn server is running on http://0.0.0.0:8001"

