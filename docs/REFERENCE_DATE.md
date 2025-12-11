# Reference Date

**Snapshot Date**: 2025-12-12  
**Export Date**: 2025-12-12  
**Data Range**: 2022-01-01 to 2024-12-31

---

## Purpose

This reference date is used for all recency calculations in RFM analysis and churn risk scoring.

## Recency Calculation

```
Recency (days) = 2025-12-12 - MAX(transaction_date)
```

## Impact on Metrics

- **RFM Analysis**: All recency scores calculated from 2025-12-12
- **Churn Risk**: "Days since last transaction" measured from 2025-12-12
- **Active Customer Definition**: Active as of 2025-12-12

## Reproducibility

To reproduce exact metrics:
1. Use reference date: 2025-12-12
2. Load data from `data/raw_sample/` (exported 2025-12-12)
3. Run `python run_full_analysis.py`

All outputs will match `outputs/` directory.

---

**Note**: When re-running analysis on different dates, update reference date in code and documentation for consistency.
