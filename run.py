#!/usr/bin/env python3
"""
P4 SaaS Growth Analytics Engine - Single Command Entrypoint

Usage:
    python run.py                    # Run with default config
    python run.py --config configs/example_override.yaml
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_loader import load_sample_data
from transform import clean_and_transform
from engine import run_growth_simulation
from metrics import calculate_kpis
from export import export_outputs


def main():
    parser = argparse.ArgumentParser(
        description="P4 SaaS Growth Analytics Engine - End-to-End Pipeline"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default.yaml",
        help="Path to configuration YAML file (default: configs/default.yaml)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory for output files (default: outputs/)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("P4 SaaS Growth Analytics Engine")
    print("=" * 70)
    print(f"Config: {args.config}")
    print(f"Output Directory: {args.output_dir}")
    print("=" * 70)
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Step 1: Load Data
        print("\n[1/5] Loading sample data...")
        raw_data = load_sample_data()
        print(f"      OK - Loaded {len(raw_data['customers'])} customers, "
              f"{len(raw_data['subscriptions'])} subscriptions")
        
        # Step 2: Transform
        print("\n[2/5] Cleaning and transforming data...")
        clean_data = clean_and_transform(raw_data, args.config)
        print(f"      OK - Transformed data ready for analytics")
        
        # Step 3: Run Simulation Engine
        print("\n[3/5] Running growth simulation engine...")
        simulation_results = run_growth_simulation(clean_data, args.config)
        print(f"      OK - Simulated {simulation_results['months_projected']} months")
        
        # Step 4: Calculate KPIs
        print("\n[4/5] Calculating KPIs and metrics...")
        kpis = calculate_kpis(clean_data, simulation_results, args.config)
        print(f"      OK - Calculated {len(kpis)} key metrics")
        
        # Step 5: Export Outputs
        print("\n[5/5] Exporting outputs...")
        export_outputs(
            clean_data=clean_data,
            simulation_results=simulation_results,
            kpis=kpis,
            output_dir=args.output_dir
        )
        print(f"      OK - Exported to {args.output_dir}/")
        
        print("\n" + "=" * 70)
        print("SUCCESS! Pipeline completed.")
        print("=" * 70)
        print("\nGenerated files:")
        print(f"  • {args.output_dir}/base_forecast.csv")
        print(f"  • {args.output_dir}/scenario_summary.csv")
        print(f"  • {args.output_dir}/kpi_snapshot.csv")
        print("\nNext steps:")
        print("  1. Review outputs/ directory")
        print("  2. Open kpi_snapshot.csv for key metrics")
        print("  3. See docs/demo_script.md for 90s demo")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
