# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first for better caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install  -r requirements.txt

# Copy the rest of the application source code
COPY . /app

# Expose the Flask server port
EXPOSE 5000

# Run the Flask application
CMD ["python", "NexScan.py"]
