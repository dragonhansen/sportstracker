# Use a Python base image with your desired Python version
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the application code and requirements.txt into the container
COPY app.py /app/
COPY scraper.py /app/
COPY static/* /app/static/
COPY templates/* /app/templates/
COPY requirements.txt /app/

# Install any project dependencies
RUN pip install -r requirements.txt

# Expose the port your web server will listen on
EXPOSE 8000

# Define the command to run your Python application
CMD ["python", "app.py"]