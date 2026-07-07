import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('superstore_sales.csv')
if 'Data Ordem' in df.columns:
    df.columns = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
                  'Customer ID', 'Customer Name', 'Segment', 'Country', 'City',
                  'State', 'Postal Code', 'Region', 'Product ID', 'Category',
                  'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']

df['Order Date'] = pd.to_datetime(df['Order Date'])
weekly = df.resample('W', on='Order Date')['Sales'].sum()

# 指数平滑预测 (Holt's method)
alpha = 0.3  # 水平平滑参数
beta = 0.1   # 趋势平滑参数

# 初始化
level = weekly.iloc[0]
trend = weekly.iloc[1] - weekly.iloc[0]
fitted = [level + trend]

# 拟合历史
for i in range(1, len(weekly)):
    prev_level = level
    level = alpha * weekly.iloc[i] + (1 - alpha) * (level + trend)
    trend = beta * (level - prev_level) + (1 - beta) * trend
    fitted.append(level + trend)

# 预测未来12周
n_forecast = 12
forecast = []
for i in range(n_forecast):
    forecast.append(level + trend * (i + 1))

# 生成预测日期
last_date = weekly.index[-1]
forecast_dates = pd.date_range(start=last_date + pd.Timedelta(weeks=1), periods=n_forecast, freq='W')

# 绘图
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(weekly.index, weekly.values, label='Actual Sales', color='#2E86AB', linewidth=1.5)
ax.plot(weekly.index, fitted, label='Fitted', color='#F18F01', linewidth=1, alpha=0.7)
ax.plot(forecast_dates, forecast, label='Forecast', color='#A23B72', linewidth=2, linestyle='--')
ax.axvline(x=last_date, color='gray', linestyle=':', alpha=0.7)

ax.set_title('Sales Forecast (Exponential Smoothing)', fontsize=14, fontweight='bold')
ax.set_xlabel('Date')
ax.set_ylabel('Weekly Sales ($)')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('chart7_forecast.png', dpi=150)
print("图7 预测已保存")
print(f"\n未来12周预测:")
for d, v in zip(forecast_dates, forecast):
    print(f"  {d.strftime('%Y-%m-%d')}: ${v:,.2f}")