"""
Funnel Analysis - Calculates activation and conversion metrics
"""

import pandas as pd
import numpy as np


def calculate_funnel_metrics(users_df):
    """
    Calculate funnel conversion rates.
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with funnel metrics
    """
    total_users = len(users_df)
    free_users = len(users_df[users_df['initial_plan'] == 'Free'])
    
    # Stage 1: Sign-up to Activated
    activated_users = users_df['activated'].sum()
    activation_rate = activated_users / total_users if total_users > 0 else 0
    
    # Stage 2: Activated to Paid (for Free users)
    free_activated = len(users_df[(users_df['initial_plan'] == 'Free') & (users_df['activated'] == True)])
    converted_to_paid = users_df['converted_to_paid'].sum()
    conversion_rate = converted_to_paid / free_activated if free_activated > 0 else 0
    
    # Stage 3: Paid to Retained (not churned after 30 days)
    paid_users = users_df[users_df['converted_to_paid'] == True]
    retained_paid = len(paid_users[(paid_users['churned'] == False) | 
                                   ((paid_users['churned'] == True) & (paid_users['lifetime_days'] > 30))])
    retention_rate = retained_paid / len(paid_users) if len(paid_users) > 0 else 0
    
    funnel_metrics = pd.DataFrame([{
        'stage': 'Total Sign-ups',
        'users': total_users,
        'conversion_rate': 1.0,
        'cumulative_rate': 1.0
    }, {
        'stage': 'Activated',
        'users': activated_users,
        'conversion_rate': activation_rate,
        'cumulative_rate': activation_rate
    }, {
        'stage': 'Converted to Paid',
        'users': converted_to_paid,
        'conversion_rate': conversion_rate,
        'cumulative_rate': activation_rate * conversion_rate
    }, {
        'stage': 'Retained (30+ days)',
        'users': retained_paid,
        'conversion_rate': retention_rate,
        'cumulative_rate': activation_rate * conversion_rate * retention_rate
    }])
    
    return funnel_metrics


def calculate_conversion_summary(users_df):
    """
    Calculate detailed conversion metrics by channel and plan.
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with conversion summary
    """
    summaries = []
    
    # Overall conversion
    summaries.append({
        'segment': 'Overall',
        'total_users': len(users_df),
        'activated': users_df['activated'].sum(),
        'activation_rate': users_df['activated'].mean(),
        'converted_to_paid': users_df['converted_to_paid'].sum(),
        'conversion_rate': users_df['converted_to_paid'].mean(),
        'churned': users_df['churned'].sum(),
        'churn_rate': users_df['churned'].mean()
    })
    
    # By acquisition channel
    for channel in users_df['acquisition_channel'].unique():
        channel_users = users_df[users_df['acquisition_channel'] == channel]
        summaries.append({
            'segment': f'Channel: {channel}',
            'total_users': len(channel_users),
            'activated': channel_users['activated'].sum(),
            'activation_rate': channel_users['activated'].mean(),
            'converted_to_paid': channel_users['converted_to_paid'].sum(),
            'conversion_rate': channel_users['converted_to_paid'].mean(),
            'churned': channel_users['churned'].sum(),
            'churn_rate': channel_users['churned'].mean()
        })
    
    # By current plan
    for plan in users_df['current_plan'].unique():
        plan_users = users_df[users_df['current_plan'] == plan]
        summaries.append({
            'segment': f'Plan: {plan}',
            'total_users': len(plan_users),
            'activated': plan_users['activated'].sum(),
            'activation_rate': plan_users['activated'].mean(),
            'converted_to_paid': plan_users['converted_to_paid'].sum(),
            'conversion_rate': plan_users['converted_to_paid'].mean(),
            'churned': plan_users['churned'].sum(),
            'churn_rate': plan_users['churned'].mean()
        })
    
    return pd.DataFrame(summaries)


if __name__ == "__main__":
    # Test with sample data
    from user_simulation import generate_user_lifecycle
    
    users = generate_user_lifecycle(1000)
    
    print("\nFunnel Metrics:")
    funnel = calculate_funnel_metrics(users)
    print(funnel)
    
    print("\nConversion Summary:")
    summary = calculate_conversion_summary(users)
    print(summary)
