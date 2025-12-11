"""
User Lifecycle Simulation - Generates 10,000+ user records with complete lifecycle
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Set seed for reproducibility
np.random.seed(42)


def generate_user_lifecycle(num_users=10000, start_date='2022-01-01', end_date='2024-12-31'):
    """
    Generate complete user lifecycle data.
    
    Args:
        num_users: Number of users to generate
        start_date: Simulation start date
        end_date: Simulation end date
        
    Returns:
        DataFrame with user lifecycle data
    """
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    total_days = (end - start).days
    
    users = []
    
    # Acquisition channels with weights
    channels = ['organic_search', 'paid_ads', 'referral', 'sales_outbound', 'content_marketing']
    channel_weights = [0.30, 0.25, 0.20, 0.15, 0.10]
    
    # Plans with conversion rates
    plans = ['Free', 'Basic', 'Pro']
    
    for i in range(num_users):
        # Sign-up date (weighted towards recent dates)
        days_offset = int(np.random.beta(2, 5) * total_days)
        sign_up_date = start + timedelta(days=days_offset)
        
        # Acquisition channel
        channel = np.random.choice(channels, p=channel_weights)
        
        # Initial plan (80% start on Free)
        if np.random.random() < 0.80:
            initial_plan = 'Free'
        elif np.random.random() < 0.70:
            initial_plan = 'Basic'
        else:
            initial_plan = 'Pro'
        
        current_plan = initial_plan
        
        # Activation (did they use the product?)
        activated = np.random.random() < 0.65  # 65% activation rate
        
        # Conversion to paid (if started Free)
        converted_to_paid = False
        conversion_date = None
        if initial_plan == 'Free' and activated:
            if np.random.random() < 0.25:  # 25% conversion rate
                converted_to_paid = True
                # Convert within 30 days typically
                days_to_convert = int(np.random.exponential(15))
                conversion_date = sign_up_date + timedelta(days=days_to_convert)
                current_plan = 'Basic' if np.random.random() < 0.70 else 'Pro'
        
        # Upgrades/downgrades
        upgrade_events = []
        downgrade_events = []
        
        if converted_to_paid:
            # Chance of upgrade
            if current_plan == 'Basic' and np.random.random() < 0.20:
                upgrade_date = conversion_date + timedelta(days=int(np.random.exponential(60)))
                if upgrade_date < end:
                    upgrade_events.append({
                        'date': upgrade_date,
                        'from_plan': 'Basic',
                        'to_plan': 'Pro'
                    })
                    current_plan = 'Pro'
            
            # Chance of downgrade
            if current_plan == 'Pro' and np.random.random() < 0.10:
                downgrade_date = conversion_date + timedelta(days=int(np.random.exponential(90)))
                if downgrade_date < end:
                    downgrade_events.append({
                        'date': downgrade_date,
                        'from_plan': 'Pro',
                        'to_plan': 'Basic'
                    })
                    current_plan = 'Basic'
        
        # Churn
        churned = False
        churn_date = None
        lifetime_days = (end - sign_up_date).days
        
        # Churn probability based on plan and activation
        if not activated:
            churn_prob = 0.80  # High churn if not activated
            avg_lifetime = 7
        elif current_plan == 'Free':
            churn_prob = 0.60
            avg_lifetime = 45
        elif current_plan == 'Basic':
            churn_prob = 0.30
            avg_lifetime = 180
        else:  # Pro
            churn_prob = 0.15
            avg_lifetime = 365
        
        if np.random.random() < churn_prob:
            churned = True
            days_to_churn = int(np.random.exponential(avg_lifetime))
            churn_date = sign_up_date + timedelta(days=days_to_churn)
            if churn_date > end:
                churn_date = None
                churned = False
            else:
                lifetime_days = (churn_date - sign_up_date).days
        
        # CAC (varies by channel)
        cac_by_channel = {
            'organic_search': np.random.normal(200, 50),
            'paid_ads': np.random.normal(500, 100),
            'referral': np.random.normal(100, 30),
            'sales_outbound': np.random.normal(800, 150),
            'content_marketing': np.random.normal(150, 40)
        }
        cac = max(0, cac_by_channel[channel])
        
        users.append({
            'user_id': f'U{i+1:06d}',
            'sign_up_date': sign_up_date,
            'acquisition_channel': channel,
            'initial_plan': initial_plan,
            'current_plan': current_plan,
            'activated': activated,
            'converted_to_paid': converted_to_paid,
            'conversion_date': conversion_date,
            'num_upgrades': len(upgrade_events),
            'num_downgrades': len(downgrade_events),
            'churned': churned,
            'churn_date': churn_date,
            'lifetime_days': lifetime_days,
            'cac': round(cac, 2)
        })
    
    df = pd.DataFrame(users)
    
    print(f"Generated {len(df)} users")
    print(f"Activated: {df['activated'].sum()} ({df['activated'].mean()*100:.1f}%)")
    print(f"Converted to paid: {df['converted_to_paid'].sum()} ({df['converted_to_paid'].mean()*100:.1f}%)")
    print(f"Churned: {df['churned'].sum()} ({df['churned'].mean()*100:.1f}%)")
    
    return df


if __name__ == "__main__":
    # Test generation
    users = generate_user_lifecycle(10000)
    print("\nSample users:")
    print(users.head(10))
    print("\nPlan distribution:")
    print(users['current_plan'].value_counts())
