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
You can use `venv` or `conda` to create the environment:

**Using venv (Standard Python):**
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

**Using Conda:**
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
This will:
- Read `dataset/data.csv`.
- Use settings from `config.yaml`.
- Generate `metrics.json` (summary) and `run.log` (detailed logs).

---

## How to Run with Docker

This is the **easiest and recommended way** for recruiters to test the pipeline without worrying about Python versions.

### 1. Prerequisite
Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and running.

### 2. Build and Run in One Step
```bash
# Build the image
docker build -t mlops-task .

# Run the container
docker run --rm mlops-task
```
The container will process the data and print the final `metrics.json` directly to your terminal.

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
