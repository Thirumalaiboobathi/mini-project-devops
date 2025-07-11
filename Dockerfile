# Use official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir flask requests prometheus_flask_exporter

# Expose the port your app runs on
EXPOSE 4000

# Run the application
CMD ["python", "app.py"]
