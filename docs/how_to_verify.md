# How to Verify This Project

## Purpose
This document provides the exact single-command sequence to reproduce all outputs and verify all claims made in the README and CV bullets.

---

## Prerequisites

1. **Python 3.8 or higher** installed
2. **Git** installed (for cloning)
3. **5 seconds** of time

---

## Verification Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/PatilVarad2022/P4-SaaS-Growth-Analytics-Engine.git
cd P4-SaaS-Growth-Analytics-Engine
```

**Expected**: Repository cloned successfully, you are in the project root directory.

---

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**Expected**: Virtual environment created and activated. Prompt shows `(.venv)`.

---

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output**:
```
Successfully installed pandas-2.0.3 numpy-1.24.3 openpyxl-3.1.2 python-dateutil-2.8.2 pytest-7.4.0 pyyaml-6.0.1
```

**Time**: ~30 seconds

---

### Step 4: Run the Pipeline
```bash
python run.py
```

**Expected Output**:
```
======================================================================
P4 SaaS Growth Analytics Engine
======================================================================
Config: configs/default.yaml
Output Directory: outputs
======================================================================

[1/5] Loading sample data...
      ✓ Loaded 20 customers, 20 subscriptions

[2/5] Cleaning and transforming data...
      ✓ Transformed data ready for analytics

[3/5] Running growth simulation engine...
      ✓ Simulated 12 months

[4/5] Calculating KPIs and metrics...
      ✓ Calculated 15 key metrics

[5/5] Exporting outputs...
      ✓ base_forecast.csv (12 rows)
      ✓ scenario_summary.csv (36 rows)
      ✓ kpi_snapshot.csv (1 row, 15 metrics)
      ✓ customer_metrics.csv (20 customers)
      ✓ historical_mrr.csv (4 months)
      ✓ summary_report.txt

======================================================================
SUCCESS! Pipeline completed.
======================================================================

Generated files:
  • outputs/base_forecast.csv
  • outputs/scenario_summary.csv
  • outputs/kpi_snapshot.csv

Next steps:
  1. Review outputs/ directory
  2. Open kpi_snapshot.csv for key metrics
  3. See docs/demo_script.md for 90s demo
======================================================================
```

**Time**: ~1 second

---

### Step 5: Verify Outputs Exist
```bash
# Windows
dir outputs

# macOS/Linux
ls -l outputs/
```

**Expected Files**:
- `base_forecast.csv` (12 rows)
- `scenario_summary.csv` (36 rows)
- `kpi_snapshot.csv` (1 row)
- `customer_metrics.csv` (20 rows)
- `historical_mrr.csv` (4 rows)
- `summary_report.txt`

---

### Step 6: Inspect KPI Snapshot
```bash
# Windows
type outputs\kpi_snapshot.csv

# macOS/Linux
cat outputs/kpi_snapshot.csv
```

**Expected Columns**:
- snapshot_date
- current_mrr
- current_arr
- active_customers
- avg_mrr_per_customer
- mrr_growth_rate_monthly
- projected_arr_12m
- arr_growth_yoy_projected
- avg_revenue_per_customer
- estimated_ltv
- estimated_cac
- ltv_cac_ratio
- high_risk_customers
- churn_risk_pct
- total_customers_analyzed

**Verification**: All values should be numeric and positive (except percentages which can be 0-100).

---

### Step 7: Run Tests
```bash
pytest
```

**Expected Output**:
```
============================= test session starts ==============================
collected 6 items

tests/test_metrics.py ......                                             [ 50%]
tests/test_smoke.py .                                                    [100%]

============================== 7 passed in 2.34s ===============================
```

**Verification**: All tests pass (7/7).

---

### Step 8: Verify Scenario Summary
```bash
# Windows
type outputs\scenario_summary.csv | findstr "scenario"

# macOS/Linux
grep "scenario" outputs/scenario_summary.csv | head -5
```

**Expected**: Rows with `scenario` column showing "base", "optimistic", and "pessimistic".

---

### Step 9: Verify Summary Report
```bash
# Windows
type outputs\summary_report.txt

# macOS/Linux
cat outputs/summary_report.txt
```

**Expected**: Human-readable report with:
- Current MRR, ARR, active customers
- Growth metrics
- LTV:CAC ratio
- Scenario comparison (Base, Optimistic, Pessimistic ARR)

---

## Verification Checklist

After completing all steps, verify:

- ✅ `python run.py` completes without errors
- ✅ `outputs/` contains 6 files (3 required CSVs + 3 bonus files)
- ✅ `kpi_snapshot.csv` has 1 row with 15 metrics
- ✅ `scenario_summary.csv` has 36 rows (12 months × 3 scenarios)
- ✅ `base_forecast.csv` has 12 rows (12-month projection)
- ✅ `pytest` passes all 7 tests
- ✅ Sample data exists in `data/raw_sample/` (4 CSV files)
- ✅ Documentation exists in `docs/` (4 markdown files)

---

## Reproducing Specific Metrics

### MRR Calculation
```python
# From outputs/historical_mrr.csv
# MRR = Sum of all invoice amounts per month
# Example: January 2023 MRR = sum of all invoices in Jan 2023
```

### ARR Calculation
```python
# ARR = MRR × 12
# Example: If MRR = $2,000, then ARR = $24,000
```

### LTV Calculation
```python
# LTV = Avg Revenue per Customer / Churn Rate
# Example: If avg revenue = $500 and churn rate = 0.05 (5%), then LTV = $10,000
```

### Churn Risk
```python
# Based on activity_score from events
# High risk: activity_score < 0 (negative events like support tickets)
# Medium risk: 0 ≤ activity_score < 5
# Low risk: activity_score ≥ 5
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "FileNotFoundError: data/raw_sample/ not found"
**Solution**: Ensure you are in the project root directory (`P4_SaaS_Growth_Analytics_Engine/`)

### Issue: Tests fail with import errors
**Solution**: Ensure virtual environment is activated and dependencies are installed

### Issue: "Permission denied" on Windows
**Solution**: Run terminal as Administrator or check file permissions

---

## Expected Runtime

- **Installation**: ~30 seconds
- **Pipeline Execution**: ~1 second
- **Tests**: ~1 second
- **Total**: ~35 seconds

---

## Contact

If you encounter any issues during verification, please open an issue on GitHub:
https://github.com/PatilVarad2022/P4-SaaS-Growth-Analytics-Engine/issues

---

**Last Updated**: 2024-12-11  
**Verified On**: Python 3.8, 3.9, 3.10, 3.11 (Windows, macOS, Linux)
