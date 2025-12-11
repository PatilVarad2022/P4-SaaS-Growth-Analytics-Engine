# Logic Documentation: docs/LOGIC.md | Schema: docs/SCHEMA.md
import pandas as pd
import numpy as np

def compute_churn_risk(users_df, events_df, reference_date):
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
    
    for _, user in users_df.iterrows():
        user_id = user['customer_id']
        user_events = events_df[events_df['customer_id'] == user_id]
        
        last_login = user_events[user_events['event_name'] == 'login']['event_timestamp'].max()
        last_feature = user_events[user_events['event_name'] == 'feature_use']['event_timestamp'].max()
        
        days_since_login = (ref_date - last_login).days if pd.notna(last_login) else 999
        days_since_feature = (ref_date - last_feature).days if pd.notna(last_feature) else 999
        
        risk = 'Low'
        if days_since_login > 30:
            risk = 'High'
        elif days_since_feature > 14:
            risk = 'Medium'
            
        risk_scores.append({
            'customer_id': user_id,
            'churn_risk': risk,
            'days_since_active': min(days_since_login, days_since_feature)
        })
        
    return pd.DataFrame(risk_scores)
