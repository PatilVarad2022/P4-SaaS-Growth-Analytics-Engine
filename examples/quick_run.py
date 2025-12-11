"""
Quick Run Example - Demonstrates the SaaS Analytics Engine

This script shows how to use the engine in just a few lines.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from user_simulation import generate_user_lifecycle
from funnel import calculate_funnel_metrics
from revenue import calculate_revenue_metrics
from unit_economics import calculate_unit_economics_summary

# Generate 1000 users for quick demo
print("Generating 1000 sample users...")
users = generate_user_lifecycle(num_users=1000)

# Calculate funnel
print("\nFunnel Metrics:")
funnel = calculate_funnel_metrics(users)
print(funnel)

# Calculate revenue
print("\nRevenue Metrics (last 6 months):")
revenue = calculate_revenue_metrics(users)
print(revenue.tail(6))

# Calculate unit economics
print("\nUnit Economics Summary:")
economics = calculate_unit_economics_summary(calculate_unit_economics(users))
print(economics)

print("\n✓ Quick demo complete!")
print("For full analysis with 10,000 users, run: python run_full_analysis.py")
