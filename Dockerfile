FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libpq-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Create and activate a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the web app
EXPOSE 80

# Command to run the app
CMD ["python", "app.py"]