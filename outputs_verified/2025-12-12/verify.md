# Verified Run - 2025-12-12

## Run Details

**Date**: 2025-12-12  
**Time**: 00:40 IST  
**Command**: `python run.py --config configs/default.yaml`

## Environment

**Python Version**: 3.13.5  
**OS**: Windows 11  
**CPU**: 16 threads  
**RAM**: Available  

## Performance

**Elapsed Time**: ~1.0 second  
**Files Generated**: 3 key CSVs

## Output Files

1. `kpi_snapshot.csv` - 1 row, 15 KPIs
2. `base_forecast.csv` - 12 rows (12-month projection)
3. `scenario_summary.csv` - 36 rows (3 scenarios × 12 months)

## Key Metrics (Verified)

From `kpi_snapshot.csv`:
- **Current MRR**: $1,737.00
- **Current ARR**: $20,844.00
- **Active Customers**: 13
- **Monthly Growth Rate**: 41.15%
- **Projected ARR (12m)**: $1,303,511.69
- **LTV:CAC Ratio**: 8.44x
- **Churn Risk**: 15.0% (3 customers)

## Reproducibility

**Random Seed**: 42 (set in `configs/default.yaml`)  
**Deterministic**: Yes - same inputs produce identical outputs

## Verification Command

```bash
# Run pipeline
python run.py

# Compare outputs
diff outputs/kpi_snapshot.csv outputs_verified/2025-12-12/kpi_snapshot.csv
diff outputs/base_forecast.csv outputs_verified/2025-12-12/base_forecast.csv
diff outputs/scenario_summary.csv outputs_verified/2025-12-12/scenario_summary.csv
```

All diffs should be empty (files identical).

## Checksums

See `../verify_checksums.txt` for SHA256 hashes of these files.

---

**Purpose**: Instant proof for recruiters that claims are verifiable.  
**Status**: ✅ VERIFIED
