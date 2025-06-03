
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

df = pd.read_csv('global_ev_sales.csv')  # Ensure this file exists in the working directory

print("First 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
print("\nCleaned Column Names:", df.columns.tolist())

df_sales = df[(df['parameter'].str.lower() == 'ev sales') & (df['unit'].str.lower() == 'vehicles')].copy()

print("\nFiltered EV sales data sample:")
print(df_sales.head())

df_sales['year'] = pd.to_numeric(df_sales['year'], errors='coerce')
df_sales['value'] = pd.to_numeric(df_sales['value'], errors='coerce')
df_sales.dropna(subset=['year', 'value'], inplace=True)
df_sales['year'] = df_sales['year'].astype(int)

sales_by_year = df_sales.groupby('year')['value'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x='year', y='value', data=sales_by_year, marker='o')
plt.title('Global EV Sales Over Years')
plt.xlabel('Year')
plt.ylabel('EV Sales (Units)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

if 'region' in df_sales.columns:
    region_sales = df_sales.groupby('region')['value'].sum().reset_index()
    region_sales = region_sales.sort_values(by='value', ascending=False).head(10)

    # Create a unique color for each bar (10 regions)
    palette = sns.color_palette("viridis", n_colors=10)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=region_sales, x='value', y='region', hue='region', dodge=False, palette=palette, legend=False)
    plt.title('Top 10 Regions by EV Sales')
    plt.xlabel('Total Sales')
    plt.ylabel('Region')
    plt.tight_layout()
    plt.show()

sales_by_year['YoY_growth'] = sales_by_year['value'].pct_change() * 100
print("\nYear-over-Year Growth Rates:")
print(sales_by_year)

plt.figure(figsize=(10, 5))
sns.barplot(data=sales_by_year, x='year', y='YoY_growth', hue='year', dodge=False, palette='coolwarm', legend=False)
plt.title('Year-over-Year EV Sales Growth (%)')
plt.ylabel('Growth Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

