import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pandas as pd
import pytest
from metrics import compute_rfm
from engine import compute_churn_risk

def test_recency_correctness():
    # Setup data
    ref_date = '2024-12-12'
    users = pd.DataFrame({'customer_id': ['U1', 'U2']})
    
    # U1: Transaction on 2024-12-10 (2 days ago), Event on 2024-12-01
    transactions = pd.DataFrame({
        'transaction_id': ['T1'],
        'customer_id': ['U1'],
        'transaction_date': ['2024-12-10'],
        'amount': [100]
    })
    events = pd.DataFrame({
        'event_id': ['E1', 'E2'],
        'customer_id': ['U1', 'U2'],
        'event_name': ['login', 'login'],
        'event_timestamp': ['2024-12-01', '2024-12-11']
    })
    
    # U2: No transaction, Event on 2024-12-11 (1 day ago)
    # Expected: U1 recency = 2 days (from txn), U2 recency = 1 day (from evt)
    
    rfm = compute_rfm(users, transactions, ref_date, events_df=events)
    
    u1_rec = rfm.loc['U1', 'recency_days']
    u2_rec = rfm.loc['U2', 'recency_days']
    
    assert u1_rec == 2, f"U1 recency should be 2, got {u1_rec}"
    assert u2_rec == 1, f"U2 recency should be 1, got {u2_rec}"

def test_churn_rule_correctness():
    # Setup data
    ref_date = '2024-12-12'
    users_df = pd.DataFrame({'customer_id': ['HighRiskUser', 'MedRiskUser', 'LowRiskUser', 'TicketRiskUser']})
    
    events_df = pd.DataFrame([
        # HighRiskUser: Login > 30 days ago
        {'customer_id': 'HighRiskUser', 'event_name': 'login', 'event_timestamp': '2024-11-01'}, # 41 days ago
        {'customer_id': 'HighRiskUser', 'event_name': 'feature_use', 'event_timestamp': '2024-12-10'}, # Recent feature, but NO RECENT LOGIN
        
        # MedRiskUser: Login OK, No Feature Use in 14 days
        {'customer_id': 'MedRiskUser', 'event_name': 'login', 'event_timestamp': '2024-12-10'}, # 2 days ago
        {'customer_id': 'MedRiskUser', 'event_name': 'feature_use', 'event_timestamp': '2024-11-20'}, # 22 days ago
        
        # LowRiskUser: Active in last 7 days (Login + Feature)
        {'customer_id': 'LowRiskUser', 'event_name': 'login', 'event_timestamp': '2024-12-10'}, 
        {'customer_id': 'LowRiskUser', 'event_name': 'feature_use', 'event_timestamp': '2024-12-10'},
        
        # TicketRiskUser: Login OK, but bad ticket
        {'customer_id': 'TicketRiskUser', 'event_name': 'login', 'event_timestamp': '2024-12-10'},
    ])
    
    tickets_df = pd.DataFrame([
        {'customer_id': 'TicketRiskUser', 'satisfaction_score': 1}
    ])
    
    risks = compute_churn_risk(users_df, events_df, tickets_df, ref_date)
    risk_map = risks.set_index('customer_id')['churn_risk']
    
    assert risk_map['HighRiskUser'] == 'High'
    assert risk_map['MedRiskUser'] == 'Medium'
    assert risk_map['LowRiskUser'] == 'Low'
    assert risk_map['TicketRiskUser'] == 'High'
