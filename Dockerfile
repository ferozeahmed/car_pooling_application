# Dockerfile for fastapi
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8005 available to the world outside this container
EXPOSE 8005

# command
CMD ["uvicorn", "main:app", "--port", "8005", "--host", "0.0.0.0"]