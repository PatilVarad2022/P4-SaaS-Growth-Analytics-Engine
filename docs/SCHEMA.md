# Schema Documentation

## customers.csv
customer_id,signup_date,acquisition_source,initial_plan,activated,country
U000001,2023-01-23,organic_search,Free,True,UK

## transactions.csv
transaction_id,customer_id,transaction_date,amount,currency,invoice_status
TXN00000001,U000006,2023-03-17,49,USD,paid

## subscriptions.csv
subscription_id,customer_id,start_date,end_date,status,plan_price,plan_name
SUB000006,U000006,2023-03-17,,active,49,Basic

## events.csv
event_id,customer_id,event_name,event_timestamp
EVT00000001,U000001,login,2023-12-07

## support_tickets.csv
ticket_id,customer_id,created_at,closed_at,status,satisfaction_score
TKT000001,U000005,2024-09-26,2024-09-29,closed,2.0
