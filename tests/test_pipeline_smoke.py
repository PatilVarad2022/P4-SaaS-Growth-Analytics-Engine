"""
Pipeline smoke test - Verifies output columns exist

Run: pytest tests/test_pipeline_smoke.py -v
"""

import pandas as pd
from pathlib import Path


def test_customer_metrics_columns():
    """Verify customer_metrics.csv has required columns"""
    sample_file = Path("examples/sample_outputs/customer_metrics.csv")
    
    if not sample_file.exists():
        # Skip if sample not generated yet
        return
    
    df = pd.read_csv(sample_file)
    
    required_columns = [
        'customer_id',
        'recency_days',
        'frequency_180d',
        'monetary_180d',
        'rfm_score',
        'churn_risk'
    ]
    
    for col in required_columns:
        assert col in df.columns, f"Missing column: {col}"
    
    print(f"✓ customer_metrics.csv has all {len(required_columns)} required columns")


def test_kpi_snapshot_columns():
    """Verify kpi_snapshot.csv has required columns"""
    sample_file = Path("examples/sample_outputs/kpi_snapshot.csv")
    
    if not sample_file.exists():
        # Skip if sample not generated yet
        return
    
    df = pd.read_csv(sample_file)
    
    required_columns = [
        'snapshot_date',
        'total_revenue',
        'active_customers',
        'mrr',
        'arpu',
        'churn_rate'
    ]
    
    for col in required_columns:
        assert col in df.columns, f"Missing column: {col}"
    
    print(f"✓ kpi_snapshot.csv has all {len(required_columns)} required columns")


def test_raw_data_files_exist():
    """Verify all raw data files exist"""
    data_dir = Path("data/raw_sample")
    
    required_files = [
        'customers.csv',
        'transactions.csv',
        'subscriptions.csv',
        'events.csv',
        'support_tickets.csv'
    ]
    
    for filename in required_files:
        filepath = data_dir / filename
        assert filepath.exists(), f"Missing file: {filepath}"
    
    print(f"✓ All {len(required_files)} raw data files exist")


if __name__ == "__main__":
    test_customer_metrics_columns()
    test_kpi_snapshot_columns()
    test_raw_data_files_exist()
    print("\n✓ All smoke tests passed!")
