# PHASE 2 - ARCHITECTURE PLAN (RE-VERIFIED)

## 1. Project Folder Structure
```
ML_Intern_/
├── data.csv (dataset)
├── config.yaml (config file)
├── run.py (main execution script)
├── requirements.txt (dependencies)
├── Dockerfile (Docker definition)
├── README.md (project documentation)
├── metrics.json (generated output)
└── run.log (generated log)
```

## 2. Required Files
- `run.py`: Entry point for the batch job. Handles CLI arguments, processing, and output generation.
- `config.yaml`: Configuration settings (seed, window, version).
- `data.csv`: Input dataset (OHLCV).
- `requirements.txt`: Python dependencies (pandas, pyyaml, numpy).
- `Dockerfile`: Container image configuration.
- `README.md`: Instructions for local and Docker runs.

## 3. Script Responsibilities (`run.py`)
- `setup_logging(log_file)`: Configures the logging module to output to both a file and stderr.
- `load_config(config_path)`: Reads YAML and validates `seed`, `window`, and `version`.
- `load_data(data_path)`: Reads CSV and validates 'close' column existence. Handles missing/empty files.
- `process_data(df, window, seed)`:
    - Sets random seed for reproducibility.
    - Computes `rolling_mean` on the 'close' column using `window`.
    - Generates binary `signal` (1 if close > rolling_mean, 0 otherwise).
    - Excludes first `window-1` rows from signal rate computation.
- `calculate_metrics(df, start_time, version, seed)`:
    - `rows_processed`: Count of all rows.
    - `signal_rate`: Mean of binary signals excluding NaNs.
    - `latency_ms`: Execution time in milliseconds.
- `save_metrics(metrics, output_path)`: Writes to JSON and prints to stdout.
- `main()`: Orchestrates the flow and implements high-level error handling.

## 4. Data Flow
`data.csv` (input) -> `load_data` -> `process_data` (rolling mean, signal) -> `calculate_metrics` -> `save_metrics` -> `metrics.json` (output).

## 5. Logging Strategy
- Log file: `run.log`.
- Log entries:
    - Job start/end.
    - Config loading status.
    - Dataset statistics (rows loaded).
    - Processing step markers.
    - Metrics summary.
    - Detailed error/exception information.

## 6. Error Handling Strategy
- Catch file-related errors (`FileNotFoundError`).
- Catch parsing errors (`ValueError`, `yaml.YAMLError`).
- Catch data-related errors (missing columns).
- Always write a `status: error` `metrics.json` on any failure.
- Ensure non-zero exit code for all failures.

## 7. Metrics Generation Logic
- Success output keys: `version`, `rows_processed`, `metric`, `value`, `latency_ms`, `seed`, `status`.
- Value for `metric` is `signal_rate`.

## 8. Docker Execution Behavior
- Copies all code and data into the container.
- Installs dependencies from `requirements.txt`.
- Runs `run.py` with the required CLI arguments.
- Prints the final JSON to stdout.
