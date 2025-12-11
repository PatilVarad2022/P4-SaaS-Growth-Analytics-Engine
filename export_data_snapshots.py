"""
Export synthetic dataset snapshots from user_simulation.py

This script generates and exports raw CSV files for Power BI and external analysis.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from user_simulation import generate_user_lifecycle

# Set seed for reproducibility
np.random.seed(42)

def export_raw_snapshots():
    """Export raw data snapshots to data/raw_sample/"""
    
    print("Generating 10,000 users...")
    users = generate_user_lifecycle(num_users=10000, start_date='2022-01-01', end_date='2024-12-31')
    
    # Create directory
    data_dir = Path("data/raw_sample")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Export customers.csv
    customers = users[['user_id', 'sign_up_date', 'acquisition_channel', 'initial_plan', 'activated']].copy()
    customers.columns = ['customer_id', 'signup_date', 'acquisition_source', 'initial_plan', 'activated']
    customers['country'] = np.random.choice(['US', 'UK', 'CA', 'AU', 'DE'], size=len(customers))
    customers.to_csv(data_dir / 'customers.csv', index=False)
    print(f"✓ Exported customers.csv ({len(customers)} rows)")
    
    # 2. Generate and export transactions.csv
    transactions = []
    transaction_id = 1
    
    for _, user in users.iterrows():
        if user['converted_to_paid']:
            # Generate monthly transactions
            start = pd.to_datetime(user['conversion_date']) if pd.notna(user['conversion_date']) else pd.to_datetime(user['sign_up_date'])
            end = pd.to_datetime(user['churn_date']) if pd.notna(user['churn_date']) else pd.Timestamp('2024-12-31')
            
            # Monthly transactions
            current = start
            while current <= end:
                plan_prices = {'Free': 0, 'Basic': 49, 'Pro': 199}
                amount = plan_prices.get(user['current_plan'], 0)
                
                if amount > 0:  # Only paid plans
                    transactions.append({
                        'transaction_id': f'TXN{transaction_id:08d}',
                        'customer_id': user['user_id'],
                        'transaction_date': current,
                        'amount': amount,
                        'currency': 'USD',
                        'invoice_status': 'paid'
                    })
                    transaction_id += 1
                
                current += pd.DateOffset(months=1)
    
    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv(data_dir / 'transactions.csv', index=False)
    print(f"✓ Exported transactions.csv ({len(transactions_df)} rows)")
    
    # 3. Export subscriptions.csv
    subscriptions = []
    for _, user in users.iterrows():
        if user['converted_to_paid']:
            subscriptions.append({
                'subscription_id': f'SUB{user["user_id"][1:]}',
                'customer_id': user['user_id'],
                'start_date': user['conversion_date'] if pd.notna(user['conversion_date']) else user['sign_up_date'],
                'end_date': user['churn_date'] if user['churned'] else None,
                'status': 'churned' if user['churned'] else 'active',
                'plan_price': {'Free': 0, 'Basic': 49, 'Pro': 199}.get(user['current_plan'], 0)
            })
    
    subscriptions_df = pd.DataFrame(subscriptions)
    subscriptions_df.to_csv(data_dir / 'subscriptions.csv', index=False)
    print(f"✓ Exported subscriptions.csv ({len(subscriptions_df)} rows)")
    
    # 4. Generate and export events.csv
    events = []
    event_id = 1
    event_types = ['login', 'feature_use', 'page_view', 'export_data', 'invite_sent']
    
    for _, user in users.iterrows():
        if user['activated']:
            # Generate 5-20 events per activated user
            num_events = np.random.randint(5, 21)
            start = pd.to_datetime(user['sign_up_date'])
            end = pd.to_datetime(user['churn_date']) if pd.notna(user['churn_date']) else pd.Timestamp('2024-12-31')
            
            for _ in range(num_events):
                event_date = start + pd.Timedelta(days=np.random.randint(0, (end - start).days + 1))
                events.append({
                    'event_id': f'EVT{event_id:08d}',
                    'customer_id': user['user_id'],
                    'event_name': np.random.choice(event_types),
                    'event_timestamp': event_date
                })
                event_id += 1
    
    events_df = pd.DataFrame(events)
    events_df.to_csv(data_dir / 'events.csv', index=False)
    print(f"✓ Exported events.csv ({len(events_df)} rows)")
    
    # 5. Generate and export support_tickets.csv
    tickets = []
    ticket_id = 1
    
    for _, user in users.iterrows():
        # 20% of users create support tickets
        if np.random.random() < 0.20:
            num_tickets = np.random.randint(1, 4)
            start = pd.to_datetime(user['sign_up_date'])
            end = pd.to_datetime(user['churn_date']) if pd.notna(user['churn_date']) else pd.Timestamp('2024-12-31')
            
            for _ in range(num_tickets):
                created = start + pd.Timedelta(days=np.random.randint(0, (end - start).days + 1))
                closed = created + pd.Timedelta(days=np.random.randint(1, 8))
                
                tickets.append({
                    'ticket_id': f'TKT{ticket_id:06d}',
                    'customer_id': user['user_id'],
                    'created_at': created,
                    'closed_at': closed if closed <= end else None,
                    'status': 'closed' if closed <= end else 'open',
                    'satisfaction_score': np.random.randint(1, 6) if closed <= end else None
                })
                ticket_id += 1
    
    tickets_df = pd.DataFrame(tickets)
    tickets_df.to_csv(data_dir / 'support_tickets.csv', index=False)
    print(f"✓ Exported support_tickets.csv ({len(tickets_df)} rows)")
    
    print(f"\n✓ All snapshots exported to {data_dir}/")
    print(f"  Total customers: {len(customers):,}")
    print(f"  Total transactions: {len(transactions_df):,}")
    print(f"  Total subscriptions: {len(subscriptions_df):,}")
    print(f"  Total events: {len(events_df):,}")
    print(f"  Total support tickets: {len(tickets_df):,}")


if __name__ == "__main__":
    export_raw_snapshots()
