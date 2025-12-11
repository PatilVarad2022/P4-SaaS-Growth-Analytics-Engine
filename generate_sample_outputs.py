"""
Generate sample pipeline outputs for examples/sample_outputs/

This creates representative samples of customer_metrics and kpi_snapshot
"""

import pandas as pd
from pathlib import Path

# Create directory
output_dir = Path("examples/sample_outputs")
output_dir.mkdir(parents=True, exist_ok=True)

# Sample customer_metrics.csv
customer_metrics_sample = pd.DataFrame([
    {
        'customer_id': 'U000001',
        'recency_days': 45,
        'frequency_180d': 12,
        'monetary_180d': 588,
        'rfm_score': 'High',
        'churn_risk': 'Low'
    },
    {
        'customer_id': 'U000002',
        'recency_days': 75,
        'frequency_180d': 3,
        'monetary_180d': 147,
        'rfm_score': 'Medium',
        'churn_risk': 'Medium'
    },
    {
        'customer_id': 'U000003',
        'recency_days': 120,
        'frequency_180d': 1,
        'monetary_180d': 49,
        'rfm_score': 'Low',
        'churn_risk': 'High'
    }
])

customer_metrics_sample.to_csv(output_dir / 'customer_metrics.csv', index=False)
print(f"✓ Created {output_dir / 'customer_metrics.csv'}")

# Sample kpi_snapshot.csv
kpi_snapshot_sample = pd.DataFrame([
    {
        'snapshot_date': '2025-12-12',
        'total_revenue': 229302.00,
        'active_customers': 9234,
        'mrr': 229302.00,
        'arpu': 24.83,
        'churn_rate': 0.05
    }
])

kpi_snapshot_sample.to_csv(output_dir / 'kpi_snapshot.csv', index=False)
print(f"✓ Created {output_dir / 'kpi_snapshot.csv'}")

print("\n✓ Sample outputs created in examples/sample_outputs/")
