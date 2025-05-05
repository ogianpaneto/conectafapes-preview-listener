FROM python:3.13-slim

# Install SSH client
RUN apt-get update && apt-get install -y openssh-client && rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

# Copy SSH key (you’ll mount the key at runtime instead in production)
RUN mkdir -p /root/.ssh

# Default port
EXPOSE 8080

CMD ["python", "app.py"]
