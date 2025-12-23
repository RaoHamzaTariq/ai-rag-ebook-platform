# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# 1. Copy requirements using the full path from the repo root.
COPY backend/requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the entire backend folder into the /app directory
COPY backend/ .

# 4. Set PYTHONPATH so Python can find the 'src' folder inside /app
ENV PYTHONPATH=/app

# 5. Expose the port
EXPOSE 80

# 6. Start FastAPI 
# Since we copied the contents of 'backend' into '/app', 
# your 'src' folder is now at '/app/src'
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
