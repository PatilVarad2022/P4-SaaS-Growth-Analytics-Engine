"""
Export - Produces CSV/Excel outputs and charts
"""

import pandas as pd
import os
from pathlib import Path


def export_outputs(clean_data, simulation_results, kpis, output_dir):
    """
    Export all required outputs to CSV files.
    
    Args:
        clean_data: Cleaned data dictionary
        simulation_results: Simulation results
        kpis: Calculated KPIs
        output_dir: Output directory path
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Base Forecast CSV
    base_forecast = simulation_results['base_forecast'].copy()
    base_forecast['scenario'] = 'base'
    base_forecast.to_csv(output_path / 'base_forecast.csv', index=False)
    
    # 2. Scenario Summary CSV (all three scenarios)
    optimistic = simulation_results['optimistic_forecast'].copy()
    optimistic['scenario'] = 'optimistic'
    
    pessimistic = simulation_results['pessimistic_forecast'].copy()
    pessimistic['scenario'] = 'pessimistic'
    
    scenario_summary = pd.concat([base_forecast, optimistic, pessimistic], ignore_index=True)
    scenario_summary.to_csv(output_path / 'scenario_summary.csv', index=False)
    
    # 3. KPI Snapshot CSV
    kpi_df = pd.DataFrame([kpis])
    kpi_df.to_csv(output_path / 'kpi_snapshot.csv', index=False)
    
    # 4. Customer Metrics (bonus output)
    customer_metrics = clean_data['customer_metrics']
    customer_metrics.to_csv(output_path / 'customer_metrics.csv', index=False)
    
    # 5. Historical MRR (bonus output)
    historical = simulation_results['historical_data'][
        ['month', 'mrr', 'arr', 'active_customers']
    ].copy()
    historical['month'] = historical['month'].astype(str)
    historical.to_csv(output_path / 'historical_mrr.csv', index=False)
    
    # 6. Create summary report
    create_summary_report(kpis, simulation_results, output_path)
    
    print(f"      OK - base_forecast.csv ({len(base_forecast)} rows)")
    print(f"      OK - scenario_summary.csv ({len(scenario_summary)} rows)")
    print(f"      OK - kpi_snapshot.csv (1 row, {len(kpis)} metrics)")
    print(f"      OK - customer_metrics.csv ({len(customer_metrics)} customers)")
    print(f"      OK - historical_mrr.csv ({len(historical)} months)")


def create_summary_report(kpis, simulation_results, output_path):
    """Create a human-readable summary report."""
    
    report_lines = [
        "=" * 70,
        "P4 SaaS Growth Analytics Engine - Summary Report",
        "=" * 70,
        f"Generated: {kpis['snapshot_date']}",
        "",
        "KEY METRICS",
        "-" * 70,
        f"Current MRR:              ${kpis['current_mrr']:,.2f}",
        f"Current ARR:              ${kpis['current_arr']:,.2f}",
        f"Active Customers:         {kpis['active_customers']:,}",
        f"Avg MRR per Customer:     ${kpis['avg_mrr_per_customer']:,.2f}",
        "",
        "GROWTH METRICS",
        "-" * 70,
        f"Monthly MRR Growth:       {kpis['mrr_growth_rate_monthly']:.2f}%",
        f"Projected ARR (12m):      ${kpis['projected_arr_12m']:,.2f}",
        f"YoY ARR Growth:           {kpis['arr_growth_yoy_projected']:.2f}%",
        "",
        "CUSTOMER HEALTH",
        "-" * 70,
        f"Estimated LTV:            ${kpis['estimated_ltv']:,.2f}",
        f"Estimated CAC:            ${kpis['estimated_cac']:,.2f}",
        f"LTV:CAC Ratio:            {kpis['ltv_cac_ratio']:.2f}x",
        f"High Risk Customers:      {kpis['high_risk_customers']} ({kpis['churn_risk_pct']:.1f}%)",
        "",
        "SCENARIOS (12-Month Projection)",
        "-" * 70,
    ]
    
    # Add scenario comparison
    base_arr = simulation_results['base_forecast']['arr'].iloc[-1]
    opt_arr = simulation_results['optimistic_forecast']['arr'].iloc[-1]
    pess_arr = simulation_results['pessimistic_forecast']['arr'].iloc[-1]
    
    report_lines.extend([
        f"Base Case ARR:            ${base_arr:,.2f}",
        f"Optimistic ARR:           ${opt_arr:,.2f} (+{(opt_arr/base_arr - 1)*100:.1f}%)",
        f"Pessimistic ARR:          ${pess_arr:,.2f} ({(pess_arr/base_arr - 1)*100:.1f}%)",
        "",
        "=" * 70,
    ])
    
    report_text = "\n".join(report_lines)
    
    with open(output_path / 'summary_report.txt', 'w') as f:
        f.write(report_text)
    
    print(f"      OK - summary_report.txt")
