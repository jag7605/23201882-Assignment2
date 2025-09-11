FROM python:3.11-slim

# All of the Dockerfiles in this project are based on python 3.11-slim and are pretty much identical with the exception of the
# Dockerfile in frontend/src.

WORKDIR /app

# Install netcat (needed for wait-for-it.sh)
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Make wait-for-it executable
RUN chmod +x wait-for-it.sh

# Start service with wait-for-it
CMD ["./wait-for-it.sh", "student-db", "5432", "python", "app.py"]