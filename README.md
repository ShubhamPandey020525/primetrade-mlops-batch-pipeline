# MLOps Batch Job - Task 0 Technical Assessment

## Overview
This is a minimal MLOps-style batch job that calculates a rolling mean and generates binary signals from a dataset of 10,000 OHLCV rows.

## Project Structure
```
ML_Intern_/
├── data.csv              # Input dataset (OHLCV)
├── config.yaml           # Configuration file (seed, window, version)
├── run.py                # Main batch job script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container definition
├── README.md             # Project documentation and run instructions
├── metrics.json          # Generated output (machine-readable)
├── run.log               # Detailed execution logs
├── what.txt              # Deep analysis and technical definitions
└── architecture_plan.md  # Detailed architecture design
```

## How to Run Locally

### 1. Set up the Environment
The project requires Python 3.9+ and dependencies listed in `requirements.txt`.
You can use Miniconda to create the environment:
```bash
conda create -n ML_intern python=3.9
conda activate ML_intern
pip install -r requirements.txt
```

### 2. Run the Job
Run the following command to process the dataset:
```bash
python run.py --input dataset/data.csv --config config.yaml --output metrics.json --log-file run.log
```

## How to Run with Docker

### 1. Prerequisite: Install Docker Desktop
If you get an error like `'docker' is not recognized as an internal or external command`, it means Docker is not installed or not in your system's PATH.
- **Download and install Docker Desktop** for Windows from [docker.com](https://www.docker.com/products/docker-desktop/).
- Ensure **Docker Desktop is running** (check the tray icon).
- **Restart your terminal** after installation to refresh the environment variables.

### 2. Build the Docker Image
```bash
docker build -t mlops-task .
```

### 3. Run the Docker Container
```bash
docker run --rm mlops-task
```
The container will:
- Process the dataset.
- Generate `metrics.json` and `run.log`.
- Print the final metrics JSON to stdout.

## Expected Outputs

### Example metrics.json (Success)
```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```

### Example metrics.json (Error)
```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}
```
