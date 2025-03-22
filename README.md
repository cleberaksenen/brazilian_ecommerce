# Brazilian E-Commerce Public Dataset by Olist

## Available at:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Power BI relations

### 1. olist_orders_dataset (main)
### 2. olist_order_items_dataset
#### product_id -> olist_products_dataset
#### seller_id -> olist_sellers_dataset

## New measures added in Power BI

### Basic Measures
#### Total_Orders = COUNT(olist_orders_dataset[order_id])
#### Total_Revenue = SUM(olist_order_payments_dataset[payment_value])
#### Unique_Customers = DISTINCTCOUNT(olist_customers_dataset[customer_id])
#### Total_Products_Sold = SUM(olist_order_items_dataset[order_item_id])

### KPIs for Dashboard
#### Avg_Ticket_Per_Order = [Total_Revenue] / [Total_Orders]
#### Avg_Ticket_Per_Customer = [Total_Revenue] / [Unique_Customers]

