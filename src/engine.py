"""
Engine - Core simulation and business logic for SaaS growth modeling
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def run_growth_simulation(clean_data, config_path):
    """
    Run growth simulation to project future MRR, churn, and expansion.
    
    Args:
        clean_data: Dictionary of cleaned DataFrames
        config_path: Path to configuration file
        
    Returns:
        dict: Simulation results including forecasts and scenarios
    """
    from data_loader import load_config
    config = load_config(config_path)
    
    mrr_data = clean_data['mrr_data']
    customer_metrics = clean_data['customer_metrics']
    
    # Get historical growth rates
    mrr_data['month_dt'] = mrr_data['month'].dt.to_timestamp()
    mrr_data = mrr_data.sort_values('month_dt')
    
    # Calculate month-over-month growth
    mrr_data['mrr_growth'] = mrr_data['mrr'].pct_change()
    avg_growth_rate = mrr_data['mrr_growth'].mean()
    
    # Project 12 months forward
    last_month = mrr_data['month_dt'].max()
    last_mrr = mrr_data['mrr'].iloc[-1]
    last_customers = mrr_data['active_customers'].iloc[-1]
    
    # Base scenario: continue historical growth
    base_forecast = project_forward(
        start_month=last_month,
        start_mrr=last_mrr,
        start_customers=last_customers,
        growth_rate=avg_growth_rate,
        churn_rate=config.get('base_churn_rate', 0.05),
        months=12
    )
    
    # Optimistic scenario: +50% growth rate, -20% churn
    optimistic_forecast = project_forward(
        start_month=last_month,
        start_mrr=last_mrr,
        start_customers=last_customers,
        growth_rate=avg_growth_rate * 1.5,
        churn_rate=config.get('base_churn_rate', 0.05) * 0.8,
        months=12
    )
    
    # Pessimistic scenario: -50% growth rate, +50% churn
    pessimistic_forecast = project_forward(
        start_month=last_month,
        start_mrr=last_mrr,
        start_customers=last_customers,
        growth_rate=avg_growth_rate * 0.5,
        churn_rate=config.get('base_churn_rate', 0.05) * 1.5,
        months=12
    )
    
    return {
        'base_forecast': base_forecast,
        'optimistic_forecast': optimistic_forecast,
        'pessimistic_forecast': pessimistic_forecast,
        'historical_data': mrr_data,
        'avg_growth_rate': avg_growth_rate,
        'months_projected': 12
    }


def project_forward(start_month, start_mrr, start_customers, growth_rate, churn_rate, months):
    """
    Project MRR forward using growth and churn assumptions.
    
    Returns:
        pd.DataFrame: Forecasted monthly data
    """
    forecast = []
    
    current_mrr = start_mrr
    current_customers = start_customers
    current_month = start_month
    
    for i in range(months):
        current_month = current_month + relativedelta(months=1)
        
        # Apply growth and churn
        new_mrr = current_mrr * (1 + growth_rate)
        churned_customers = int(current_customers * churn_rate)
        new_customers = int(current_customers * growth_rate) + churned_customers
        
        current_customers = current_customers - churned_customers + new_customers
        current_mrr = new_mrr
        
        forecast.append({
            'month': current_month,
            'mrr': round(current_mrr, 2),
            'arr': round(current_mrr * 12, 2),
            'active_customers': current_customers,
            'new_customers': new_customers,
            'churned_customers': churned_customers,
            'net_new_customers': new_customers - churned_customers
        })
    
    return pd.DataFrame(forecast)
