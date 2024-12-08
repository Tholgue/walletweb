# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    cron \
    supervisor

# Set the working directory in the container
WORKDIR /app

RUN mkdir /db

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src /app

# Create a cron job file
COPY job-cron /etc/cron.d/my-cron-job

# Set permissions for the cron job file
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply the cron job
RUN crontab /etc/cron.d/my-cron-job

# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the Flask port
EXPOSE 8000


# Start supervisord
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
# CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "walletweb:app"]