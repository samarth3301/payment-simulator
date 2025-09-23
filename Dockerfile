# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Environment defaults
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast pip) or fall back to pip
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY app/ ./app/
COPY run.py ./
COPY migrations/ ./migrations/
COPY models/ ./models/
COPY data/ ./data/
COPY .env.docker ./.env

# Install Python dependencies
RUN uv pip install --system -e .

# Train the fraud detection model
RUN PYTHONPATH=/app python models/transaction-detection/run_training.py

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Run the application
CMD ["python", "run.py"]