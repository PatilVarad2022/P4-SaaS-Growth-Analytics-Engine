# What Is This Project?

## One-Line Pitch
**P4 SaaS Growth Analytics Engine** is a Python-based simulation and forecasting tool that models B2B SaaS growth metrics (MRR, churn, LTV) and generates scenario-based projections for business planning.

## Problem Statement
SaaS companies need to forecast revenue, understand customer cohort behavior, and model "what-if" scenarios to make data-driven decisions about pricing, customer acquisition, and churn reduction. Manual spreadsheet modeling is error-prone, non-reproducible, and doesn't scale.

## Solution
This project provides an **automated, reproducible analytics pipeline** that:
- Ingests raw customer, subscription, invoice, and event data
- Calculates key SaaS metrics (MRR, ARR, churn rate, LTV, CAC)
- Projects growth forward 12 months using three scenarios (base, optimistic, pessimistic)
- Exports analysis-ready CSV files for dashboarding and decision-making

## Target Audience
- **Business Analysts** who need to forecast SaaS metrics
- **Finance/FP&A Teams** planning revenue and budgets
- **Product Managers** evaluating pricing or feature impact
- **Data Analysts** building dashboards or reports
- **Recruiters/Hiring Managers** evaluating analytical and Python skills

## Key Use Cases
1. **Monthly Business Reviews**: Generate KPI snapshots showing current MRR, ARR, customer counts, and growth rates
2. **Scenario Planning**: Model impact of pricing changes, churn reduction initiatives, or acquisition campaigns
3. **Investor Reporting**: Produce standardized metrics (ARR, LTV:CAC, retention) for board decks
4. **Dashboard Feeds**: Export clean CSVs for Tableau, Power BI, or Looker visualizations

## Technical Approach
- **Language**: Python 3.8+
- **Core Libraries**: pandas, numpy, pyyaml, python-dateutil
- **Architecture**: Modular pipeline (load → transform → simulate → calculate → export)
- **Configuration**: YAML-driven parameters for easy scenario testing
- **Testing**: pytest suite with smoke tests and metric validation

## Assumptions & Simplifications
1. **MRR Calculation**: Assumes monthly invoices represent recurring revenue (no one-time charges separated)
2. **Churn**: Subscription status = 'churned' or missing renewal invoices indicates churn
3. **Growth Projection**: Uses historical average growth rate; does not account for seasonality or external factors
4. **LTV Estimate**: Simplified as `Avg Revenue / Churn Rate` (does not include discount rate)
5. **CAC**: Configured as a fixed estimate (not calculated from actual marketing spend data)
6. **Sample Data**: Includes 4 months of synthetic data for demonstration; real deployments would use actual data sources

## Limitations
- **No Machine Learning**: Forecasts use simple trend extrapolation, not predictive models
- **No Real-Time Data**: Designed for batch processing, not streaming analytics
- **Limited Cohort Analysis**: Retention matrix is simplified; does not include full cohort LTV curves
- **No Multi-Currency Support**: All amounts assumed in USD
- **No API Integration**: Requires manual CSV input (could be extended to pull from Stripe, ChartMogul, etc.)

## What This Project Demonstrates
✅ **Data Engineering**: ETL pipeline design, data validation, schema enforcement  
✅ **Business Acumen**: Understanding of SaaS metrics, cohort analysis, scenario modeling  
✅ **Python Proficiency**: pandas, modular code structure, configuration management  
✅ **Reproducibility**: Single-command execution, pinned dependencies, sample data included  
✅ **Documentation**: Clear README, demo script, CV-ready bullets, proof artifacts  

## Next Steps (Future Enhancements)
- Add cohort LTV curves and retention heatmaps
- Integrate with Stripe API for live data ingestion
- Build interactive Streamlit dashboard
- Add ARIMA/Prophet forecasting models
- Support multi-product/multi-region segmentation
- Export to Excel with formatted charts

---

**For Recruiters**: This project showcases end-to-end analytical thinking, from data ingestion to business insights. The code is production-quality, fully tested, and demonstrates skills directly applicable to business analyst, data analyst, and FP&A roles.

**For Technical Reviewers**: Run `python run.py` to see the full pipeline in action. All outputs are in `outputs/`. See `docs/demo_script.md` for a 90-second walkthrough.
