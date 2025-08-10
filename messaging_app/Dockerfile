# Use official Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt first for caching dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose default Django port
EXPOSE 8000

# Default command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
