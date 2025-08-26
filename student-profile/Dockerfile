FROM python:3.11-slim

WORKDIR /app

# Install netcat (use correct package name for Debian slim)
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

# Start with wait-for-it
CMD ["./wait-for-it.sh", "student-db", "5432", "python", "app.py"]
