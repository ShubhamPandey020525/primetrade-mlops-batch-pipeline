import argparse
import io
import json
import logging
import os
import sys
import time
import pandas as pd
import yaml
import numpy as np

def setup_logging(log_file):
    """Configures the logging module."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stderr)
        ]
    )
    return logging.getLogger("mlops_job")

def load_config(config_path, logger):
    """Loads and validates the YAML configuration."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")
            
    required_fields = ['seed', 'window', 'version']
    for field in required_fields:
        if config is None or field not in config:
            raise ValueError(f"Missing required config field: {field}")
            
    logger.info(f"Config loaded + validated (seed={config['seed']}/window={config['window']}/version={config['version']})")
    return config

def load_data(data_path, logger):
    """Loads and validates the CSV dataset."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found: {data_path}")
    
    try:
        # Check if it's empty
        if os.path.getsize(data_path) == 0:
            raise ValueError("Dataset file is empty")
            
        df = pd.read_csv(data_path)
        
        # Robust check: if only one column and it looks like it's quoted, fix it
        if len(df.columns) == 1:
            first_col = df.columns[0]
            if ',' in first_col:
                # Re-read with explicit quoting handling if necessary
                # or just strip quotes and split if it's that bad
                df = pd.read_csv(data_path, quotechar='"', skipinitialspace=True)
                if len(df.columns) == 1:
                    # Last resort: read all lines, strip quotes, and re-parse
                    with open(data_path, 'r') as f:
                        lines = [line.strip().strip('"') for line in f if line.strip()]
                    df = pd.read_csv(io.StringIO('\n'.join(lines)))
    except Exception as e:
        raise ValueError(f"Invalid CSV format: {str(e)}")
        
    if 'close' not in df.columns:
        raise ValueError("Missing required column: 'close'")
        
    logger.info(f"Rows loaded: {len(df)}")
    return df

def save_metrics(metrics, output_path):
    """Saves metrics to a JSON file and prints to stdout."""
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    # The requirement is to print final metrics JSON to stdout
    print(json.dumps(metrics, indent=2))

def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="MLOps Batch Job")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--output", required=True, help="Path to output JSON metrics file")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    
    args = parser.parse_args()
    
    # Setup logging as early as possible
    logger = setup_logging(args.log_file)
    logger.info("Job start timestamp: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    
    version = "unknown"
    seed = None
    
    try:
        # 1. Load + validate config
        config = load_config(args.config, logger)
        version = config['version']
        seed = config['seed']
        window = config['window']
        
        # Set seed: numpy.random.seed(seed)
        np.random.seed(seed)
        
        # 2. Load + validate dataset
        df = load_data(args.input, logger)
        
        # 3. Rolling mean
        logger.info(f"Processing step: computing rolling mean with window={window}")
        df['rolling_mean'] = df['close'].rolling(window=window).mean()
        
        # 4. Signal generation
        logger.info("Processing step: generating binary signal")
        # signal = 1 if close > rolling_mean else 0
        # Handling the first window-1 rows: allow NaNs and exclude from signal computation
        df['signal'] = np.where(df['rolling_mean'].isna(), np.nan, (df['close'] > df['rolling_mean']).astype(float))
        
        # 5. Calculate metrics
        # signal_rate = mean(signal)
        # Exclude NaNs from signal computation as per instructions
        valid_signals = df['signal'].dropna()
        signal_rate = float(valid_signals.mean()) if not valid_signals.empty else 0.0
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        metrics = {
            "version": version,
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }
        
        logger.info(f"Metrics summary: {metrics}")
        save_metrics(metrics, args.output)
        logger.info("Job end + status: success")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        error_metrics = {
            "version": version,
            "status": "error",
            "error_message": str(e)
        }
        save_metrics(error_metrics, args.output)
        logger.info("Job end + status: failure")
        sys.exit(1)

if __name__ == "__main__":
    main()
