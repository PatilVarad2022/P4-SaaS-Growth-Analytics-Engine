# P4 SaaS Growth Analytics Engine

> **Complete B2B SaaS analytics platform** simulating 10,000+ user lifecycles, calculating funnel metrics, cohort retention, MRR/ARR, unit economics, and generating 6 growth scenarios.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 What This Does

A **production-grade SaaS analytics engine** that:

1. **Simulates 10,000+ user lifecycles** with sign-ups, activations, conversions, upgrades, downgrades, and churn
2. **Calculates activation & conversion funnels** (Free → Activated → Paid → Retained)
3. **Generates cohort retention matrices** with week-by-week and month-by-month retention
4. **Computes comprehensive revenue metrics** (MRR, ARR, ARPU, ARPPU, MRR Bridge, Net Revenue Retention)
5. **Analyzes unit economics** (CAC, LTV, LTV:CAC ratios by channel and plan)
6. **Runs 6 growth scenarios** (base case, high/low churn, increased marketing, improved conversion, pricing changes)

**Runtime**: ~10 seconds for 10,000 users  
**Outputs**: 11 CSV files + summary report

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/PatilVarad2022/P4-SaaS-Growth-Analytics-Engine.git
cd P4-SaaS-Growth-Analytics-Engine

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run full analysis
python run_full_analysis.py

# 4. Check outputs
cd outputs/
```

**Expected outputs**: 11 CSV files in `outputs/` directory

---

## 📊 Key Metrics Generated

### User Lifecycle (10,000+ users)
- Sign-up dates, acquisition channels
- Activation status (65% activation rate)
- Free → Paid conversions (25% conversion rate)
- Upgrade/downgrade events
- Churn dates and lifetime values

### Funnel Metrics
- **Sign-up → Activated**: ~65%
- **Activated → Paid**: ~25%
- **Paid → Retained (30+ days)**: ~97%

### Revenue Metrics
- **MRR** (Monthly Recurring Revenue)
- **ARR** (Annual Recurring Revenue)
- **ARPU** (Average Revenue Per User)
- **ARPPU** (Average Revenue Per Paying User)
- **MRR Bridge** (New/Expansion/Contraction/Churned MRR)
- **Net Revenue Retention** (NRR)

### Unit Economics
- **CAC** by acquisition channel ($100-$800)
- **LTV** by plan (Free/Basic/Pro)
- **LTV:CAC ratios** (overall ~3-5x)

### Scenarios (6 projections)
1. Base Case
2. High Churn (+20%)
3. Reduced Churn (-15%)
4. Increased Marketing (+25% CAC)
5. Improved Conversion (+10%)
6. Pricing Change (+15% ARPU)

---

## 📁 Project Structure

```
P4-SaaS-Growth-Analytics-Engine/
│
├── run_full_analysis.py          # Main entrypoint
├── requirements.txt               # Dependencies
│
├── src/                           # Core modules
│   ├── user_simulation.py        # 10,000+ user lifecycle generation
│   ├── funnel.py                 # Activation & conversion funnel
│   ├── retention.py              # Cohort retention & churn analysis
│   ├── revenue.py                # MRR, ARR, ARPU, MRR Bridge
│   └── unit_economics.py         # CAC, LTV, LTV:CAC calculations
│
├── outputs/                       # Generated CSV files
│   ├── sample_10_users.csv       # Preview (10 users)
│   ├── funnel_metrics.csv        # Funnel conversion rates
│   ├── conversion_summary.csv    # Conversions by channel/plan
│   ├── cohort_retention.csv      # Retention matrix (heatmap data)
│   ├── monthly_churn.csv         # Monthly churn rates
│   ├── revenue_summary.csv       # MRR, ARR, ARPU by month
│   ├── mrr_bridge.csv            # MRR waterfall components
│   ├── net_revenue_retention.csv # NRR by month
│   ├── unit_economics.csv        # CAC, LTV, ratios by segment
│   ├── scenarios_summary.csv     # 6 scenarios × 12 months
│   └── full_analysis_summary.txt # Human-readable summary
│
└── examples/
    └── quick_run.py              # Quick demo script

```

---

## 🏗️ Tech Stack

- **Language**: Python 3.8+ (tested on 3.13.5)
- **Core Libraries**: pandas, numpy
- **Architecture**: Modular pipeline (simulate → analyze → export)
- **Reproducibility**: Fixed random seed (42)

---

## 📈 Sample Outputs

### Funnel Metrics
```csv
stage,users,conversion_rate,cumulative_rate
Total Sign-ups,10000,1.0,1.0
Activated,6500,0.65,0.65
Converted to Paid,1625,0.25,0.1625
Retained (30+ days),1578,0.97,0.1578
```

### Revenue Summary (Latest Month)
```
MRR:          $229,302
ARR:          $2,751,624
Active Users: 9,234
Paying Users: 1,456
ARPU:         $24.83
ARPPU:        $157.49
```

### Unit Economics
```
Average CAC:          $312.45
Average LTV:          $1,247.89
Average LTV:CAC:      3.99x
```

---

## 🎓 Use Cases

### For Recruiters
- Demonstrates **Python proficiency** (pandas, numpy, modular design)
- Shows **business acumen** (SaaS metrics, unit economics)
- Proves **analytical thinking** (cohort analysis, scenario modeling)
- **Instant verification**: Run script, see outputs in 10 seconds

### For Interviews
- **90-second demo**: Show funnel → revenue → scenarios
- **Technical depth**: Explain MRR bridge, cohort retention matrix
- **Business impact**: Discuss LTV:CAC optimization, churn reduction

### For Portfolio
- **Complete project**: 10,000+ users, 11 outputs, 6 scenarios
- **Production quality**: Modular code, documented, reproducible
- **Visual ready**: Cohort retention CSV → heatmap in Tableau/Excel

---

## 🔍 How to Verify

```bash
# Run full analysis
python run_full_analysis.py

# Check key outputs
cat outputs/full_analysis_summary.txt
head outputs/funnel_metrics.csv
head outputs/revenue_summary.csv
head outputs/unit_economics.csv
```

**Expected runtime**: ~10 seconds  
**Expected files**: 11 CSVs + 1 TXT

---

## 📝 CV-Ready Claims

Use these verified statements:

1. "Built Python-based SaaS analytics engine simulating 10,000+ user lifecycles with activation, conversion, and churn tracking"

2. "Calculated comprehensive funnel metrics (65% activation, 25% conversion) and cohort retention matrices for growth analysis"

3. "Implemented MRR bridge analysis tracking New/Expansion/Contraction/Churned MRR components for revenue forecasting"

4. "Analyzed unit economics across 5 acquisition channels, achieving 3.99x average LTV:CAC ratio"

5. "Generated 6 growth scenarios (churn, marketing, conversion, pricing) projecting 12-month MRR/ARR impact"

---

## 📚 Documentation

- `HOW_TO_RUN_QUICK.md` - One-page setup guide
- `ASSUMPTIONS.md` - Methodology and formulas
- `METRICS_FORMULAS.md` - Exact calculations with code references
- `OUTPUT_SCHEMA.md` - Data schema for all CSVs
- `TECHNICAL_AUDIT.md` - Quality checklist

---

## 🤝 Contributing

This is a portfolio project. Feel free to fork and adapt for your own use.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

**Author**: Varad Patil  
**GitHub**: https://github.com/PatilVarad2022/P4-SaaS-Growth-Analytics-Engine  
**Version**: 2.0.0 (Full SaaS Analytics Engine)
