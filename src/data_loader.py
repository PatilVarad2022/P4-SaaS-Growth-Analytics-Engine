"""
Data Loader - Loads sample raw data for the SaaS Growth Analytics Engine
"""

import pandas as pd
from pathlib import Path


def load_sample_data():
    """
    Load sample raw data from data/raw_sample/ directory.
    
    Returns:
        dict: Dictionary containing DataFrames for customers, subscriptions, invoices, events
    """
    data_dir = Path(__file__).parent.parent / "data" / "raw_sample"
    
    if not data_dir.exists():
        raise FileNotFoundError(
            f"Sample data directory not found: {data_dir}\n"
            "Please ensure data/raw_sample/ contains the required CSV files."
        )
    
    # Load all required files
    customers = pd.read_csv(data_dir / "customers.csv")
    subscriptions = pd.read_csv(data_dir / "subscriptions.csv")
    invoices = pd.read_csv(data_dir / "invoices.csv")
    events = pd.read_csv(data_dir / "events.csv")
    
    # Basic validation
    assert len(customers) > 0, "customers.csv is empty"
    assert len(subscriptions) > 0, "subscriptions.csv is empty"
    assert 'customer_id' in customers.columns, "customers.csv missing customer_id"
    assert 'subscription_id' in subscriptions.columns, "subscriptions.csv missing subscription_id"
    
    return {
        'customers': customers,
        'subscriptions': subscriptions,
        'invoices': invoices,
        'events': events
    }


def load_config(config_path):
    """Load configuration from YAML file."""
    import yaml
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config
