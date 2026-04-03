# PHASE 2 - ARCHITECTURE PLAN (FINAL VERIFIED)

## 1. Project Folder Structure
```
primetrade-mlops-batch-pipeline/
├── dataset/
│   └── data.csv          # Input dataset (OHLCV)
├── config.yaml           # Configuration file (seed, window, version)
├── run.py                # Main execution script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker definition
├── README.md             # Project documentation
├── metrics.json          # Generated output (machine-readable)
├── run.log               # Detailed execution logs
├── what.txt              # Technical definitions & deep analysis
└── architecture_plan.md  # This document
```

## 2. Component Definitions
- `run.py`: Entry point for the batch job. Implements the processing pipeline, handles CLI arguments, and output generation.
- `config.yaml`: Central configuration for hyperparameters (seed, window, version).
- `dataset/data.csv`: Source of 10,000 rows of OHLCV market data.
- `requirements.txt`: Minimal dependencies (`pandas`, `pyyaml`, `numpy`).
- `Dockerfile`: Multi-stage ready, standard environment definition using `python:3.9-slim`.
- `README.md`: User-facing instructions for local and Docker execution.

## 3. Script Pipeline Logic (`run.py`)
- **Initialization**: Configures dual-logging (file + stderr) via `setup_logging`.
- **Configuration**: Loads and validates YAML structure using `load_config`.
- **Data Ingestion**: Robust `load_data` function with CSV validation (handles empty files, missing columns, and formatting issues).
- **Transformation (`process_data`)**:
    - Enforces reproducibility via `np.random.seed`.
    - Computes `rolling_mean` on the 'close' column using the specified `window`.
    - Generates binary `signal`: `1` if `close > rolling_mean`, `0` otherwise.
    - Excludes the initial `window-1` rows from final signal calculations to ensure data integrity.
- **Metric Computation**:
    - `rows_processed`: Total record count.
    - `signal_rate`: Average of valid signals.
    - `latency_ms`: End-to-end execution time.
- **Output Orchestration**: Saves JSON result to disk and prints to `stdout` for container visibility.

## 4. Execution Flow
1. **Input**: `dataset/data.csv` + `config.yaml`.
2. **Process**: Load -> Validate -> Transform (Rolling Mean) -> Signal Generation.
3. **Metric**: Compute rate, latency, and status.
4. **Output**: `metrics.json` + `run.log`.

## 5. Error Handling & Reliability
- **Graceful Failures**: All exceptions are caught and logged.
- **Error JSON**: If a failure occurs, a `status: error` JSON is generated with a descriptive `error_message`.
- **Exit Codes**: Returns `0` on success and `1` on failure for pipeline integration.

## 6. Docker Implementation
- **Isolation**: Standardized environment using `python:3.9-slim`.
- **Reproducibility**: `requirements.txt` ensures identical library versions.
- **Portability**: CLI arguments passed via `CMD` allow for easy parameter overriding if needed.
- **Visibility**: Final metrics printed to container logs (stdout) for easy monitoring.

## 7. Compliance & Quality
- Follows PEP 8 coding standards.
- Implements modular, testable functions.
- Provides comprehensive logging for troubleshooting.
