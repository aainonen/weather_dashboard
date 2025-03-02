# Use a lightweight Python base image
FROM python:3.9-slim

# Prevent Python from writing pyc files to disc and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port the app will run on (matching Gunicorn's port)
EXPOSE 8000

# Use Gunicorn as the production WSGI server to run your app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
