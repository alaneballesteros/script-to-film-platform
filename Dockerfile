FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY pyproject.toml .

# Install the package
RUN pip install -e .

# Create data directories
RUN mkdir -p data/scripts data/output data/temp

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "script_to_film.main:app", "--host", "0.0.0.0", "--port", "8000"]
