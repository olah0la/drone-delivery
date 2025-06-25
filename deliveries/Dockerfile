FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY generate_events.py .

# Command to run the application
CMD ["python", "generate_events.py", "${BASE_URL}"]
