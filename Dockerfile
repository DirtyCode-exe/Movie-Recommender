FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PORT 5050
ENV FLASK_APP=app.py

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5050
EXPOSE 5050

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=$PORT"]
