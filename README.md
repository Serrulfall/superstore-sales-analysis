# Superstore Sales Analysis

基于 Superstore 零售数据集（9,994条订单记录），使用 Python + Pandas 进行数据清洗与探索性分析，通过 Matplotlib 生成 5 张可视化图表，揭示销售趋势、品类表现及地区差异。

## 数据源

Superstore Sales Dataset，包含 2017 年 1 月至 9 月共 9,994 条订单记录，涵盖订单信息、客户、产品、地区、销售额、利润等 21 个字段。

## 可视化图表

| 图表 | 说明 |
|------|------|
| 月度销售趋势 | 按月聚合销售额，展示整体销售走势与季节性波动 |
| 品类销售与利润对比 | 分品类对比销售额与利润，揭示各品类盈利能力差异 |
| 地区销售分布 | 横向对比 East/West/Central/South 四大区域的销售表现 |
| Top 10 子品类 | 识别销售额最高的 10 个产品子品类 |
| 品类利润率对比 | 对比各品类利润率，发现 Furniture 利润率极低（<1%） |

## 关键发现

- **Technology** 品类销售额最高（$456K），利润率最优（~21%）
- **Furniture** 销售额排名第二，但利润率仅约 0.6%，主要受高折扣影响
- **West** 地区销售额领先，**South** 地区表现最弱
- **Phones** 是销售额最高的子品类，其次是 Chairs 和 Storage

## 技术栈

- Python 3.10
- Pandas — 数据处理与聚合
- Matplotlib — 数据可视化

## 文件结构
    ├── superstore_sales.csv # 原始数据
    ├── chart1_monthly_sales_trend.png
    ├── chart2_category_sales_profit.png
    ├── chart3_region_sales.png
    ├── chart4_top10_subcategory.png
    ├── chart5_profit_margin.png
    └── README.md