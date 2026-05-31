FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create instance directory for database
RUN mkdir -p instance

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]