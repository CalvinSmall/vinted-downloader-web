FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install vinted-downloader
RUN pip install vinted-downloader

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install flask gunicorn

# Create downloads directory
RUN mkdir -p /app/downloads

# Expose port
EXPOSE 5000

# Start application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]