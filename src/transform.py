"""
Transform - Data cleaning and transformation logic
"""

import pandas as pd
import numpy as np
from datetime import datetime
from data_loader import load_config


def clean_and_transform(raw_data, config_path):
    """
    Clean and transform raw data for analytics.
    
    Args:
        raw_data: Dictionary of raw DataFrames
        config_path: Path to configuration file
        
    Returns:
        dict: Dictionary of cleaned DataFrames
    """
    config = load_config(config_path)
    
    customers = raw_data['customers'].copy()
    subscriptions = raw_data['subscriptions'].copy()
    invoices = raw_data['invoices'].copy()
    events = raw_data['events'].copy()
    
    # Parse dates
    subscriptions['start_date'] = pd.to_datetime(subscriptions['start_date'])
    if 'end_date' in subscriptions.columns:
        subscriptions['end_date'] = pd.to_datetime(subscriptions['end_date'], errors='coerce')
    
    invoices['invoice_date'] = pd.to_datetime(invoices['invoice_date'])
    events['event_date'] = pd.to_datetime(events['event_date'])
    
    # Calculate derived fields
    subscriptions['is_active'] = subscriptions['status'] == 'active'
    subscriptions['tenure_days'] = (
        pd.Timestamp.now() - subscriptions['start_date']
    ).dt.days
    
    # Calculate MRR from invoices
    mrr_data = calculate_mrr(invoices, subscriptions)
    
    # Calculate customer metrics
    customer_metrics = calculate_customer_metrics(
        customers, subscriptions, invoices, events, config
    )
    
    return {
        'customers': customers,
        'subscriptions': subscriptions,
        'invoices': invoices,
        'events': events,
        'mrr_data': mrr_data,
        'customer_metrics': customer_metrics,
        'config': config
    }


def calculate_mrr(invoices, subscriptions):
    """Calculate Monthly Recurring Revenue from invoices."""
    # Group by month
    invoices['month'] = invoices['invoice_date'].dt.to_period('M')
    
    mrr_by_month = invoices.groupby('month').agg({
        'amount': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    mrr_by_month.columns = ['month', 'mrr', 'active_customers']
    mrr_by_month['arr'] = mrr_by_month['mrr'] * 12
    
    return mrr_by_month


def calculate_customer_metrics(customers, subscriptions, invoices, events, config):
    """Calculate per-customer metrics (LTV, churn risk, etc)."""
    
    # Calculate total revenue per customer
    customer_revenue = invoices.groupby('customer_id')['amount'].sum().reset_index()
    customer_revenue.columns = ['customer_id', 'total_revenue']
    
    # Calculate event activity scores
    event_weights = config.get('activity_weights', {
        'login': 1,
        'feature_use': 2,
        'support_ticket': -5
    })
    
    events['weight'] = events['event_type'].map(event_weights).fillna(0)
    activity_scores = events.groupby('customer_id')['weight'].sum().reset_index()
    activity_scores.columns = ['customer_id', 'activity_score']
    
    # Merge all metrics
    metrics = customers[['customer_id', 'region', 'acquisition_channel']].copy()
    metrics = metrics.merge(customer_revenue, on='customer_id', how='left')
    metrics = metrics.merge(activity_scores, on='customer_id', how='left')
    
    metrics['total_revenue'] = metrics['total_revenue'].fillna(0)
    metrics['activity_score'] = metrics['activity_score'].fillna(0)
    
    # Calculate churn risk (simple heuristic)
    metrics['churn_risk'] = np.where(
        metrics['activity_score'] < 0,
        'high',
        np.where(metrics['activity_score'] < 5, 'medium', 'low')
    )
    
    return metrics
