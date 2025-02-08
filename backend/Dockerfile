FROM python:3.10.0-slim AS builder

# Set the working directory
WORKDIR /app

# Copy requirements.txt and setup.py
COPY requirements.txt setup.py ./

# Install dependencies (Including FastAPI and Uvicorn)
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install fastapi uvicorn

# Verify uvicorn installation
RUN uvicorn --version

COPY . .

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]