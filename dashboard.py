import kagglehub
import shutil
import os
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

customers_dataset = pd.read_csv("./data/olist_customers_dataset.csv")
geolocation_dataset = pd.read_csv("./data/olist_geolocation_dataset.csv")
orders_dataset = pd.read_csv("./data/olist_orders_dataset.csv")
order_items_dataset = pd.read_csv("./data/olist_order_items_dataset.csv")
order_payments_dataset = pd.read_csv("./data/olist_order_payments_dataset.csv")
order_reviews_dataset = pd.read_csv("./data/olist_order_reviews_dataset.csv")
products_dataset = pd.read_csv("./data/olist_products_dataset.csv")
sellers_dataset = pd.read_csv("./data/olist_sellers_dataset.csv")

### 1. Frequency of each order status
order_status_counts = orders_dataset["order_status"].value_counts().reset_index()
order_status_counts.columns = ["Status", "Count"]

fig_orders = px.bar(
    order_status_counts, 
    x="Status", 
    y="Count", 
    title="📦 Order Status in E-Commerce", 
    text="Count",
    color="Status", 
    color_discrete_sequence=px.colors.qualitative.Set2,
)

fig_orders.update_traces(
    marker=dict(line=dict(width=1, color="black"))
)

fig_orders.update_layout(
    title_font_size=20, 
    xaxis_title="Order Status",
    yaxis_title="Order count",
    xaxis_tickangle=-30, 
    template="plotly_white",
)

### 2. Frequency of each payment type
payment_type_counts = order_payments_dataset["payment_type"].value_counts().reset_index()
payment_type_counts.columns = ["Payment type", "Count"]

fig_payments = px.bar(
    payment_type_counts, 
    x="Payment type", 
    y="Count", 
    title="💳 Payment Types in E-Commerce", 
    text="Count",
    color="Payment type",
    color_discrete_sequence=px.colors.qualitative.Set1,
)

fig_payments.update_traces(
    marker=dict(line=dict(width=1, color="black"))
)

fig_payments.update_layout(
    title_font_size=20,
    xaxis_title="Payment Type",
    yaxis_title="Payment Count",
    xaxis_tickangle=-30,
    template="plotly_white",
)

### 3. Monthly purchase period
orders_dataset["order_purchase_timestamp"] = pd.to_datetime(orders_dataset["order_purchase_timestamp"])
orders_dataset["Year-month"] = orders_dataset["order_purchase_timestamp"].dt.to_period("M")

orders_by_month = orders_dataset["Year-month"].value_counts().sort_index().reset_index()
orders_by_month["Year-month"] = orders_by_month["Year-month"].astype(str)
orders_by_month.columns = ["Year-month", "Count"]

fig_timestamp = px.line(
    orders_by_month, 
    x="Year-month", 
    y="Count", 
    title="📅 Monthly Order Count", 
    labels={"Year-month": "Period", "Count": "Quantity of Orders"}, 
    markers=True,
    line_shape="linear", 
    color_discrete_sequence=["#1f77b4"],
)

fig_timestamp.update_layout(
    title_font_size=20,
    xaxis_title="Period", 
    yaxis_title="Quantity of Orders",
    xaxis_tickangle=-45,  
    template="plotly_white",  
    plot_bgcolor="rgba(0,0,0,0)",  
    showlegend=False
)

fig_timestamp.update_xaxes(showgrid=True)
fig_timestamp.update_yaxes(showgrid=True)

### 4. Price value with freight
df_orders_items = order_items_dataset.merge(products_dataset, on="product_id")
df_orders_items["total_price"] = df_orders_items["price"] + df_orders_items["freight_value"]

revenue_by_category = df_orders_items.groupby("product_category_name")["total_price"].sum().reset_index()
top_categories = revenue_by_category.nlargest(10, "total_price")
top_categories.columns = ["Product category", "Total price"]

fig_product_category = px.bar(
    top_categories, 
    x="Total price", 
    y="Product category", 
    title="💰 Top 10 Product Categories by Revenue", 
    labels={"Total price": "Revenue", "Product category": "Category"},
    orientation="h",
    text="Total price",
    color="Product category",
    color_discrete_sequence=px.colors.qualitative.Set3,
)

fig_product_category.update_layout(
    title_font_size=20,
    xaxis_title="Count",
    yaxis_title="Category",
    template="plotly_white",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_tickangle=0,
    showlegend=False
)

fig_product_category.update_traces(
    textposition="outside",
    marker=dict(line=dict(width=1, color="black"))
)

### 5. Average value for each type of payment
df_payments = order_payments_dataset.merge(orders_dataset, on="order_id")
avg_ticket = df_payments.groupby("payment_type")["payment_value"].mean().reset_index()
avg_ticket.columns = ["Payment type", "Mean value"]
avg_ticket = avg_ticket.sort_values(by="Mean value", ascending=False)

fig_avg_ticket = px.bar(
    avg_ticket, 
    x="Payment type", 
    y="Mean value", 
    title="💳 Average Ticket by Payment Type",
    labels={"payment_type": "Payment Type", "payment_value": "Mean Value"},
    text_auto=True,
)

fig_avg_ticket.update_traces(
    marker=dict(line=dict(width=1, color="black"))
)

fig_avg_ticket.update_layout(
    title_font_size=20,
    xaxis_title="Payment Type",
    yaxis_title="Mean Value",
    xaxis_tickangle=-30,
    template="plotly_white",
)

### 6. Product Categories by Revenue
df_orders_items = order_items_dataset.merge(products_dataset, on="product_id")
df_orders_items["total_price"] = df_orders_items["price"] + df_orders_items["freight_value"]

revenue_by_category = df_orders_items.groupby("product_category_name")["total_price"].sum().reset_index()
top_categories = revenue_by_category.nlargest(10, "total_price")
top_categories.columns = ["Product category", "Total price"]

fig_top_categories = px.bar(
    top_categories, 
    x="Product category", 
    y="Total price", 
    title="💵 Top 10 Product Categories by Revenue", 
    labels={"Product category": "Category", "Total price": "Revenue"},
    text="Total price",
    color="Product category",
    color_discrete_sequence=px.colors.qualitative.Set3,
)

fig_top_categories.update_layout(
    title_font_size=20,
    xaxis_tickangle=-45,
    template="plotly_white",
    xaxis_title="Category",
    yaxis_title="Revenue",
    plot_bgcolor="rgba(0,0,0,0)",
)

fig_top_categories.update_traces(
    marker=dict(line=dict(width=1, color="black")),
    textposition="outside"
)


## Dash development
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("E-Commerce Dashboard"),
    dcc.Graph(figure=fig_orders),
    dcc.Graph(figure=fig_payments),
    dcc.Graph(figure=fig_timestamp),
    dcc.Graph(figure=fig_product_category),
    dcc.Graph(figure=fig_avg_ticket),
    dcc.Graph(figure=fig_top_categories)
])

if __name__ == "__main__":
    from threading import Timer
    import webbrowser

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8050/")

    Timer(1, open_browser).start()
    app.run_server(debug=False)