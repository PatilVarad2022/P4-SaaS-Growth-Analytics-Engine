#!/usr/bin/env python3
"""
Main Runner - Generates all SaaS analytics outputs

Usage:
    python run_full_analysis.py
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from user_simulation import generate_user_lifecycle
from funnel import calculate_funnel_metrics, calculate_conversion_summary
from retention import calculate_retention_metrics, calculate_churn_rate_monthly, generate_cohort_retention_matrix
from revenue import calculate_revenue_metrics, calculate_mrr_bridge, calculate_net_revenue_retention
from unit_economics import calculate_unit_economics, calculate_unit_economics_summary


def main():
    print("=" * 70)
    print("P4 SaaS Growth Analytics Engine - Full Analysis")
    print("=" * 70)
    
    # Create outputs directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Step 1: Generate user lifecycle data
    print("\n[1/7] Generating 10,000+ user lifecycle data...")
    users = generate_user_lifecycle(num_users=10000)
    
    # Save sample users
    users.head(10).to_csv(output_dir / "sample_10_users.csv", index=False)
    print(f"      OK - Generated {len(users)} users")
    
    # Step 2: Calculate funnel metrics
    print("\n[2/7] Calculating funnel metrics...")
    funnel_metrics = calculate_funnel_metrics(users)
    funnel_metrics.to_csv(output_dir / "funnel_metrics.csv", index=False)
    
    conversion_summary = calculate_conversion_summary(users)
    conversion_summary.to_csv(output_dir / "conversion_summary.csv", index=False)
    print("      OK - Funnel metrics calculated")
    
    # Step 3: Calculate retention metrics
    print("\n[3/7] Calculating retention and churn...")
    retention_metrics = calculate_retention_metrics(users)
    
    monthly_churn = calculate_churn_rate_monthly(users)
    monthly_churn.to_csv(output_dir / "monthly_churn.csv", index=False)
    
    cohort_retention = generate_cohort_retention_matrix(users)
    cohort_retention.to_csv(output_dir / "cohort_retention.csv", index=False)
    print("      OK - Retention metrics calculated")
    
    # Step 4: Calculate revenue metrics
    print("\n[4/7] Calculating revenue metrics...")
    revenue_metrics = calculate_revenue_metrics(users)
    revenue_metrics.to_csv(output_dir / "revenue_summary.csv", index=False)
    
    mrr_bridge = calculate_mrr_bridge(users)
    mrr_bridge.to_csv(output_dir / "mrr_bridge.csv", index=False)
    
    nrr = calculate_net_revenue_retention(users)
    nrr.to_csv(output_dir / "net_revenue_retention.csv", index=False)
    print("      OK - Revenue metrics calculated")
    
    # Step 5: Calculate unit economics
    print("\n[5/7] Calculating unit economics...")
    economics = calculate_unit_economics(users)
    economics_summary = calculate_unit_economics_summary(economics)
    economics_summary.to_csv(output_dir / "unit_economics.csv", index=False)
    print("      OK - Unit economics calculated")
    
    # Step 6: Generate scenarios
    print("\n[6/7] Running scenario analysis...")
    scenarios = generate_scenarios(users, revenue_metrics)
    scenarios.to_csv(output_dir / "scenarios_summary.csv", index=False)
    print("      OK - 6 scenarios generated")
    
    # Step 7: Generate summary report
    print("\n[7/7] Generating summary report...")
    generate_summary_report(users, funnel_metrics, revenue_metrics, economics_summary, output_dir)
    print("      OK - Summary report generated")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUCCESS! Full analysis completed.")
    print("=" * 70)
    print("\nGenerated files:")
    print(f"  • sample_10_users.csv")
    print(f"  • funnel_metrics.csv")
    print(f"  • conversion_summary.csv")
    print(f"  • cohort_retention.csv")
    print(f"  • monthly_churn.csv")
    print(f"  • revenue_summary.csv")
    print(f"  • mrr_bridge.csv")
    print(f"  • net_revenue_retention.csv")
    print(f"  • unit_economics.csv")
    print(f"  • scenarios_summary.csv")
    print(f"  • full_analysis_summary.txt")
    print("=" * 70)
    
    return 0


def generate_scenarios(users_df, base_revenue):
    """Generate 6 scenario projections."""
    scenarios = []
    
    # Get latest metrics
    latest = base_revenue.iloc[-1]
    base_mrr = latest['mrr']
    base_users = latest['active_users']
    base_churn = users_df['churned'].mean()
    base_conversion = users_df['converted_to_paid'].mean()
    
    # Scenario definitions
    scenario_configs = [
        {'name': 'Base Case', 'churn_mult': 1.0, 'growth_mult': 1.0, 'cac_mult': 1.0, 'conversion_mult': 1.0, 'price_mult': 1.0},
        {'name': 'High Churn (+20%)', 'churn_mult': 1.2, 'growth_mult': 1.0, 'cac_mult': 1.0, 'conversion_mult': 1.0, 'price_mult': 1.0},
        {'name': 'Reduced Churn (-15%)', 'churn_mult': 0.85, 'growth_mult': 1.0, 'cac_mult': 1.0, 'conversion_mult': 1.0, 'price_mult': 1.0},
        {'name': 'Increased Marketing (+25% CAC)', 'churn_mult': 1.0, 'growth_mult': 1.15, 'cac_mult': 1.25, 'conversion_mult': 1.0, 'price_mult': 1.0},
        {'name': 'Improved Conversion (+10%)', 'churn_mult': 1.0, 'growth_mult': 1.0, 'cac_mult': 1.0, 'conversion_mult': 1.10, 'price_mult': 1.0},
        {'name': 'Pricing Change (+15% ARPU)', 'churn_mult': 1.0, 'growth_mult': 1.0, 'cac_mult': 1.0, 'conversion_mult': 1.0, 'price_mult': 1.15},
    ]
    
    for config in scenario_configs:
        # Project 12 months
        current_mrr = base_mrr
        current_users = base_users
        
        for month in range(1, 13):
            # Apply scenario modifiers
            monthly_churn_rate = base_churn * config['churn_mult']
            growth_rate = 0.05 * config['growth_mult']  # 5% base growth
            
            # Calculate changes
            churned_users = int(current_users * monthly_churn_rate)
            new_users = int(current_users * growth_rate)
            current_users = current_users - churned_users + new_users
            
            # MRR changes
            current_mrr = current_mrr * (1 + growth_rate - monthly_churn_rate) * config['price_mult']
            
            # LTV:CAC (simplified)
            avg_ltv = current_mrr / current_users * 12 if current_users > 0 else 0
            avg_cac = 300 * config['cac_mult']
            ltv_cac = avg_ltv / avg_cac if avg_cac > 0 else 0
            
            scenarios.append({
                'scenario': config['name'],
                'month': month,
                'mrr': round(current_mrr, 2),
                'arr': round(current_mrr * 12, 2),
                'users': current_users,
                'churn_rate': monthly_churn_rate,
                'ltv_cac_ratio': round(ltv_cac, 2),
                'net_revenue_impact': round(current_mrr - base_mrr, 2)
            })
    
    return pd.DataFrame(scenarios)


def generate_summary_report(users, funnel, revenue, economics, output_dir):
    """Generate human-readable summary report."""
    
    latest_revenue = revenue.iloc[-1]
    
    report = f"""
{'=' * 70}
P4 SaaS Growth Analytics Engine - Full Analysis Summary
{'=' * 70}
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

