# How to Run - Quick Start

## One-Command Setup

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate (Windows)
.venv\Scripts\activate

# 3. Activate (macOS/Linux)
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run pipeline
python run.py --config configs/default.yaml
```

## Expected Output

After running `python run.py`, you should see:

```
======================================================================
P4 SaaS Growth Analytics Engine
======================================================================
Config: configs/default.yaml
Output Directory: outputs
======================================================================

[1/5] Loading sample data...
[2/5] Cleaning and transforming data...
[3/5] Running growth simulation engine...
[4/5] Calculating KPIs and metrics...
[5/5] Exporting outputs...

SUCCESS! Pipeline completed.
```

## Verify Key Metrics

Open `outputs/kpi_snapshot.csv` and verify first 3 rows:

```csv
snapshot_date,current_mrr,current_arr,active_customers,avg_mrr_per_customer...
2025-12-12,1737,20844,13,133.62...
```

**Expected Values**:
- `current_mrr`: 1737
- `current_arr`: 20844
- `active_customers`: 13

## Runtime

**Expected**: ~1 second on modern hardware

## Troubleshooting

**Issue**: ModuleNotFoundError  
**Fix**: Run `pip install -r requirements.txt`

**Issue**: Permission denied  
**Fix**: Run terminal as Administrator (Windows) or use `sudo` (Linux/macOS)

---

**Total Time**: < 2 minutes from clone to verified outputs
