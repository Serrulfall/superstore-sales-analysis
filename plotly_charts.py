import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('superstore_sales.csv')
if 'Data Ordem' in df.columns:
    df.columns = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
                  'Customer ID', 'Customer Name', 'Segment', 'Country', 'City',
                  'State', 'Postal Code', 'Region', 'Product ID', 'Category',
                  'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']

df['Order Date'] = pd.to_datetime(df['Order Date'])

# 图1: 交互式月度趋势（带 hover）
monthly = df.resample('ME', on='Order Date')['Sales'].sum().reset_index()
fig1 = px.line(monthly, x='Order Date', y='Sales', title='Monthly Sales Trend (Interactive)')
fig1.update_layout(template='plotly_white')
fig1.write_html('interactive_chart1_monthly_sales.html')

# 图2: 交互式品类气泡图（X=销售额, Y=利润, 气泡大小=订单量, 颜色=品类）
cat_bubble = df.groupby('Category').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique')
).reset_index()
fig2 = px.scatter(cat_bubble, x='Sales', y='Profit', size='Orders', color='Category',
                  title='Category Performance Bubble Chart',
                  hover_data=['Orders'], size_max=60)
fig2.update_layout(template='plotly_white')
fig2.write_html('interactive_chart2_category_bubble.html')

print("2张交互图已保存，双击 HTML 文件在浏览器打开")