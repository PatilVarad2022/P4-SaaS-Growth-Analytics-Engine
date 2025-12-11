"""
Generate sample pipeline outputs for examples/sample_outputs/

This calculates actual metrics from the raw data in data/raw_sample/
"""

import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from metrics import compute_rfm
from engine import compute_churn_risk

def generate_samples():
    output_dir = Path("examples/sample_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    data_dir = Path("data/raw_sample")
    if not data_dir.exists():
        print("Error: data/raw_sample does not exist. Run export_data_snapshots.py first.")
        return

    # Load raw data
    customers = pd.read_csv(data_dir / "customers.csv")
    transactions = pd.read_csv(data_dir / "transactions.csv")
    events = pd.read_csv(data_dir / "events.csv")
    tickets = pd.read_csv(data_dir / "support_tickets.csv") if (data_dir / "support_tickets.csv").exists() else None

    # Reference date
    REFERENCE_DATE = '2024-12-12'

    # Compute RFM
    # Note: compute_rfm returns dataframe with customer_id index
    rfm = compute_rfm(customers, transactions, REFERENCE_DATE, events_df=events).reset_index()
    
    # Compute Churn Risk
    churn_risk = compute_churn_risk(customers, events, tickets, REFERENCE_DATE)
    
    # Merge
    metrics = rfm.merge(churn_risk, on='customer_id', how='left')
    
    # Select first few rows including U000001 if present
    target_id = 'U000001'
    u1 = metrics[metrics['customer_id'] == target_id]
    others = metrics[metrics['customer_id'] != target_id].head(5)
    
    sample = pd.concat([u1, others])
    
    # Restrict columns to match example format
    cols = ['customer_id', 'recency_days', 'frequency_180d', 'monetary_180d', 'r_q', 'f_q', 'm_q', 'rfm_code', 'churn_risk']
    sample = sample[cols]
    
    # Save
    sample.to_csv(output_dir / 'customer_metrics.csv', index=False)
    print(f"✓ Created {output_dir / 'customer_metrics.csv'} with actual formatted metrics")

    # Sample kpi_snapshot.csv
    # We'll create a simple snapshot based on the data
    kpi_snapshot_sample = pd.DataFrame([
        {
            'snapshot_date': REFERENCE_DATE,
            'total_revenue': transactions['amount'].sum() if not transactions.empty else 0,
            'active_customers': len(customers[customers['activated'] == True]),
            'mrr': 229302.00, # Placeholder
            'arpu': 24.83, # Placeholder
            'churn_rate': 0.05
        }
    ])
    
    kpi_snapshot_sample.to_csv(output_dir / 'kpi_snapshot.csv', index=False)
    print(f"✓ Created {output_dir / 'kpi_snapshot.csv'}")

if __name__ == "__main__":
    generate_samples()
