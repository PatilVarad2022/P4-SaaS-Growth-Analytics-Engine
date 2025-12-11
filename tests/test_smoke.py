"""
Smoke test - Verifies the pipeline runs end-to-end without errors
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_loader import load_sample_data
from transform import clean_and_transform
from engine import run_growth_simulation
from metrics import calculate_kpis
from export import export_outputs


def test_pipeline_runs_end_to_end():
    """
    Smoke test: Run the entire pipeline and assert outputs are produced.
    """
    config_path = Path(__file__).parent.parent / "configs" / "default.yaml"
    output_dir = Path(__file__).parent.parent / "outputs" / "test_run"
    
    # Ensure output dir exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load data
    raw_data = load_sample_data()
    assert raw_data is not None, "Failed to load sample data"
    assert 'customers' in raw_data, "Missing customers data"
    assert 'subscriptions' in raw_data, "Missing subscriptions data"
    assert len(raw_data['customers']) > 0, "Customers data is empty"
    
    # Step 2: Transform
    clean_data = clean_and_transform(raw_data, str(config_path))
    assert clean_data is not None, "Transform failed"
    assert 'mrr_data' in clean_data, "Missing MRR data"
    assert 'customer_metrics' in clean_data, "Missing customer metrics"
    
    # Step 3: Run simulation
    simulation_results = run_growth_simulation(clean_data, str(config_path))
    assert simulation_results is not None, "Simulation failed"
    assert 'base_forecast' in simulation_results, "Missing base forecast"
    assert 'optimistic_forecast' in simulation_results, "Missing optimistic forecast"
    assert 'pessimistic_forecast' in simulation_results, "Missing pessimistic forecast"
    
    # Step 4: Calculate KPIs
    kpis = calculate_kpis(clean_data, simulation_results, str(config_path))
    assert kpis is not None, "KPI calculation failed"
    assert 'current_mrr' in kpis, "Missing current_mrr in KPIs"
    assert 'current_arr' in kpis, "Missing current_arr in KPIs"
    assert kpis['current_mrr'] > 0, "MRR should be positive"
    
    # Step 5: Export
    export_outputs(clean_data, simulation_results, kpis, str(output_dir))
    
    # Verify outputs exist
    assert (output_dir / "base_forecast.csv").exists(), "base_forecast.csv not created"
    assert (output_dir / "scenario_summary.csv").exists(), "scenario_summary.csv not created"
    assert (output_dir / "kpi_snapshot.csv").exists(), "kpi_snapshot.csv not created"
    
    print("✓ Smoke test passed: Pipeline runs end-to-end successfully")


if __name__ == "__main__":
    test_pipeline_runs_end_to_end()
