import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('superstore_sales.csv')
if 'Data Ordem' in df.columns:
    df.columns = ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
                  'Customer ID', 'Customer Name', 'Segment', 'Country', 'City',
                  'State', 'Postal Code', 'Region', 'Product ID', 'Category',
                  'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']

df['Order Date'] = pd.to_datetime(df['Order Date'])

# 以数据最后一天+1天作为参考日期
reference_date = df['Order Date'].max() + pd.Timedelta(days=1)

# 计算 RFM 指标
rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (reference_date - x.max()).days,  # Recency
    'Order ID': 'nunique',                                     # Frequency
    'Sales': 'sum'                                             # Monetary
}).reset_index()
rfm.columns = ['Customer ID', 'Recency', 'Frequency', 'Monetary']

print("=== RFM 统计 ===")
print(rfm[['Recency', 'Frequency', 'Monetary']].describe())

# K-Means 聚类（3类）
features = rfm[['Recency', 'Frequency', 'Monetary']]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(features_scaled)

# 查看各簇特征
cluster_summary = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
print("\n=== 聚类结果 ===")
print(cluster_summary)

# 3D 散点图展示分群
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

colors = ['#2E86AB', '#A23B72', '#F18F01']
labels = ['Low Value', 'Medium Value', 'High Value']

for c in range(3):
    subset = rfm[rfm['Cluster'] == c]
    ax.scatter(subset['Recency'], subset['Frequency'], subset['Monetary'],
               c=colors[c], label=labels[c], alpha=0.6, s=30)

ax.set_xlabel('Recency (days)')
ax.set_ylabel('Frequency (orders)')
ax.set_zlabel('Monetary ($)')
ax.set_title('RFM Customer Segmentation', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('chart6_rfm_clustering.png', dpi=150)
print("图6 RFM已保存")

