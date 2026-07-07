import numpy as np
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('superstore_sales.csv')

if 'Data Ordem' in df.columns:
    df.columns = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
                  'Customer ID', 'Customer Name', 'Segment', 'Country', 'City',
                  'State', 'Postal Code', 'Region', 'Product ID', 'Category',
                  'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']

df['Order Date'] = pd.to_datetime(df['Order Date'])
monthly = df.resample('ME', on='Order Date')['Sales'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly['Order Date'], monthly['Sales'], marker='o', color='#2E86AB', linewidth=2)
ax.fill_between(monthly['Order Date'], monthly['Sales'], alpha=0.15, color='#2E86AB')
ax.set_title('Monthly Sales Trend (2017)', fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Sales ($)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('chart1_monthly_sales_trend.png', dpi=150)
print("图1已保存")

cat_summary = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()

positions = np.arange(len(cat_summary))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(positions - width/2, cat_summary['Sales'], width, label='Sales', color='#2E86AB')
bars2 = ax.bar(positions + width/2, cat_summary['Profit'], width, label='Profit', color='#A23B72')

ax.set_xticks(positions)
ax.set_xticklabels(cat_summary['Category'])
ax.set_title('Sales vs Profit by Category', fontsize=14, fontweight='bold')
ax.set_ylabel('Amount ($)')
ax.legend()

for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
            f'${bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
            f'${bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8)

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('chart2_category_sales_profit.png', dpi=150)
print("图2已保存")

# 按地区汇总
region_summary = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
region_summary = region_summary.sort_values('Sales', ascending=True)

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#A23B72', '#F18F01', '#C73E1D', '#2E86AB']
bars = ax.barh(region_summary['Region'], region_summary['Sales'], color=colors[:len(region_summary)])

ax.set_title('Sales by Region', fontsize=14, fontweight='bold')
ax.set_xlabel('Sales ($)')

for bar in bars:
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'${bar.get_width():,.0f}', ha='left', va='center', fontsize=9)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('chart3_region_sales.png', dpi=150)
print("图3已保存")
top10 = df.groupby('Sub-Category')['Sales'].sum().nlargest(10).sort_values(ascending=True)

top10 = df.groupby('Sub-Category')['Sales'].sum().nlargest(10).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(top10.index, top10.values, color='#3A86FF')

ax.set_title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')
ax.set_xlabel('Sales ($)')

for bar in bars:
    ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
            f'${bar.get_width():,.0f}', ha='left', va='center', fontsize=8)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('chart4_top10_subcategory.png', dpi=150)
print("图4已保存")

cat_summary = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
cat_summary['Profit Margin'] = cat_summary['Profit'] / cat_summary['Sales'] * 100

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#2E86AB' if x >= 0 else '#A23B72' for x in cat_summary['Profit Margin']]
bars = ax.bar(cat_summary['Category'], cat_summary['Profit Margin'], color=colors)

ax.set_title('Profit Margin by Category', fontsize=14, fontweight='bold')
ax.set_ylabel('Profit Margin (%)')
ax.axhline(y=0, color='black', linewidth=0.5)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2,
            height + (1 if height >= 0 else -2),
            f'{height:.1f}%', ha='center', va='bottom' if height >= 0 else 'top',
            fontsize=10, fontweight='bold')

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('chart5_profit_margin.png', dpi=150)
print("图5已保存")