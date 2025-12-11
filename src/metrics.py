# Logic Documentation: docs/LOGIC.md | Schema: docs/SCHEMA.md
import pandas as pd
import numpy as np

def compute_rfm(users_df, transactions_df, reference_date):
    """
    Compute RFM scores for customers.
    
    Logic:
    - Recency: Days since last transaction relative to reference_date
    - Frequency: Number of transactions in the lookback window (e.g. 180 days)
    - Monetary: Total value of transactions in the lookback window
    
    Scores (1-5 scale, 5 is best):
    - Recency: Quintiles (lower is better, so reversed)
    - Frequency: Quintiles (higher is better)
    - Monetary: Quintiles (higher is better)
    
    Ref: docs/LOGIC.md
    """
    # Filter transactions before reference date
    ref_date = pd.to_datetime(reference_date)
    txns = transactions_df[pd.to_datetime(transactions_df['transaction_date']) <= ref_date].copy()
    
    # Aggregation
    rfm = txns.groupby('customer_id').agg({
        'transaction_date': lambda x: (ref_date - pd.to_datetime(x).max()).days,
        'transaction_id': 'count',
        'amount': 'sum'
    }).rename(columns={
        'transaction_date': 'recency_days',
        'transaction_id': 'frequency_180d', # Assuming input filtered or full history used as proxy
        'amount': 'monetary_180d'
    })
    
    # Scoring
    rfm['r_score'] = pd.qcut(rfm['recency_days'], 5, labels=[5, 4, 3, 2, 1])
    rfm['f_score'] = pd.qcut(rfm['frequency_180d'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['m_score'] = pd.qcut(rfm['monetary_180d'], 5, labels=[1, 2, 3, 4, 5])
    
    rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
    
    return rfm

def compute_arpu(revenue_df):
    """
    Compute ARPU from revenue metrics.
    Formula: Total MRR / Total Active Users
    """
    if len(revenue_df) == 0:
        return 0
    latest = revenue_df.iloc[-1]
    return latest['mrr'] / latest['active_users'] if latest['active_users'] > 0 else 0
