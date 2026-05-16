FROM python:3.12-bookworm

# Install system dependencies if aiboto3 needs to compile (common on slim)
#RUN apt-get update && apt-get install -y --no-install-recommends \
    
  
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Use host network during build if you still get 'Name Resolution' errors
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY . .

# --host 0.0.0.0 is required for Docker access
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