USER BASE
{'-' * 70}
Total Users Generated:        {len(users):,}
Activated Users:              {users['activated'].sum():,} ({users['activated'].mean()*100:.1f}%)
Converted to Paid:            {users['converted_to_paid'].sum():,} ({users['converted_to_paid'].mean()*100:.1f}%)
Churned Users:                {users['churned'].sum():,} ({users['churned'].mean()*100:.1f}%)

FUNNEL METRICS
{'-' * 70}
Sign-up to Activated:         {funnel.iloc[1]['conversion_rate']*100:.1f}%
Activated to Paid:            {funnel.iloc[2]['conversion_rate']*100:.1f}%
Paid to Retained (30+ days):  {funnel.iloc[3]['conversion_rate']*100:.1f}%

CURRENT REVENUE (Latest Month)
{'-' * 70}
MRR:                          ${latest_revenue['mrr']:,.2f}
ARR:                          ${latest_revenue['arr']:,.2f}
Active Users:                 {latest_revenue['active_users']:,}
Paying Users:                 {latest_revenue['paying_users']:,}
ARPU:                         ${latest_revenue['arpu']:.2f}
ARPPU:                        ${latest_revenue['arppu']:.2f}

UNIT ECONOMICS
{'-' * 70}
Average CAC:                  ${economics.iloc[0]['avg_cac']:.2f}
Average LTV:                  ${economics.iloc[0]['avg_ltv']:.2f}
Average LTV:CAC Ratio:        {economics.iloc[0]['avg_ltv_cac_ratio']:.2f}x
Median LTV:CAC Ratio:         {economics.iloc[0]['median_ltv_cac_ratio']:.2f}x

PLAN DISTRIBUTION
{'-' * 70}
Free:                         {len(users[users['current_plan']=='Free']):,} ({len(users[users['current_plan']=='Free'])/len(users)*100:.1f}%)
Basic:                        {len(users[users['current_plan']=='Basic']):,} ({len(users[users['current_plan']=='Basic'])/len(users)*100:.1f}%)
Pro:                          {len(users[users['current_plan']=='Pro']):,} ({len(users[users['current_plan']=='Pro'])/len(users)*100:.1f}%)

{'=' * 70}
"""
    
    with open(output_dir / "full_analysis_summary.txt", 'w') as f:
        f.write(report)
    
    # Don't print to console to avoid encoding issues
    # print(report)


if __name__ == "__main__":
    sys.exit(main())
