# Use an official Python 3.10 slim image as the base
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures that Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project code into the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# The command that will be run when the container starts
# It starts the Gunicorn server to serve your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "learning_log_project.wsgi"]

# Expose port 8000 for Docker
EXPOSE 8000