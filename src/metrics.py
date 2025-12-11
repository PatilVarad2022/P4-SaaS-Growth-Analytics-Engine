# See docs/LOGIC.md for RFM and churn rules; see docs/SCHEMA.md for CSV schemas.
# Logic Documentation: docs/LOGIC.md | Schema: docs/SCHEMA.md
import pandas as pd
import numpy as np

def compute_rfm(users_df, transactions_df, reference_date, events_df=None):
    """
    Compute RFM scores for customers.
    
    Logic:
    - Recency: Days since last interaction (transaction OR login OR feature_use) relative to reference_date
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
    
    # Calculate Last Interaction Date (Max of Transaction Date and Event Timestamp)
    # 1. Last Transaction
    last_txn = txns.groupby('customer_id')['transaction_date'].max()
    last_txn = pd.to_datetime(last_txn)
    
    # 2. Last Event (if provided)
    last_evt = pd.Series(dtype='datetime64[ns]')
    if events_df is not None:
        evts = events_df[pd.to_datetime(events_df['event_timestamp']) <= ref_date]
        if not evts.empty:
            last_evt = evts.groupby('customer_id')['event_timestamp'].max()
            last_evt = pd.to_datetime(last_evt)
    
    # Combine to find absolute max date per customer
    # We align them by customer_id
    interactions = pd.concat([last_txn, last_evt], axis=1, keys=['txn', 'evt'])
    interactions['last_interaction'] = interactions[['txn', 'evt']].max(axis=1)
    
    # Aggregation for F and M
    rfm_metrics = txns.groupby('customer_id').agg({
        'transaction_id': 'count',
        'amount': 'sum'
    }).rename(columns={
        'transaction_id': 'frequency_180d', # Assuming input filtered appropriately or using full history
        'amount': 'monetary_180d'
    })
    
    # Merge recency source
    rfm = rfm_metrics.merge(interactions['last_interaction'], left_index=True, right_index=True, how='outer')
    
    # Calculate Recency Days
    # Fill NaT with large number or handle appropriately? 
    # If no interaction, recency is undefined or huge.
    # We will exclude strictly empty ones or fill with a default?
    # Logic implies active customers usually have some interaction.
    # If a customer has no transaction but has event, they appear in 'interactions' but maybe not 'rfm_metrics' (outer merge handles this).
    
    rfm['recency_days'] = (ref_date - rfm['last_interaction']).dt.days
    
    # Fill NaN F/M with 0 (if they have event but no transaction)
    rfm['frequency_180d'] = rfm['frequency_180d'].fillna(0)
    rfm['monetary_180d'] = rfm['monetary_180d'].fillna(0)
    
    # For recency scoring, we need to handle NaN recency (never interacted before ref date?)
    # Dropping them or assigning max score.
    rfm = rfm.dropna(subset=['recency_days'])
    
    # Scoring
    # Use qcut with duplicates='drop'
    # Recency: Lower days = Higher Score (5). Labels [5, 4, 3, 2, 1] means 1st quintile (lowest days) -> 5.
    rfm['r_q'] = pd.qcut(rfm['recency_days'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop').astype(int)
    rfm['f_q'] = pd.qcut(rfm['frequency_180d'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['m_q'] = pd.qcut(rfm['monetary_180d'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    rfm['rfm_code'] = rfm['r_q'].astype(str) + "-" + rfm['f_q'].astype(str) + "-" + rfm['m_q'].astype(str)
    
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
