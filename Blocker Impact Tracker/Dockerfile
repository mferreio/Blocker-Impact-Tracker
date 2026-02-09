# Base image
FROM python:3.9-slim

# Working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Note: Health check handled by Koyeb externally

# Entrypoint - Use PORT env var (Koyeb sets this)
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
