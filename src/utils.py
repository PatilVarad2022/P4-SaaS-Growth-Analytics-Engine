"""
Utility functions for SaaS Analytics Engine
"""

import pandas as pd
import numpy as np
from datetime import datetime


def format_currency(value):
    """Format value as currency."""
    return f"${value:,.2f}"


def format_percentage(value):
    """Format value as percentage."""
    return f"{value*100:.1f}%"


def calculate_growth_rate(current, previous):
    """Calculate growth rate between two values."""
    if previous == 0:
        return 0
    return (current - previous) / previous


def get_month_name(date):
    """Get month name from date."""
    return pd.to_datetime(date).strftime('%B %Y')


def validate_dataframe(df, required_columns):
    """Validate that DataFrame has required columns."""
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True


def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers, returning default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def round_to_nearest(value, nearest=1):
    """Round value to nearest specified number."""
    return round(value / nearest) * nearest


# Plan pricing constants
PLAN_PRICING = {
    'Free': 0,
    'Basic': 49,
    'Pro': 199
}


# Acquisition channel CAC ranges
CHANNEL_CAC = {
    'organic_search': (150, 250),
    'paid_ads': (400, 600),
    'referral': (70, 130),
    'sales_outbound': (650, 950),
    'content_marketing': (100, 200)
}


def get_plan_price(plan_name):
    """Get price for a plan."""
    return PLAN_PRICING.get(plan_name, 0)


def get_channel_cac_range(channel):
    """Get CAC range for acquisition channel."""
    return CHANNEL_CAC.get(channel, (200, 400))
