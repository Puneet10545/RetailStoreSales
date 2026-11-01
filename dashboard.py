
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="Retail Store Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("SuperMarket Analysis.csv")

    data["Date"] = pd.to_datetime(
        data["Date"],
        format="%m/%d/%Y"
    )

    data["Month"] = data["Date"].dt.month_name()
    data["Day"] = data["Date"].dt.day_name()

    return data


df = load_data()

# --------------------------------------------------
# 3. DASHBOARD TITLE
# --------------------------------------------------
st.title("🛒 Retail Store Sales Analysis")
st.write("Interactive dashboard for retail store sales performance.")

# --------------------------------------------------
# 4. SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

# City filter
city_options = sorted(df["City"].unique())

selected_city = st.sidebar.multiselect(
    "Select City",
    options=city_options,
    default=city_options
)

# Product Line filter
product_options = sorted(df["Product line"].unique())

selected_product = st.sidebar.multiselect(
    "Select Product Line",
    options=product_options,
    default=product_options
)

# Date filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_date = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# --------------------------------------------------
# 5. FILTER DATA
# --------------------------------------------------
filtered_df = df[
    (df["City"].isin(selected_city)) &
    (df["Product line"].isin(selected_product))
].copy()

# Apply date filter only when start and end dates are selected
if isinstance(selected_date, (tuple, list)) and len(selected_date) == 2:
    start_date, end_date = selected_date

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date) &
        (filtered_df["Date"].dt.date <= end_date)
    ]

# --------------------------------------------------
# 6. KEY METRICS
# --------------------------------------------------
st.subheader("Key Business Metrics")

total_sales = filtered_df["Sales"].sum()
total_income = filtered_df["gross income"].sum()
total_transactions = filtered_df["Invoice ID"].nunique()

if len(filtered_df) > 0:
    average_rating = filtered_df["Rating"].mean()
else:
    average_rating = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Gross Income", f"${total_income:,.2f}")
col3.metric("Transactions", f"{total_transactions:,}")
col4.metric("Average Rating", f"{average_rating:.2f}/10")

st.divider()

# --------------------------------------------------
# 7. SALES BY PRODUCT LINE
# --------------------------------------------------
st.subheader("Sales by Product Line")

if not filtered_df.empty:

    product_sales = (
        filtered_df.groupby("Product line")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    product_sales.plot(
        kind="bar",
        ax=ax1
    )

    ax1.set_xlabel("Product Line")
    ax1.set_ylabel("Total Sales")
    ax1.set_title("Total Sales by Product Line")
    ax1.tick_params(axis="x", rotation=45)

    fig1.tight_layout()

    st.pyplot(fig1)
    plt.close(fig1)

else:
    st.warning("No data available for the selected filters.")

# --------------------------------------------------
# 8. MONTHLY SALES
# --------------------------------------------------
st.subheader("Monthly Sales Analysis")

if not filtered_df.empty:

    monthly_sales = filtered_df.groupby("Month")["Sales"].sum()

    month_order = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]

    monthly_sales = monthly_sales.reindex(month_order).dropna()

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    monthly_sales.plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_xlabel("Month")
    ax2.set_ylabel("Total Sales")
    ax2.set_title("Monthly Sales")
    ax2.tick_params(axis="x", rotation=45)

    fig2.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)

else:
    st.warning("No monthly sales data available.")

# --------------------------------------------------
# 9. DATASET PREVIEW
# --------------------------------------------------
st.subheader("Dataset Preview")

st.write(
    f"Showing {len(filtered_df)} records out of {len(df)} total records."
)

st.dataframe(
    filtered_df,
    use_container_width=True
)

# --------------------------------------------------
# 10. DOWNLOAD FILTERED DATA
# --------------------------------------------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_retail_sales.csv",
    mime="text/csv"
)
