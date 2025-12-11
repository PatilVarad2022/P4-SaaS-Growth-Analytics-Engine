"""
Smoke test for verified values - prevents claim drift
"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_verified_kpi_values():
    """
    Test that KPI values match verified outputs from 2025-12-12 run.
    This prevents accidental claim drift when code changes.
    """
    verified_path = Path(__file__).parent.parent / "outputs_verified" / "2025-12-12"
    current_path = Path(__file__).parent.parent / "outputs"
    
    # Load verified KPI snapshot
    verified_kpis = pd.read_csv(verified_path / "kpi_snapshot.csv")
    
    # Load current KPI snapshot (from last run)
    if not (current_path / "kpi_snapshot.csv").exists():
        # Run pipeline first
        import subprocess
        subprocess.run([sys.executable, "run.py"], check=True, cwd=Path(__file__).parent.parent)
    
    current_kpis = pd.read_csv(current_path / "kpi_snapshot.csv")
    
    # Define tolerances for floating point comparison
    tolerance = 0.01  # 1 cent tolerance for currency
    pct_tolerance = 0.1  # 0.1% tolerance for percentages
    
    # Test key metrics
    assert abs(current_kpis['current_mrr'].values[0] - verified_kpis['current_mrr'].values[0]) < tolerance, \
        f"MRR drift detected: {current_kpis['current_mrr'].values[0]} != {verified_kpis['current_mrr'].values[0]}"
    
    assert abs(current_kpis['current_arr'].values[0] - verified_kpis['current_arr'].values[0]) < tolerance, \
        f"ARR drift detected"
    
    assert current_kpis['active_customers'].values[0] == verified_kpis['active_customers'].values[0], \
        f"Active customers drift detected"
    
    assert abs(current_kpis['ltv_cac_ratio'].values[0] - verified_kpis['ltv_cac_ratio'].values[0]) < tolerance, \
        f"LTV:CAC ratio drift detected"
    
    print("OK - All verified values match within tolerance")


def test_verified_forecast_shape():
    """Test that forecast output has expected shape."""
    verified_path = Path(__file__).parent.parent / "outputs_verified" / "2025-12-12"
    
    forecast = pd.read_csv(verified_path / "base_forecast.csv")
    
    assert len(forecast) == 12, f"Expected 12 months, got {len(forecast)}"
    assert 'mrr' in forecast.columns, "Missing mrr column"
    assert 'arr' in forecast.columns, "Missing arr column"
    
    print("OK - Forecast shape verified")


def test_verified_scenarios():
    """Test that scenario summary has all 3 scenarios."""
    verified_path = Path(__file__).parent.parent / "outputs_verified" / "2025-12-12"
    
    scenarios = pd.read_csv(verified_path / "scenario_summary.csv")
    
    assert len(scenarios) == 36, f"Expected 36 rows (12×3), got {len(scenarios)}"
    
    scenario_types = scenarios['scenario'].unique()
    assert len(scenario_types) == 3, f"Expected 3 scenarios, got {len(scenario_types)}"
    assert 'base' in scenario_types, "Missing base scenario"
    assert 'optimistic' in scenario_types, "Missing optimistic scenario"
    assert 'pessimistic' in scenario_types, "Missing pessimistic scenario"
    
    print("OK - All 3 scenarios present")


if __name__ == "__main__":
    test_verified_kpi_values()
    test_verified_forecast_shape()
    test_verified_scenarios()
    print("\nOK - All smoke value tests passed!")
