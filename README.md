# E-Commerce Sales & Customer Behavior Analysis

## Project Overview

This project analyzes the Brazilian Olist E-Commerce dataset to uncover insights into customer behavior, sales performance, product trends, payment preferences, and customer satisfaction.

The dataset contains information about customers, orders, products, sellers, payments, reviews, and geolocation data from a real-world e-commerce platform.

## Business Problem

E-commerce businesses generate large amounts of transactional data every day. Understanding customer behavior and sales performance is critical for improving decision-making and business growth.

This project aims to transform raw e-commerce data into actionable business insights.

## Business Questions

- What is the total revenue generated?
- How have sales changed over time?
- Which product categories generate the most revenue?
- Which states contribute the most sales?
- What payment methods are most frequently used?
- What is the average order value?
- How satisfied are customers based on review scores?
- Who are the most valuable customers?

## Dataset

Source: Kaggle - Brazilian E-Commerce Public Dataset by Olist

Tables used:
- Customers
- Orders
- Order Items
- Products
- Sellers
- Payments
- Reviews
- Product Category Translation
- Geolocation

## Entity Relationship Diagram (ERD)
![ERD](flowcharts\ERD.png)

### Table Relationships

```text
customers
    |
    | customer_id
    v
orders
    |
    | order_id
    +------------------+------------------+
    |                  |                  |
    v                  v                  v
order_items      order_payments    order_reviews
    |
    +------------------+
    |                  |
    v                  v
products          sellers
    |
    v
category_translation

customers
    |
    | customer_zip_code_prefix
    v
geolocation

sellers
    |
    | seller_zip_code_prefix
    v
geolocation
```

## Project Workflow

1. Data Understanding
2. Data Quality Assessment
3. Data Cleaning
4. Data Modeling
5. Exploratory Data Analysis
6. Customer Segmentation (RFM)
7. Dashboard Development
8. Business Insights & Recommendations

## Tools & Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Jupyter Notebook
- Streamlit

## Key Insights

### 1. Macro Financials & Payment Preferences
* **Healthy Transaction Baseline:** The marketplace maintains a steady, predictable core transaction engine with an average order value (AOV) that remains balanced across seasonal peaks.
* **Credit Superiority:** An overwhelming majority of customer transactions are processed via credit card, indicating a high consumer preference for installment options or deferred financing options over instant cash options like Boleto.

### 2. Fulfillment Performance & Customer Sentiment
* **The Logistics Deficit:** Delivery timelines show substantial variation throughout the year, with a clear lag during high-volume seasonal spikes.
* **The Attrition Penalty:** Orders suffering from negative fulfillment cushions (Actual Delivery > Promised SLA) experience an aggressive drop in customer satisfaction, collapsing average review scores to **~1.0 to 1.5 stars**, proving that logistical delays are the primary driver of negative platform sentiment.

### 3. Customer Retention & 3D RFM Dynamics
* **The Acquisition Machine:** Olist functions almost exclusively as a high-velocity acquisition pipeline. Approximately **96.9%** of the unique customer database consists of one-time buyers.
* **The Elite Core:** True repeat-buyer behavior ($F \ge 2$) is concentrated in a tiny **3.1%** layer of the ecosystem, divided among **Champions (1.12%)**, **At Risk (1.10%)**, and **Loyal Customers (0.91%)**.

---

## Dashboard

(Add dashboard here)

## Strategic Business Recommendations

Based on the interactive dashboards built across your core performance domains, Olist should deploy the following three operational plays:

### 🎯 1. Implement the "Second-Purchase Bridge" for High-Value First-Timers
* **Target:** *Potential Loyalists* (15.44% of the database) — recent, high-spending, single-purchase shoppers ($R \ge 4, M \ge 4, F = 1$).
* **Action:** Deploy automated, programmatic email and push-notification triggers within 14 days of successful initial delivery. Offer time-bounded vouchers (e.g., *"Get R$ 25 off your next checkout—expires in 7 days"*) to capture maximum user engagement and force single-buyers into repeat behaviors.

### 📉 2. Prevent Churn with Predictive Recommendation Loops
* **Target:** *Need Attention* (19.16% of the database) — moderate-spend, single-purchase buyers whose recency metrics are starting to drop.
* **Action:** Break down what these users originally bought and push personalized cross-category product offerings to their feeds before their recency slips entirely into the *Lost Customers* tier.

### 🚚 3. Protect Customer Sentiment with Dynamic Shipping SLA Guardrails
* **Target:** High-volume product categories suffering from systematic delivery delays.
* **Action:** Use your *Fulfillment Bottlenecks* analytics matrix to adjust estimated fulfillment dates during seasonal rushes. Setting safer delivery cushion windows protects customer expectations, prevents low review ratings, and avoids permanent brand attrition.
