import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# 1. PLATFORM CONFIGURATION & DARK MODE ENGINE
# ==========================================================
st.set_page_config(
    page_title="Olist Advanced Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom injection to force layout dark background and glowing scorecard typography
st.markdown("""
    <style>
    .main {background-color: #0f172a;}
    [data-testid="stMetricValue"] {font-size: 2.5rem; font-weight: 800; color: #38bdf8; letter-spacing: -0.5px;}
    [data-testid="stMetricLabel"] {font-size: 0.9rem; font-weight: 600; color: #94a3b8; text-transform: uppercase;}
    .stAlert {background-color: #1e293b; border-radius: 12px; border: 1px solid #334155;}
    h1, h2, h3, h4, h5, h6, p, span {color: #f8fafc !important;}
    div.block-container {padding-top: 1.5rem;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 2. DEFENSIVE CACHED DATA PIPELINE (Master & Payments)
# ==========================================================
@st.cache_data
def load_enterprise_data():
    # Load all analytical dependencies safely
    payments = pd.read_csv('clean_files/payments_clean.csv')
    order_pmts = pd.read_csv('clean_files/order_payments_clean.csv')
    rfm_df = pd.read_csv('clean_files/rfm_clean.csv')
    master = pd.read_csv('clean_files/master_clean.csv')
    
    # Standardize explicit timestamp formats
    payments['order_purchase_timestamp'] = pd.to_datetime(payments['order_purchase_timestamp'])
    payments['Year_Month'] = payments['order_purchase_timestamp'].dt.to_period('M').astype(str)
    payments['Year'] = payments['order_purchase_timestamp'].dt.year.astype(str)
    
    master['order_purchase_timestamp'] = pd.to_datetime(master['order_purchase_timestamp'])
    
    # Process isolated tracking properties if not present in input states
    if 'delivery_delta' not in master.columns and 'estimated_delivery_days' in master.columns and 'actual_delivery_days' in master.columns:
        master['delivery_delta'] = master['estimated_delivery_days'] - master['actual_delivery_days']
        
    return payments, order_pmts, rfm_df, master

try:
    payments_df, order_payments, rfm, master_df = load_enterprise_data()
except Exception as e:
    st.error(f"🚨 **Data Synchronization Interrupted:** Verify your pipeline has written 'payments_clean.csv', 'order_payments_clean.csv', 'rfm_clean.csv', and 'master_clean.csv' into your system directory. Trace: {e}")
    st.stop()

# Reusable Plotly layout configuration to apply dark-mode styling globally
def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#f8fafc',
        title_font=dict(size=14, color='#f8fafc', weight='bold'), # 🌟 FIXED HERE: Removed the extra nested dict
        xaxis=dict(gridcolor='#334155', title_font=dict(color='#94a3b8'), tickfont=dict(color='#cbd5e1')),
        yaxis=dict(gridcolor='#334155', title_font=dict(color='#94a3b8'), tickfont=dict(color='#cbd5e1')),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    return fig

# ==========================================================
# 3. SIDEBAR NAVIGATION CONSOLE
# ==========================================================
with st.sidebar:
    st.markdown("## ⚡ Navigation Deck")
    page = st.radio(
        "Select Performance View",
        [
            "📊 Financial Streams", 
            "🚚 Logistics & Operations", 
            "🛍️ Marketplace Slices",
            "🕰️ Temporal Shopping Behaviors",
            "👥 Cohort Segmentation"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 🎛️ Active Timeline Filters")
    available_years = sorted(payments_df['Year'].unique())
    selected_years = st.multiselect("Active Scope", available_years, default=available_years)

# Global data filtration masks
filtered_payments = payments_df[payments_df['Year'].isin(selected_years)]
filtered_master = master_df[master_df['order_purchase_timestamp'].dt.year.astype(str).isin(selected_years)]

# Dynamic Platform Metrics Card Values
total_revenue = filtered_payments['payment_value'].sum()
total_unique_orders = filtered_payments['order_id'].nunique()
calc_aov = total_revenue / total_unique_orders if total_unique_orders > 0 else 0

# ==========================================================
# 4. VIEW 1: FINANCIAL STREAMS
# ==========================================================
if page == "📊 Financial Streams":
    st.title("📊 Macro Financial Performance Streams")
    st.markdown("---")
    
    # KPI Scorecard Layout
    k1, k2, k3 = st.columns(3)
    k1.metric("Gross Revenue (GMV)", f"R$ {total_revenue:,.2f}")
    k2.metric("Unique Order Clearances", f"{total_unique_orders:,}")
    k3.metric("True Average Order Value (AOV)", f"R$ {calc_aov:,.2f}")
    
    st.markdown("---")
    
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        st.subheader("📈 Chronological Monthly Sales Trend Line")
        monthly_sales = filtered_payments.groupby('Year_Month')['payment_value'].sum().reset_index().sort_values('Year_Month')
        monthly_sales.columns = ['Year_Month', 'Total_Revenue_BRL']
        
        fig_trend = px.line(monthly_sales, x='Year_Month', y='Total_Revenue_BRL', markers=True, color_discrete_sequence=['#38bdf8'])
        st.plotly_chart(apply_dark_theme(fig_trend), use_container_width=True)
        
    with f_col2:
        st.subheader("🗓️ Seasonal Baseline Aggregations (Jan - Dec)")
        filtered_payments_cp = filtered_payments.copy()
        filtered_payments_cp['order_month_name'] = filtered_payments_cp['order_purchase_timestamp'].dt.strftime('%B')
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
        seasonal_sales = filtered_payments_cp.groupby('order_month_name')['payment_value'].sum().reindex(index=month_order).reset_index()
        fig_season = px.bar(seasonal_sales, x='order_month_name', y='payment_value', color_discrete_sequence=['#6366f1'])
        st.plotly_chart(apply_dark_theme(fig_season), use_container_width=True)

# ==========================================================
# 5. VIEW 2: LOGISTICS & OPERATIONS
# ==========================================================
elif page == "🚚 Logistics & Operations":
    st.title("🚚 Delivery Pipeline Efficiency & Sentiment Vectors")
    st.markdown("---")
    
    # Process delivery data safely out of master_df / payments fallback frames
    filtered_master_delivered = filtered_master[filtered_master['order_status'] == 'delivered'].copy()
    filtered_master_delivered['order_year_month_str'] = filtered_master_delivered['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        st.subheader("🗓️ Logistical Deviation Tracking: Actual vs Promised Days")
        delivery_trend = filtered_master_delivered.groupby('order_year_month_str')[['actual_delivery_days', 'estimated_delivery_days']].mean().reset_index()
        
        fig_logistics = go.Figure()
        fig_logistics.add_trace(go.Scatter(x=delivery_trend['order_year_month_str'], y=delivery_trend['estimated_delivery_days'], name='SLA Promised Days', line=dict(color='#94a3b8', dash='dash', width=2)))
        fig_logistics.add_trace(go.Scatter(x=delivery_trend['order_year_month_str'], y=delivery_trend['actual_delivery_days'], name='Actual Delivery Days', line=dict(color='#4ade80', width=3)))
        st.plotly_chart(apply_dark_theme(fig_logistics), use_container_width=True)
        
    with l_col2:
        st.subheader("🎯 Direct Impact of Logistics Exceptions on Review Scores")
        filtered_master_delivered['is_late'] = filtered_master_delivered['delivery_delta'].apply(lambda x: 'Late' if x < 0 else 'On-Time')
        late_vs_ontime = filtered_master_delivered.groupby('is_late').agg(avg_score=('review_score', 'mean')).reset_index()
        
        fig_rating = px.bar(late_vs_ontime, x='is_late', y='avg_score', color='is_late', color_discrete_map={'Late': '#f43f5e', 'On-Time': '#10b981'}, text_auto='.2f')
        fig_rating.update_layout(yaxis=dict(range=[1, 5]))
        st.plotly_chart(apply_dark_theme(fig_rating), use_container_width=True)

# ==========================================================
# 6. VIEW 3: MARKETPLACE SLICES
# ==========================================================
elif page == "🛍️ Marketplace Slices":
    st.title("🛍️ Category Volume Matrices & Payment Method Splits")
    st.markdown("---")
    
    # Calculate Payment Distribution details
    pay_summary = order_payments['payment_type'].value_counts(normalize=True).reset_index()
    pay_summary.columns = ['payment_type', 'percentage']
    pay_summary['percentage'] *= 100
    
    # Category Analytics Data Frame
    category_summary = filtered_master.groupby('product_category_name_english').agg(
        total_revenue=('price', 'sum'),
        total_orders=('order_id', 'nunique')
    ).reset_index()
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.subheader("💳 Platform Checkout Method Distribution")
        fig_pay = px.bar(pay_summary, x='percentage', y='payment_type', orientation='h', color_discrete_sequence=['#38bdf8'], text_auto='.2f')
        fig_pay.update_layout(xaxis=dict(range=[0, 100]), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_dark_theme(fig_pay), use_container_width=True)
        
    with p_col2:
        st.subheader("💰 Top 10 Marketplace Revenue Drivers")
        top_rev_cat = category_summary.sort_values(by='total_revenue', ascending=False).head(10)
        fig_cat_rev = px.bar(top_rev_cat, x='product_category_name_english', y='total_revenue', color_discrete_sequence=['#6366f1'])
        st.plotly_chart(apply_dark_theme(fig_cat_rev), use_container_width=True)
        
    st.markdown("---")
    
    p_col3, p_col4 = st.columns(2)
    with p_col3:
        st.subheader("📦 Top 10 Product Categories by Transaction Volume")
        top_vol_cat = category_summary.sort_values(by='total_orders', ascending=False).head(10)
        fig_cat_vol = px.bar(top_vol_cat, x='total_orders', y='product_category_name_english', orientation='h', color_discrete_sequence=['#a855f7'])
        fig_cat_vol.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_dark_theme(fig_cat_vol), use_container_width=True)
        
    with p_col4:
        st.subheader("⚠️ Top 10 Systemic Bottlenecks: Weakest Shipping Cushion Categories")
        categories_perf = filtered_master.groupby('product_category_name_english').agg(
            total_orders=('order_id', 'nunique'),
            avg_delivery_delta=('delivery_delta', 'mean')
        ).reset_index()
        # Ensure robust evaluation threshold
        frequent_cats = categories_perf[categories_perf['total_orders'] > 100]
        worst_shipping = frequent_cats.sort_values(by='avg_delivery_delta', ascending=True).head(10)
        
        fig_bottleneck = px.bar(worst_shipping, x='avg_delivery_delta', y='product_category_name_english', orientation='h', color_discrete_sequence=['#f43f5e'])
        fig_bottleneck.update_layout(yaxis={'categoryorder':'total descending'})
        st.plotly_chart(apply_dark_theme(fig_bottleneck), use_container_width=True)

# ==========================================================
# 7. VIEW 4: TEMPORAL SHOPPING BEHAVIORS
# ==========================================================
elif page == "🕰️ Temporal Shopping Behaviors":
    st.title("🕰️ Hourly and Weekly Demand Fluctuations")
    st.markdown("---")
    
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.subheader("🕒 The Buying Clock: Transaction Distributions Across 24 Hours")
        hourly_orders = filtered_master.groupby('order_hour')['order_id'].nunique().reset_index()
        hourly_orders.columns = ['hour_of_day', 'total_orders']
        
        fig_hour = px.line(hourly_orders, x='hour_of_day', y='total_orders', color_discrete_sequence=['#38bdf8'])
        fig_hour.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        st.plotly_chart(apply_dark_theme(fig_hour), use_container_width=True)
        
    with t_col2:
        st.subheader("🗓️ Weekly Distribution Patterns")
        weekly_orders = filtered_master.groupby('order_day_name')['order_id'].nunique().reset_index()
        weekly_orders.columns = ['day_of_week', 'total_orders']
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_orders['day_of_week'] = pd.Categorical(weekly_orders['day_of_week'], categories=day_order, ordered=True)
        weekly_orders = weekly_orders.sort_values('day_of_week')
        
        fig_week = px.bar(weekly_orders, x='day_of_week', y='total_orders', color_discrete_sequence=['#facc15'])
        st.plotly_chart(apply_dark_theme(fig_week), use_container_width=True)

# ==========================================================
# 8. VIEW 5: COHORT SEGMENTATION
# ==========================================================
elif page == "👥 Cohort Segmentation":
    st.title("👥 Customer Loyalty Breakdown & Custom 3D RFM Matrix")
    st.markdown("---")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.subheader("🎯 Marketplace Lifetime Engagement Funnel")
        cust_counts = filtered_master.groupby('customer_unique_id')['order_id'].nunique().reset_index()
        cust_counts.columns = ['customer_unique_id', 'order_count']
        cust_counts['customer_type'] = cust_counts['order_count'].apply(lambda x: 'One-Time Customer' if x == 1 else 'Repeat Customer')
        
        loyalty = cust_counts['customer_type'].value_counts().reset_index()
        loyalty.columns = ['customer_type', 'count']
        
        # Interactive dark-themed Donut/Pie setup
        fig_pie = px.pie(loyalty, values='count', names='customer_type', hole=0.4, color_discrete_sequence=['#475569', '#38bdf8'])
        st.plotly_chart(apply_dark_theme(fig_pie), use_container_width=True)
        
    with c_col2:
        st.subheader("📊 Complete Custom 3D RFM Structural Distribution")
        segment_summary = rfm['Segment'].value_counts().reset_index()
        segment_summary.columns = ['Customer Segment', 'Total Customers']
        segment_summary['Percentage Share'] = (segment_summary['Total Customers'] / len(rfm)) * 100
        
        fig_rfm = px.bar(segment_summary, x='Total Customers', y='Customer Segment', orientation='h', color='Percentage Share', color_continuous_scale='Blues')
        fig_rfm.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(apply_dark_theme(fig_rfm), use_container_width=True)
        
    st.markdown("---")
    st.subheader("📋 Core Audit Data Ledger")
    st.dataframe(segment_summary.style.format({'Total Customers': '{:,}', 'Percentage Share': '{:.2f}%'}), use_container_width=True)
