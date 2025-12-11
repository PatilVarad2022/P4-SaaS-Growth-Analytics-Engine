"""
Retention Analysis - Calculates retention rates and cohort analysis
"""

import pandas as pd
import numpy as np
from datetime import timedelta


def calculate_retention_metrics(users_df):
    """
    Calculate retention metrics for each user.
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with retention metrics per user
    """
    retention_data = []
    
    for _, user in users_df.iterrows():
        sign_up = pd.to_datetime(user['sign_up_date'])
        churn = pd.to_datetime(user['churn_date']) if pd.notna(user['churn_date']) else None
        
        # Week 1 retention (7 days)
        week_1_date = sign_up + timedelta(days=7)
        retention_week_1 = not user['churned'] or (churn and churn > week_1_date)
        
        # Week 4 retention (28 days)
        week_4_date = sign_up + timedelta(days=28)
        retention_week_4 = not user['churned'] or (churn and churn > week_4_date)
        
        # Month 3 retention (90 days)
        month_3_date = sign_up + timedelta(days=90)
        retention_month_3 = not user['churned'] or (churn and churn > month_3_date)
        
        retention_data.append({
            'user_id': user['user_id'],
            'sign_up_date': user['sign_up_date'],
            'current_plan': user['current_plan'],
            'retention_week_1': retention_week_1,
            'retention_week_4': retention_week_4,
            'retention_month_3': retention_month_3,
            'lifetime_days': user['lifetime_days'],
            'churned': user['churned']
        })
    
    return pd.DataFrame(retention_data)


def calculate_churn_rate_monthly(users_df):
    """
    Calculate monthly churn rates.
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with monthly churn rates
    """
    # Convert dates
    users_df['sign_up_month'] = pd.to_datetime(users_df['sign_up_date']).dt.to_period('M')
    users_df['churn_month'] = pd.to_datetime(users_df['churn_date']).dt.to_period('M')
    
    # Get all months
    all_months = pd.period_range(
        start=users_df['sign_up_month'].min(),
        end=users_df['sign_up_month'].max() + 12,
        freq='M'
    )
    
    monthly_churn = []
    
    for month in all_months:
        # Active users at start of month
        active_start = len(users_df[
            (users_df['sign_up_month'] <= month) &
            ((users_df['churn_month'].isna()) | (users_df['churn_month'] > month))
        ])
        
        # Churned during month
        churned_in_month = len(users_df[users_df['churn_month'] == month])
        
        # Churn rate
        churn_rate = churned_in_month / active_start if active_start > 0 else 0
        
        monthly_churn.append({
            'month': month.to_timestamp(),
            'active_users_start': active_start,
            'churned_users': churned_in_month,
            'churn_rate_monthly': churn_rate
        })
    
    return pd.DataFrame(monthly_churn)


def generate_cohort_retention_matrix(users_df):
    """
    Generate cohort retention matrix (heatmap data).
    
    Args:
        users_df: DataFrame with user lifecycle data
        
    Returns:
        DataFrame with cohort retention rates
    """
    users_df['cohort_month'] = pd.to_datetime(users_df['sign_up_date']).dt.to_period('M')
    
    cohorts = []
    
    for cohort in sorted(users_df['cohort_month'].unique()):
        cohort_users = users_df[users_df['cohort_month'] == cohort]
        cohort_size = len(cohort_users)
        
        cohort_data = {
            'cohort_month': cohort.to_timestamp(),
            'cohort_size': cohort_size
        }
        
        # Calculate retention for months 0-12
        for month_offset in range(13):
            target_date = cohort.to_timestamp() + pd.DateOffset(months=month_offset)
            
            # Count users still active at target date
            retained = len(cohort_users[
                (pd.to_datetime(cohort_users['sign_up_date']) <= target_date) &
                ((cohort_users['churn_date'].isna()) | 
                 (pd.to_datetime(cohort_users['churn_date']) > target_date))
            ])
            
            retention_rate = retained / cohort_size if cohort_size > 0 else 0
            cohort_data[f'month_{month_offset}'] = retention_rate
        
        cohorts.append(cohort_data)
    
    return pd.DataFrame(cohorts)


if __name__ == "__main__":
    # Test with sample data
    from user_simulation import generate_user_lifecycle
    
    users = generate_user_lifecycle(1000)
    
    print("\nRetention Metrics (first 10 users):")
    retention = calculate_retention_metrics(users)
    print(retention.head(10))
    
    print("\nMonthly Churn Rates:")
    monthly_churn = calculate_churn_rate_monthly(users)
    print(monthly_churn.head(10))
    
    print("\nCohort Retention Matrix:")
    cohort_matrix = generate_cohort_retention_matrix(users)
    print(cohort_matrix.head())
