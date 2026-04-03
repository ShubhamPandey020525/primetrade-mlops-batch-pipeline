# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and config files into the container
COPY run.py .
COPY config.yaml .
COPY dataset/data.csv dataset/data.csv

# Set default command to run the script
# python run.py --input dataset/data.csv --config config.yaml --output metrics.json --log-file run.log
CMD ["python", "run.py", "--input", "dataset/data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]
