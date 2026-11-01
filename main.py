
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load dataset
df = pd.read_csv("SuperMarket Analysis.csv")

# 2. Basic dataset information
print("\n--- DATASET INFORMATION ---")
print("Dataset shape:", df.shape)
print("Column names:", df.columns.tolist())
df.info()

# 3. Check missing values and duplicates
print("\n--- DATA CLEANING CHECK ---")
print("Missing values:")
print(df.isnull().sum())

print("Duplicate rows:", df.duplicated().sum())

# 4. Convert Date column
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m/%d/%Y"
)

# 5. Create Month and Day columns
df["Month"] = df["Date"].dt.month_name()
df["Day"] = df["Date"].dt.day_name()

print("\n--- DATE CHECK ---")
print(df[["Date", "Month", "Day"]].head())

# 6. Calculate key business metrics
total_sales = df["Sales"].sum()
total_gross_income = df["gross income"].sum()
total_transactions = df["Invoice ID"].nunique()

print("\n--- KEY BUSINESS METRICS ---")
print("Total Sales:", round(total_sales, 2))
print("Total Gross Income:", round(total_gross_income, 2))
print("Total Transactions:", total_transactions)

# 7. Sales by Product Line
product_sales = (
    df.groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- SALES BY PRODUCT LINE ---")
print(product_sales)

# 8. Monthly Sales Analysis
monthly_sales = df.groupby("Month")["Sales"].sum()

month_order = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
]

monthly_sales = monthly_sales.reindex(month_order).dropna()

print("\n--- MONTHLY SALES ---")
print(monthly_sales)

# 9. Product Line Sales Chart
plt.figure(figsize=(10, 6))

product_sales.plot(kind="bar")

plt.title("Total Sales by Product Line")
plt.xlabel("Product Line")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("product_sales.png")
plt.show()
plt.close()

# 10. Monthly Sales Chart
plt.figure(figsize=(10, 6))

monthly_sales.plot(kind="bar")

plt.title("Monthly Sales Analysis")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("monthly_sales.png")
plt.show()
plt.close()

print("\nAnalysis completed successfully!")
print("Charts saved as product_sales.png and monthly_sales.png")
