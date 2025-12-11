# 90-Second Demo Script

## Purpose
This script guides you through a quick demonstration of the P4 SaaS Growth Analytics Engine for recruiters, interviewers, or stakeholders.

## Prerequisites
- Python 3.8+ installed
- Repository cloned locally
- 90 seconds of time

---

## Demo Steps (90 seconds)

### Step 1: Run the Pipeline (10 seconds)
```bash
cd P4_SaaS_Growth_Analytics_Engine
python run.py
```

**What to say**: "This single command runs the entire analytics pipeline—loading sample data, calculating metrics, running growth simulations, and exporting outputs."

---

### Step 2: Show KPI Snapshot (20 seconds)
Open `outputs/kpi_snapshot.csv` in Excel or a text editor.

**What to highlight**:
- **Current MRR & ARR**: Shows current monthly and annual recurring revenue
- **Active Customers**: Total customer count
- **Growth Rate**: Month-over-month MRR growth percentage
- **LTV:CAC Ratio**: Customer lifetime value to acquisition cost ratio
- **Churn Risk**: Percentage of customers at high risk of churning

**What to say**: "This snapshot gives executives a one-row view of all critical SaaS health metrics—perfect for board decks or monthly reviews."

---

### Step 3: Show Scenario Summary (25 seconds)
Open `outputs/scenario_summary.csv` in Excel.

**What to highlight**:
- **Three scenarios**: Base, Optimistic, Pessimistic
- **12-month projection**: MRR, ARR, customer counts for each month
- **Scenario comparison**: Shows range of possible outcomes

**What to say**: "This file models three growth scenarios over 12 months. Finance teams use this for budgeting, and product teams use it to evaluate the impact of churn reduction or pricing changes."

**Pro tip**: Filter by `scenario` column to compare outcomes side-by-side.

---

### Step 4: Show Base Forecast (15 seconds)
Open `outputs/base_forecast.csv`.

**What to highlight**:
- **Monthly detail**: MRR, ARR, new customers, churned customers
- **Net new customers**: Shows customer acquisition vs. churn each month

**What to say**: "This is the detailed month-by-month forecast using historical growth rates. It's the foundation for the scenario analysis."

---

### Step 5: Show Summary Report (10 seconds)
Open `outputs/summary_report.txt`.

**What to highlight**:
- **Human-readable format**: No need to parse CSVs
- **Key metrics at a glance**: MRR, growth, LTV:CAC, churn risk
- **Scenario comparison**: ARR projections for all three scenarios

**What to say**: "This text report is auto-generated for quick reviews—perfect for sharing via email or Slack."

---

### Step 6: Explain Reproducibility (10 seconds)
Show the `data/raw_sample/` directory.

**What to say**: "The project includes sample data so anyone can run the pipeline immediately without external dependencies. In production, you'd point this at real Stripe or billing data."

---

## Closing Statement
"This project demonstrates end-to-end analytical thinking: data ingestion, transformation, metric calculation, scenario modeling, and export. It's production-ready, fully tested, and designed to be extended with real data sources or advanced forecasting models."

---

## Bonus: Show Configuration (if time allows)
Open `configs/default.yaml`.

**What to highlight**:
- **Configurable parameters**: Churn rate, CAC, activity weights, scenario modifiers
- **No code changes needed**: Analysts can tweak assumptions without touching Python

**What to say**: "All business logic is externalized to YAML configs, so non-technical users can run sensitivity analyses by just editing this file."

---

## Total Time: ~90 seconds

**Files to have open**:
1. `outputs/kpi_snapshot.csv`
2. `outputs/scenario_summary.csv`
3. `outputs/summary_report.txt`

**Key talking points**:
- ✅ Single-command execution
- ✅ Production-quality outputs
- ✅ Scenario modeling for decision-making
- ✅ Reproducible with sample data
- ✅ Configurable without code changes
