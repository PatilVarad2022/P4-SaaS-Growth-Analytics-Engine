# Power BI Integration Guide

## Data Model
Load all CSVs from `data/raw_sample/`.

### Relationships (Join Map)
- **customers** (`customer_id`) -> **transactions** (`customer_id`) [One-to-Many]
- **customers** (`customer_id`) -> **subscriptions** (`customer_id`) [One-to-Many]
- **customers** (`customer_id`) -> **events** (`customer_id`) [One-to-Many]
- **customers** (`customer_id`) -> **support_tickets** (`customer_id`) [One-to-Many]

*Note*: Ensure `customer_id` is the primary key in the Dates/Customers dimension tables if creating a Star Schema. Use a `Date Table` for all date joins.

## Data Preparation
1. **Date Fields**: Parse `signup_date`, `transaction_date`, `start_date`, `end_date`, `event_timestamp` as Date/DateTime objects.
2. **Event Normalization**: Use `configs/event_name_map.yaml` to group raw event names into canonical events (e.g. 'Login' vs 'login').

## DAX Templates

### ARPU (Average Revenue Per User)
```dax
ARPU = 
DIVIDE(
    SUM(transactions[amount]),
    DISTINCTCOUNT(transactions[customer_id]),
    0
)
```

### Monthly Churn Rate
```dax
Churn Rate % = 
VAR ChurnedUsers = CALCULATE(DISTINCTCOUNT(subscriptions[customer_id]), subscriptions[status] = "churned")
VAR TotalUsers = CALCULATE(DISTINCTCOUNT(subscriptions[customer_id]), subscriptions[status] = "active")
RETURN
DIVIDE(ChurnedUsers, TotalUsers + ChurnedUsers, 0)
```

## Filters
Apply global page filters for:
- [Placeholder: Date Range]
- [Placeholder: Customer Country]
