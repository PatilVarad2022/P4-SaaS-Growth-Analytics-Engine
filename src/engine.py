# See docs/SCHEMA.md and docs/LOGIC.md for metric definitions.
# Logic Documentation: docs/LOGIC.md | Schema: docs/SCHEMA.md
import pandas as pd
import numpy as np

def compute_churn_risk(users_df, events_df, tickets_df=None, reference_date=None):
    """
    Compute churn risk based on deterministic rules.
    
    Rules:
    - High Risk: No login in > 30 days OR Support ticket satisfaction < 2
    - Medium Risk: No usage of core features in > 14 days
    - Low Risk: Active in last 7 days
    
    Returns:
    - DataFrame with 'churn_risk' column (High, Medium, Low)
    """
    ref_date = pd.to_datetime(reference_date)
    risk_scores = []
    
    # Pre-process events
    events_df['event_timestamp'] = pd.to_datetime(events_df['event_timestamp'])
    
    # Pre-process tickets if provided
    churn_ticket_ids = set()
    if tickets_df is not None and not tickets_df.empty:
         # Filter for satisfaction < 2
         bad_tickets = tickets_df[tickets_df['satisfaction_score'] < 2]
         churn_ticket_ids = set(bad_tickets['customer_id'].unique())

    # Optimize event lookup
    grouped_events = events_df.groupby('customer_id')
    
    for _, user in users_df.iterrows():
        user_id = user['customer_id']
        
        last_login = pd.NaT
        last_feature = pd.NaT
        
        if user_id in grouped_events.groups:
            user_events = grouped_events.get_group(user_id)
            # Find max timestamp for each event type
            # Assuming event_name and event_timestamp columns exist
            # Optimizing further: filter by event type then max
            # But iterating small groups is fast enough
            
            logins = user_events[user_events['event_name'] == 'login']['event_timestamp']
            if not logins.empty:
                last_login = logins.max()
                
            features = user_events[user_events['event_name'] == 'feature_use']['event_timestamp']
            if not features.empty:
                last_feature = features.max()
        
        days_since_login = (ref_date - last_login).days if pd.notna(last_login) else 999
        days_since_feature = (ref_date - last_feature).days if pd.notna(last_feature) else 999
        
        risk = 'Low'
        if days_since_login > 30 or user_id in churn_ticket_ids:
            risk = 'High'
        elif days_since_feature > 14:
            risk = 'Medium'
            
        risk_scores.append({
            'customer_id': user_id,
            'churn_risk': risk,
            'days_since_active': min(days_since_login, days_since_feature)
        })
        
    return pd.DataFrame(risk_scores)
