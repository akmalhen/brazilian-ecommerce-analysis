import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import geopandas as gpd
from babel.numbers import format_currency
import os

sns.set(style='dark')

def create_monthly_performance_df(df):
    monthly_df = df.resample(rule='ME', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()
    monthly_df.rename(columns={"order_id": "order_count", "price": "revenue"}, inplace=True)
    return monthly_df

def create_product_performance_df(df):
    product_df = df.groupby("product_category_name_english").agg({
        "order_id": "nunique",
        "price": "sum"
    }).sort_values(by="order_id", ascending=False).reset_index()
    product_df.rename(columns={"order_id": "order_count", "price": "revenue"}, inplace=True)
    return product_df

def create_state_performance_df(df):
    state_df = df.groupby("customer_state").agg({
        "customer_unique_id": "nunique"
    }).sort_values(by="customer_unique_id", ascending=False).reset_index()
    state_df.rename(columns={"customer_unique_id": "customer_count"}, inplace=True)
    return state_df

@st.cache_data
def load_geojson(url):
    return gpd.read_file(url)

current_dir = os.path.dirname(os.path.realpath(__file__))
all_df = pd.read_csv(os.path.join(current_dir, "main_data.csv"))
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.title("Brazilian E-Commerce Dashboard")
    st.markdown("---")
    st.title("Filter Data")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

monthly_performance_df = create_monthly_performance_df(main_df)
product_performance_df = create_product_performance_df(main_df)
state_performance_df = create_state_performance_df(main_df)

st.title('Brazilian E-Commerce Dashboard')

with st.expander("Informasi Dataset & Tujuan Analisis"):
    st.write(
        """
        **Tentang Dataset:**  
        Ini adalah dataset publik e-commerce Brasil yang berisi pesanan yang dilakukan di **Olist Store**. Dataset ini memiliki informasi tentang 100.000 pesanan dari tahun 2016 hingga 2018 yang dilakukan di berbagai marketplace di Brasil.
        
        **Tujuan Analisis:**  
        Dashboard ini bertujuan untuk menjawab 3 pertanyaan bisnis:
        1. Bagaimana performa total pesanan dan pendapatan (revenue) perusahaan dalam beberapa bulan terakhir (2017 - 2018)?
        2. Bagaimana perbandingan performa antar berbagai kategori produk jika dilihat dari sisi volume pesanan dan total pendapatan yang dihasilkan selama tahun 2016 - 2018?
        3. Bagaimana distribusi geografis customer serta kontribusi total pengeluarannya di berbagai negara bagian Brasil sepanjang tahun 2016 - 2018?
        """
    )

tab1, tab2, tab3 = st.tabs(["Performa Penjualan", "Analisis Produk", "Distribusi Geografis"])

with tab1:
    st.header("Performa Penjualan & Pendapatan Bulanan")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Orders", value=monthly_performance_df.order_count.sum())
    with col2:
        total_rev = format_currency(monthly_performance_df.revenue.sum(), "BRL", locale='pt_BR')
        st.metric("Total Revenue", value=total_rev)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(monthly_performance_df["order_purchase_timestamp"], 
            monthly_performance_df["order_count"], 
            marker='o', 
            color="#72BCD4")

    ax.set_title("Total Orders per Month", fontsize=18)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Order Count", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_performance_df["order_purchase_timestamp"], 
            monthly_performance_df["revenue"], 
            marker='o', color="#8D432B")
            
    ax.set_title("Total Revenue per Month", fontsize=18)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Revenue", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)

    st.pyplot(fig)

with tab2:
    st.header("Product Category Analysis")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Total Items Sold", value=product_performance_df.order_count.sum())
    with col4:
        total_product_revenue = format_currency(product_performance_df.revenue.sum(), "BRL", locale='pt_BR')
        st.metric("Total Revenue", value=total_product_revenue)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    top_orders = product_performance_df.head(5).sort_values(by="order_count", ascending=True)

    ax.barh(top_orders["product_category_name_english"], 
            top_orders["order_count"], 
            color="#82bd92")
            
    ax.set_title("Top 15 Product Categories by Sales Volume", fontsize=18)
    ax.set_xlabel("Order Count", fontsize=12)
    ax.set_ylabel("Product Category", fontsize=12)
    ax.grid(True)

    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    top_revenue = product_performance_df.sort_values(by="revenue", ascending=False).head(5).sort_values(by="revenue", ascending=True)

    ax.barh(top_revenue["product_category_name_english"], 
            top_revenue["revenue"   ], 
            color="#bfad84")

    ax.set_title("Top 15 Product Categories by Revenue", fontsize=18)
    ax.set_xlabel("Revenue", fontsize=12)
    ax.set_ylabel("Product Category", fontsize=12)
    ax.grid(True)

    st.pyplot(fig)

with tab3:
    st.header("Distribusi Geografis Pelanggan")

    fig, ax = plt.subplots(figsize=(12, 12))
    top_states = state_performance_df.sort_values(by="customer_count", ascending=True)

    ax.barh(top_states["customer_state"], 
            top_states["customer_count"], 
            color="#e8aeb0")

    ax.set_title("States by Number of Customers", fontsize=18)
    ax.set_xlabel("Customer Count", fontsize=12)
    ax.set_ylabel("Customer State", fontsize=12)
    ax.grid(True)

    st.pyplot(fig)

    st.subheader("Customer Concentration per State")
    
    brazil_states_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    brazil_states = load_geojson(brazil_states_url)
    map_df = brazil_states.merge(state_performance_df, left_on="sigla", right_on="customer_state")

    fig, ax = plt.subplots(figsize=(10, 10))
    map_df.plot(column="customer_count", 
                cmap="YlOrRd", 
                legend=True, 
                legend_kwds={'label': "Number of Customers", 'orientation': "horizontal"}, 
                ax=ax, 
                edgecolor="black", 
                linewidth=0.5)

    for x, y, label in zip(map_df.geometry.representative_point().x, 
                            map_df.geometry.representative_point().y, 
                            map_df.sigla):
                            ax.text(x, y, label, fontsize=8, ha='center', color='black')

    plt.axis('off')

    st.pyplot(fig)
