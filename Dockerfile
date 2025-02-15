# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r REQUIREMENTS.TXT

# Make port 8282 available to the world outside this container
EXPOSE 8282

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8282"]
