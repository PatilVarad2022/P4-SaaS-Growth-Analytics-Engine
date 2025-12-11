"""
Unit Economics - CAC and LTV calculations
"""

import pandas as pd
import numpy as np


# Plan pricing
PLAN_PRICING = {
    'Free': 0,
    'Basic': 49,
    'Pro': 199
}


def calculate_unit_economics(users_df):
    """
    Calculate CAC, LTV, and LTV:CAC ratio for each user.
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with unit economics per user
    """
    economics = []
    
    for _, user in users_df.iterrows():
        # CAC is already in the data
        cac = user['cac']
        
        # LTV = Plan price × (lifetime_days / 30)
        monthly_price = PLAN_PRICING.get(user['current_plan'], 0)
        lifetime_months = user['lifetime_days'] / 30.0
        ltv = monthly_price * lifetime_months
        
        # LTV:CAC ratio
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        
        economics.append({
            'user_id': user['user_id'],
            'acquisition_channel': user['acquisition_channel'],
            'current_plan': user['current_plan'],
            'cac': cac,
            'lifetime_days': user['lifetime_days'],
            'lifetime_months': round(lifetime_months, 2),
            'monthly_price': monthly_price,
            'ltv': round(ltv, 2),
            'ltv_cac_ratio': round(ltv_cac_ratio, 2),
            'churned': user['churned']
        })
    
    return pd.DataFrame(economics)


def calculate_unit_economics_summary(economics_df):
    """
    Calculate summary statistics for unit economics.
    
    Args:
        economics_df: DataFrame with unit economics
        
    Returns:
        DataFrame with summary metrics
    """
    summaries = []
    
    # Overall
    summaries.append({
        'segment': 'Overall',
        'users': len(economics_df),
        'avg_cac': economics_df['cac'].mean(),
        'avg_ltv': economics_df['ltv'].mean(),
        'avg_ltv_cac_ratio': economics_df['ltv_cac_ratio'].mean(),
        'median_ltv_cac_ratio': economics_df['ltv_cac_ratio'].median()
    })
    
    # By channel
    for channel in economics_df['acquisition_channel'].unique():
        channel_data = economics_df[economics_df['acquisition_channel'] == channel]
        summaries.append({
            'segment': f'Channel: {channel}',
            'users': len(channel_data),
            'avg_cac': channel_data['cac'].mean(),
            'avg_ltv': channel_data['ltv'].mean(),
            'avg_ltv_cac_ratio': channel_data['ltv_cac_ratio'].mean(),
            'median_ltv_cac_ratio': channel_data['ltv_cac_ratio'].median()
        })
    
    # By plan
    for plan in economics_df['current_plan'].unique():
        plan_data = economics_df[economics_df['current_plan'] == plan]
        summaries.append({
            'segment': f'Plan: {plan}',
            'users': len(plan_data),
            'avg_cac': plan_data['cac'].mean(),
            'avg_ltv': plan_data['ltv'].mean(),
            'avg_ltv_cac_ratio': plan_data['ltv_cac_ratio'].mean(),
            'median_ltv_cac_ratio': plan_data['ltv_cac_ratio'].median()
        })
    
    return pd.DataFrame(summaries)


if __name__ == "__main__":
    from user_simulation import generate_user_lifecycle
    
    users = generate_user_lifecycle(1000)
    
    print("\nUnit Economics (first 10 users):")
    economics = calculate_unit_economics(users)
    print(economics.head(10))
    
    print("\nUnit Economics Summary:")
    summary = calculate_unit_economics_summary(economics)
    print(summary)
