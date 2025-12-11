"""
Metrics test - Verifies KPI calculations are accurate
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_loader import load_sample_data
from transform import clean_and_transform, calculate_mrr
from metrics import calculate_kpis
from engine import run_growth_simulation


def test_mrr_calculation():
    """
    Test that MRR is calculated correctly from invoices.
    """
    # Create simple test data
    invoices = pd.DataFrame({
        'invoice_id': ['INV-1', 'INV-2', 'INV-3', 'INV-4'],
        'customer_id': ['C1', 'C2', 'C1', 'C2'],
        'amount': [100, 200, 100, 200],
        'invoice_date': ['2023-01-15', '2023-01-20', '2023-02-15', '2023-02-20']
    })
    invoices['invoice_date'] = pd.to_datetime(invoices['invoice_date'])
    
    subscriptions = pd.DataFrame({
        'subscription_id': ['SUB-1', 'SUB-2'],
        'customer_id': ['C1', 'C2'],
        'start_date': ['2023-01-01', '2023-01-01']
    })
    
    mrr_data = calculate_mrr(invoices, subscriptions)
    
    # Verify MRR for January (100 + 200 = 300)
    jan_mrr = mrr_data[mrr_data['month'] == '2023-01']['mrr'].values[0]
    assert jan_mrr == 300, f"Expected MRR=300 for Jan, got {jan_mrr}"
    
    # Verify ARR is MRR * 12
    jan_arr = mrr_data[mrr_data['month'] == '2023-01']['arr'].values[0]
    assert jan_arr == 3600, f"Expected ARR=3600 for Jan, got {jan_arr}"
    
    print("✓ MRR calculation test passed")


def test_arr_calculation():
    """
    Test that ARR = MRR * 12
    """
    config_path = Path(__file__).parent.parent / "configs" / "default.yaml"
    
    raw_data = load_sample_data()
    clean_data = clean_and_transform(raw_data, str(config_path))
    
    mrr_data = clean_data['mrr_data']
    
    # Check that ARR = MRR * 12 for all months
    for _, row in mrr_data.iterrows():
        expected_arr = row['mrr'] * 12
        actual_arr = row['arr']
        assert abs(actual_arr - expected_arr) < 0.01, \
            f"ARR mismatch: expected {expected_arr}, got {actual_arr}"
    
    print("✓ ARR calculation test passed")


def test_kpi_snapshot_completeness():
    """
    Test that all required KPIs are present in the snapshot.
    """
    config_path = Path(__file__).parent.parent / "configs" / "default.yaml"
    
    raw_data = load_sample_data()
    clean_data = clean_and_transform(raw_data, str(config_path))
    simulation_results = run_growth_simulation(clean_data, str(config_path))
    kpis = calculate_kpis(clean_data, simulation_results, str(config_path))
    
    # Required KPI fields
    required_fields = [
        'snapshot_date',
        'current_mrr',
        'current_arr',
        'active_customers',
        'avg_mrr_per_customer',
        'mrr_growth_rate_monthly',
        'projected_arr_12m',
        'estimated_ltv',
        'estimated_cac',
        'ltv_cac_ratio',
        'churn_risk_pct'
    ]
    
    for field in required_fields:
        assert field in kpis, f"Missing required KPI field: {field}"
    
    # Verify data types and ranges
    assert kpis['current_mrr'] > 0, "MRR should be positive"
    assert kpis['current_arr'] > 0, "ARR should be positive"
    assert kpis['active_customers'] > 0, "Should have active customers"
    assert kpis['ltv_cac_ratio'] > 0, "LTV:CAC ratio should be positive"
    assert 0 <= kpis['churn_risk_pct'] <= 100, "Churn risk % should be 0-100"
    
    print("✓ KPI snapshot completeness test passed")


def test_ltv_calculation():
    """
    Test that LTV is calculated as avg_revenue / churn_rate
    """
    config_path = Path(__file__).parent.parent / "configs" / "default.yaml"
    
    raw_data = load_sample_data()
    clean_data = clean_and_transform(raw_data, str(config_path))
    simulation_results = run_growth_simulation(clean_data, str(config_path))
    kpis = calculate_kpis(clean_data, simulation_results, str(config_path))
    
    # LTV should be positive
    assert kpis['estimated_ltv'] > 0, "LTV should be positive"
    
    # LTV should be greater than avg revenue (since churn rate < 1)
    avg_revenue = kpis['avg_revenue_per_customer']
    assert kpis['estimated_ltv'] > avg_revenue, \
        "LTV should be greater than avg revenue per customer"
    
    print("✓ LTV calculation test passed")


def test_scenario_projections():
    """
    Test that scenario projections produce different outcomes.
    """
    config_path = Path(__file__).parent.parent / "configs" / "default.yaml"
    
    raw_data = load_sample_data()
    clean_data = clean_and_transform(raw_data, str(config_path))
    simulation_results = run_growth_simulation(clean_data, str(config_path))
    
    base_final_arr = simulation_results['base_forecast']['arr'].iloc[-1]
    opt_final_arr = simulation_results['optimistic_forecast']['arr'].iloc[-1]
    pess_final_arr = simulation_results['pessimistic_forecast']['arr'].iloc[-1]
    
    # Optimistic should be higher than base
    assert opt_final_arr > base_final_arr, \
        "Optimistic ARR should be higher than base"
    
    # Pessimistic should be lower than base
    assert pess_final_arr < base_final_arr, \
        "Pessimistic ARR should be lower than base"
    
    # All should be positive
    assert base_final_arr > 0, "Base ARR should be positive"
    assert opt_final_arr > 0, "Optimistic ARR should be positive"
    assert pess_final_arr > 0, "Pessimistic ARR should be positive"
    
    print("✓ Scenario projections test passed")


if __name__ == "__main__":
    test_mrr_calculation()
    test_arr_calculation()
    test_kpi_snapshot_completeness()
    test_ltv_calculation()
    test_scenario_projections()
    print("\n✅ All metrics tests passed!")
