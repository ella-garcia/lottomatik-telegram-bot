# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY requirements.txt requirements.txt
COPY main.py main.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default port for Cloud Run
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
