"""
Metrics - Calculate key SaaS metrics and KPIs
"""

import pandas as pd
import numpy as np
from datetime import datetime


def calculate_kpis(clean_data, simulation_results, config_path):
    """
    Calculate comprehensive SaaS KPIs.
    
    Args:
        clean_data: Dictionary of cleaned data
        simulation_results: Results from simulation engine
        config_path: Path to config file
        
    Returns:
        dict: Dictionary of calculated KPIs
    """
    from data_loader import load_config
    config = load_config(config_path)
    
    historical = simulation_results['historical_data']
    base_forecast = simulation_results['base_forecast']
    customer_metrics = clean_data['customer_metrics']
    
    # Current state KPIs
    current_mrr = historical['mrr'].iloc[-1]
    current_arr = current_mrr * 12
    current_customers = historical['active_customers'].iloc[-1]
    
    # Growth metrics
    mrr_growth_mom = simulation_results['avg_growth_rate']
    projected_arr_12m = base_forecast['arr'].iloc[-1]
    arr_growth_yoy = (projected_arr_12m - current_arr) / current_arr
    
    # Customer metrics
    avg_revenue_per_customer = customer_metrics['total_revenue'].mean()
    high_risk_customers = len(customer_metrics[customer_metrics['churn_risk'] == 'high'])
    churn_risk_pct = high_risk_customers / len(customer_metrics) * 100
    
    # Cohort metrics (simplified)
    ltv_estimate = avg_revenue_per_customer * (1 / config.get('base_churn_rate', 0.05))
    
    # CAC estimate (simplified - from acquisition channel data)
    cac_estimate = config.get('estimated_cac', 500)
    ltv_cac_ratio = ltv_estimate / cac_estimate if cac_estimate > 0 else 0
    
    # Compile all KPIs
    kpis = {
        'snapshot_date': datetime.now().strftime('%Y-%m-%d'),
        'current_mrr': round(current_mrr, 2),
        'current_arr': round(current_arr, 2),
        'active_customers': int(current_customers),
        'avg_mrr_per_customer': round(current_mrr / current_customers, 2),
        'mrr_growth_rate_monthly': round(mrr_growth_mom * 100, 2),
        'projected_arr_12m': round(projected_arr_12m, 2),
        'arr_growth_yoy_projected': round(arr_growth_yoy * 100, 2),
        'avg_revenue_per_customer': round(avg_revenue_per_customer, 2),
        'estimated_ltv': round(ltv_estimate, 2),
        'estimated_cac': cac_estimate,
        'ltv_cac_ratio': round(ltv_cac_ratio, 2),
        'high_risk_customers': high_risk_customers,
        'churn_risk_pct': round(churn_risk_pct, 2),
        'total_customers_analyzed': len(customer_metrics)
    }
    
    return kpis


def calculate_cohort_retention(subscriptions, invoices):
    """
    Calculate cohort-based retention rates.
    
    Returns:
        pd.DataFrame: Retention matrix by cohort
    """
    # Extract cohort month from subscription start date
    subscriptions['cohort_month'] = pd.to_datetime(
        subscriptions['start_date']
    ).dt.to_period('M')
    
    # Calculate months since start for each subscription
    subscriptions['months_active'] = (
        pd.Timestamp.now() - pd.to_datetime(subscriptions['start_date'])
    ).dt.days // 30
    
    # Build retention matrix
    cohort_data = subscriptions.groupby(['cohort_month', 'months_active']).size().reset_index()
    cohort_data.columns = ['cohort_month', 'months_active', 'customers']
    
    # Calculate retention rate
    cohort_sizes = subscriptions.groupby('cohort_month').size().reset_index()
    cohort_sizes.columns = ['cohort_month', 'cohort_size']
    
    cohort_data = cohort_data.merge(cohort_sizes, on='cohort_month')
    cohort_data['retention_rate'] = cohort_data['customers'] / cohort_data['cohort_size']
    
    return cohort_data
