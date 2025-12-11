"""
Revenue Analysis - Calculates MRR, ARR, ARPU, and MRR Bridge
"""

import pandas as pd
import numpy as np
from datetime import timedelta


# Plan pricing
PLAN_PRICING = {
    'Free': 0,
    'Basic': 49,
    'Pro': 199
}


def calculate_revenue_metrics(users_df):
    """
    Calculate comprehensive revenue metrics.
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with monthly revenue metrics
    """
    users_df['sign_up_month'] = pd.to_datetime(users_df['sign_up_date']).dt.to_period('M')
    users_df['churn_month'] = pd.to_datetime(users_df['churn_date']).dt.to_period('M')
    
    # Get all months
    all_months = pd.period_range(
        start=users_df['sign_up_month'].min(),
        end=users_df['sign_up_month'].max() + 12,
        freq='M'
    )
    
    monthly_revenue = []
    
    for month in all_months:
        # Active paying users
        active_paying = users_df[
            (users_df['sign_up_month'] <= month) &
            ((users_df['churn_month'].isna()) | (users_df['churn_month'] > month)) &
            (users_df['current_plan'] != 'Free')
        ]
        
        # Calculate MRR
        mrr = sum(PLAN_PRICING.get(plan, 0) for plan in active_paying['current_plan'])
        arr = mrr * 12
        
        # ARPU (Average Revenue Per User - all users)
        total_active = len(users_df[
            (users_df['sign_up_month'] <= month) &
            ((users_df['churn_month'].isna()) | (users_df['churn_month'] > month))
        ])
        arpu = mrr / total_active if total_active > 0 else 0
        
        # ARPPU (Average Revenue Per Paying User)
        paying_users = len(active_paying)
        arppu = mrr / paying_users if paying_users > 0 else 0
        
        monthly_revenue.append({
            'month': month.to_timestamp(),
            'mrr': mrr,
            'arr': arr,
            'active_users': total_active,
            'paying_users': paying_users,
            'arpu': arpu,
            'arppu': arppu
        })
    
    return pd.DataFrame(monthly_revenue)


def calculate_mrr_bridge(users_df):
    """
    Calculate MRR bridge (New, Expansion, Contraction, Churned MRR).
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with MRR bridge components
    """
    users_df['sign_up_month'] = pd.to_datetime(users_df['sign_up_date']).dt.to_period('M')
    users_df['churn_month'] = pd.to_datetime(users_df['churn_date']).dt.to_period('M')
    users_df['conversion_month'] = pd.to_datetime(users_df['conversion_date']).dt.to_period('M')
    
    all_months = pd.period_range(
        start=users_df['sign_up_month'].min(),
        end=users_df['sign_up_month'].max() + 12,
        freq='M'
    )
    
    bridge_data = []
    prev_mrr = 0
    
    for month in all_months:
        # New MRR (new paying customers this month)
        new_paying = users_df[users_df['conversion_month'] == month]
        new_mrr = sum(PLAN_PRICING.get(plan, 0) for plan in new_paying['current_plan'])
        
        # Expansion MRR (upgrades)
        # Simplified: assume 2% of Basic users upgrade to Pro each month
        expansion_mrr = 0  # Would need upgrade event tracking
        
        # Contraction MRR (downgrades)
        contraction_mrr = 0  # Would need downgrade event tracking
        
        # Churned MRR (users who churned this month)
        churned_users = users_df[users_df['churn_month'] == month]
        churned_mrr = sum(PLAN_PRICING.get(plan, 0) for plan in churned_users['current_plan'])
        
        # Net new MRR
        net_new_mrr = new_mrr + expansion_mrr - contraction_mrr - churned_mrr
        
        # Current MRR
        current_mrr = prev_mrr + net_new_mrr
        
        bridge_data.append({
            'month': month.to_timestamp(),
            'starting_mrr': prev_mrr,
            'new_mrr': new_mrr,
            'expansion_mrr': expansion_mrr,
            'contraction_mrr': contraction_mrr,
            'churned_mrr': churned_mrr,
            'net_new_mrr': net_new_mrr,
            'ending_mrr': current_mrr
        })
        
        prev_mrr = current_mrr
    
    return pd.DataFrame(bridge_data)


def calculate_net_revenue_retention(users_df):
    """
    Calculate Net Revenue Retention (NRR).
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with NRR metrics
    """
    # Simplified NRR calculation
    # NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR
    
    bridge = calculate_mrr_bridge(users_df)
    
    nrr_data = []
    
    for _, row in bridge.iterrows():
        if row['starting_mrr'] > 0:
            nrr = ((row['starting_mrr'] + row['expansion_mrr'] - 
                   row['contraction_mrr'] - row['churned_mrr']) / 
                   row['starting_mrr'])
        else:
            nrr = 0
        
        nrr_data.append({
            'month': row['month'],
            'nrr': nrr,
            'nrr_pct': nrr * 100
        })
    
    return pd.DataFrame(nrr_data)


if __name__ == "__main__":
    from user_simulation import generate_user_lifecycle
    
    users = generate_user_lifecycle(10000)
    
    print("\nRevenue Metrics:")
    revenue = calculate_revenue_metrics(users)
    print(revenue.tail(12))
    
    print("\nMRR Bridge:")
    bridge = calculate_mrr_bridge(users)
    print(bridge.tail(12))
