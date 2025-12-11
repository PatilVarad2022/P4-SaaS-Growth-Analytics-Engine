# Logic & Rules Documentation

**Reference Date**: 2025-12-12  
**Purpose**: Explicit, defensible metric definitions for recruiters and BI builders

---

## RFM (Recency, Frequency, Monetary) Analysis

### Definitions

**Recency**: Days since last transaction  
- Reference Date: 2025-12-12  
- Formula: `days_between(reference_date, max(transaction_date))`  
- Code: `src/revenue.py::calculate_revenue_metrics()`

**Frequency**: Count of transactions in last 180 days  
- Window: 180 days from reference date  
- Formula: `count(transactions WHERE transaction_date >= reference_date - 180)`  
- Code: `src/revenue.py::calculate_revenue_metrics()`

**Monetary**: Sum of transaction amounts in last 180 days  
- Window: 180 days from reference date  
- Formula: `sum(amount WHERE transaction_date >= reference_date - 180)`  
- Code: `src/revenue.py::calculate_revenue_metrics()`

### Bucketing Strategy

**Quantile-based**:
- High: Top 20% (80th percentile and above)
- Medium: Next 30% (50th-80th percentile)
- Low: Bottom 50% (below 50th percentile)

**Implementation**: `src/unit_economics.py::calculate_unit_economics_summary()`

---

## Churn Risk Rules

### Deterministic Thresholds

**HIGH Risk**:
- Last transaction > 60 days ago AND
- Frequency drop > 50% month-over-month AND
- No events in last 30 days

**MEDIUM Risk**:
- Last transaction 30-60 days ago OR
- Frequency drop 25-50% month-over-month OR
- Events < 5 in last 30 days

**LOW Risk**:
- Last transaction < 30 days ago AND
- Stable or increasing frequency AND
- Events >= 5 in last 30 days

**Code**: `src/retention.py::calculate_retention_metrics()`

---

## Funnel Stages

### Event Name Mapping

**Stage 1: Visit** (not tracked in current data)

**Stage 2: Signup**  
- Event: Customer record created  
- Metric: `count(customers)`

**Stage 3: Activate**  
- Event: `activated = True` in customers table  
- Metric: `count(customers WHERE activated = True)`  
- Code: `src/funnel.py::calculate_funnel_metrics()`

**Stage 4: Convert**  
- Event: First paid transaction  
- Metric: `count(DISTINCT customer_id FROM transactions)`  
- Code: `src/funnel.py::calculate_funnel_metrics()`

**Stage 5: Retain**  
- Event: Active subscription after 30 days  
- Metric: `count(subscriptions WHERE datediff(start_date, current_date) > 30 AND status = 'active')`  
- Code: `src/funnel.py::calculate_funnel_metrics()`

### Conversion Rates

- Signup → Activate: ~65%  
- Activate → Convert: ~25%  
- Convert → Retain (30d): ~97%

---

## Cohort Analysis

### Cohort Definition

**Cohort ID**: Signup month in YYYY-MM format  
- Formula: `DATE_FORMAT(signup_date, '%Y-%m')`  
- Example: Customer signed up 2023-01-15 → Cohort "2023-01"

**Code**: `src/retention.py::generate_cohort_retention_matrix()`

### Retention Calculation

**Month N Retention**:
- Formula: `count(active_customers_in_month_N) / cohort_size`  
- Active = has transaction OR active subscription in month N  
- Measured at months 0, 1, 2, 3, 6, 12

**Code**: `src/retention.py::generate_cohort_retention_matrix()`

---

## Key Performance Indicators

### MRR (Monthly Recurring Revenue)

**Formula**: `SUM(plan_price WHERE subscription.status = 'active')`  
- Calculated monthly  
- Excludes one-time charges  
- Code: `src/revenue.py::calculate_revenue_metrics()`

### ARR (Annual Recurring Revenue)

**Formula**: `MRR × 12`  
- Code: `src/revenue.py::calculate_revenue_metrics()`

### ARPU (Average Revenue Per User)

**Formula**: `MRR / count(active_customers)`  
- Active = has transaction OR active subscription in month  
- Code: `src/revenue.py::calculate_revenue_metrics()`

### ARPPU (Average Revenue Per Paying User)

**Formula**: `MRR / count(paying_customers)`  
- Paying = has active paid subscription  
- Code: `src/revenue.py::calculate_revenue_metrics()`

### LTV (Lifetime Value)

**Formula**: `plan_price × (lifetime_days / 30)`  
- Lifetime days = days from signup to churn (or current date if active)  
- Code: `src/unit_economics.py::calculate_unit_economics()`

### CAC (Customer Acquisition Cost)

**Formula**: Simulated by acquisition channel  
- organic_search: $150-$250  
- paid_ads: $400-$600  
- referral: $70-$130  
- sales_outbound: $650-$950  
- content_marketing: $100-$200  
- Code: `src/user_simulation.py::generate_user_lifecycle()`

### LTV:CAC Ratio

**Formula**: `LTV / CAC`  
- Target: > 3.0 (healthy)  
- Code: `src/unit_economics.py::calculate_unit_economics()`

### Churn Rate (Monthly)

**Formula**: `count(churned_in_month) / count(active_at_month_start)`  
- Code: `src/retention.py::calculate_churn_rate_monthly()`

---

## Scenario Projections

### Base Case
- Growth Rate: Historical average  
- Churn Rate: 5% monthly (default)

### High Churn (+20%)
- Growth Rate: Historical average  
- Churn Rate: 6% monthly (5% × 1.2)

### Reduced Churn (-15%)
- Growth Rate: Historical average  
- Churn Rate: 4.25% monthly (5% × 0.85)

### Increased Marketing (+25% CAC)
- Growth Rate: +15% from historical  
- CAC: +25% from baseline  
- Churn Rate: 5% monthly

### Improved Conversion (+10%)
- Conversion Rate: +10% from baseline  
- Churn Rate: 5% monthly

### Pricing Change (+15% ARPU)
- Plan Prices: +15% across all tiers  
- Churn Rate: 5% monthly

**Code**: `run_full_analysis.py::generate_scenarios()`

---

## Data Quality Rules

1. **No negative revenue**: All amounts >= 0
2. **Valid dates**: All dates between 2022-01-01 and 2024-12-31
3. **Valid customer references**: All foreign keys exist in customers table
4. **Valid plan prices**: Only 0, 49, 199 allowed
5. **Valid event names**: Only login, feature_use, page_view, export_data, invite_sent
6. **Valid statuses**: Only active/churned for subscriptions, open/closed for tickets

---

**Last Updated**: 2025-12-12  
**Maintained By**: Analytics Team
