# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# 1. Copy requirements from the backend folder
# We use ./ because the Dockerfile is already inside /backend
COPY requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy everything from the current directory (backend/) into /app
COPY . .

# 4. Expose the port
EXPOSE 8000

# 5. Start FastAPI
# We use --host 0.0.0.0 so it can be reached externally
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
