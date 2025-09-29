# Start with a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install uv and then project dependencies
RUN pip install uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Set a dummy secret key for build-time
ENV SECRET_KEY=dummy-key-for-build

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT memetrends.wsgi:application
