# Changelog

All notable changes to the P4 SaaS Growth Analytics Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-11

### Added
- Initial release of P4 SaaS Growth Analytics Engine
- Single-command entrypoint (`run.py`) for full pipeline execution
- Modular source code structure (data_loader, transform, engine, metrics, export)
- Sample raw data (customers, subscriptions, invoices, events) for reproducibility
- Configuration system with YAML files (default.yaml, example_override.yaml)
- Core simulation engine with three scenarios (base, optimistic, pessimistic)
- Comprehensive SaaS metrics calculation (MRR, ARR, LTV, CAC, churn risk)
- CSV export functionality for all outputs
- Automated test suite with pytest (smoke tests and metric validation)
- Complete documentation:
  - README.md with quickstart and project overview
  - WHAT_IS_THIS_PROJECT.md for recruiters
  - demo_script.md for 90-second demos
  - cv_bullets.md with ATS-optimized resume bullets
  - schema.md with data dictionary
- MIT License
- Pinned dependencies in requirements.txt
- .gitignore for Python projects

### Features
- **Data Loading**: Loads sample CSV files with schema validation
- **Data Transformation**: Cleans data, parses dates, calculates MRR
- **Growth Simulation**: Projects MRR, ARR, and customer counts 12 months forward
- **Scenario Modeling**: Base, optimistic, and pessimistic growth scenarios
- **KPI Calculation**: 15+ SaaS metrics including LTV:CAC ratio
- **Export**: Generates base_forecast.csv, scenario_summary.csv, kpi_snapshot.csv
- **Testing**: Smoke tests and metric validation with pytest
- **Configuration**: YAML-driven parameters for easy customization

### Documentation
- Comprehensive README with badges, quickstart, and structure
- One-page project narrative for recruiters
- 90-second demo script with talking points
- CV-ready bullets (one-line, two-line, interview variants)
- Data schema documentation with sample values
- MIT License

### Testing
- Smoke test: End-to-end pipeline execution
- Metrics tests: MRR, ARR, LTV, scenario validation
- All tests passing with pytest

---

## [Unreleased]

### Planned Features
- ARIMA/Prophet forecasting models
- Stripe API integration for live data
- Interactive Streamlit dashboard
- Multi-product/multi-region segmentation
- Cohort LTV curves and retention heatmaps
- Excel export with formatted charts

---

## Release Notes

### v1.0.0 - Initial CV-Ready Release
This release includes all components required for a CV-ready portfolio project:
- ✅ Single-command execution (`python run.py`)
- ✅ Required outputs (base_forecast.csv, scenario_summary.csv, kpi_snapshot.csv)
- ✅ Sample data for reproducibility
- ✅ Comprehensive documentation
- ✅ Passing test suite
- ✅ Pinned dependencies
- ✅ MIT License
- ✅ Professional README

**Target Audience**: Business Analysts, Data Analysts, FP&A Professionals, Recruiters

**Verification**: Run `python run.py` to generate all outputs in under 5 seconds.
