# Tutorial 02: Pandas DataFrames for Financial Analytics

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Create and manipulate Pandas DataFrames
- Filter and select data efficiently
- Perform aggregations and grouping operations
- Merge and join multiple datasets
- Apply real Quantyf data processing techniques

---

## 🎯 Why Pandas?

**Pandas is THE data analysis library for Python**. In Quantyf, we use Pandas for:
- Loading CSV/Excel data (demands, centers, vehicles)
- Data cleaning and transformation
- Calculating costs and distances
- Aggregating results
- Merging multiple data sources

Think of Pandas DataFrames as **Excel on steroids** - all the power of spreadsheets with Python's flexibility!

---

## 1. Creating DataFrames

### From Dictionaries

```python
import pandas as pd

# Create route data
routes_data = {
    'origin': ['Mumbai', 'Delhi', 'Kolkata', 'Chennai'],
    'destination': ['Delhi', 'Kolkata', 'Chennai', 'Mumbai'],
    'distance_km': [1400, 1450, 1670, 1340],
    'cost': [35000, 36250, 41750, 33500]
}

df_routes = pd.DataFrame(routes_data)
print(df_routes)
```

Output:
```
     origin destination  distance_km    cost
0    Mumbai       Delhi         1400   35000
1     Delhi     Kolkata         1450   36250
2   Kolkata     Chennai         1670   41750
3   Chennai      Mumbai         1340   33500
```

### From CSV Files (Real Quantyf Use Case)

```python
# Read demand data (like Quantyf does)
df_demands = pd.read_csv('demands.csv')

# Common parameters
df = pd.read_csv(
    'data.csv',
    sep=',',              # Delimiter
    header=0,             # First row is header
    encoding='utf-8',     # Character encoding
    parse_dates=['date'], # Parse date columns
    na_values=['', 'NA', 'null']  # Treat these as missing values
)
```

### Quick Dataset Creation for Practice

```python
# Create sample demand data
import numpy as np

df_demands = pd.DataFrame({
    'demand_id': range(1, 11),
    'source': np.random.choice(['Mumbai', 'Delhi', 'Bangalore'], 10),
    'destination': np.random.choice(['Chennai', 'Kolkata', 'Hyderabad'], 10),
    'pallets': np.random.randint(50, 200, 10),
    'priority': np.random.choice(['High', 'Medium', 'Low'], 10),
    'date': pd.date_range('2025-01-01', periods=10)
})

print(df_demands.head())
```

---

## 2. Exploring DataFrames

### Basic Information

```python
# DataFrame shape (rows, columns)
print(f"Shape: {df_demands.shape}")  # (10, 6)

# Column names
print(f"Columns: {df_demands.columns.tolist()}")

# Data types
print(df_demands.dtypes)

# First few rows
print(df_demands.head())  # Default: 5 rows
print(df_demands.head(3))  # First 3 rows

# Last few rows
print(df_demands.tail())

# Random sample
print(df_demands.sample(3))  # 3 random rows
```

### Statistical Summary

```python
# Numerical columns summary
print(df_demands.describe())

# Count non-null values
print(df_demands.count())

# Check for missing values
print(df_demands.isnull().sum())

# Unique values in a column
print(df_demands['source'].unique())
print(f"Number of unique sources: {df_demands['source'].nunique()}")

# Value counts (frequency)
print(df_demands['priority'].value_counts())
```

---

## 3. Selecting Data

### Selecting Columns

```python
# Single column (returns Series)
sources = df_demands['source']
print(type(sources))  # pandas.Series

# Single column (returns DataFrame)
sources_df = df_demands[['source']]
print(type(sources_df))  # pandas.DataFrame

# Multiple columns
subset = df_demands[['source', 'destination', 'pallets']]
print(subset.head())

# Select columns by position
first_three_cols = df_demands.iloc[:, :3]
```

### Selecting Rows

```python
# By position (iloc)
first_row = df_demands.iloc[0]
first_five_rows = df_demands.iloc[0:5]
specific_rows = df_demands.iloc[[0, 2, 4]]  # Rows 0, 2, 4

# By label (loc)
df_indexed = df_demands.set_index('demand_id')
row_by_id = df_indexed.loc[1]  # demand_id = 1

# Conditional selection (filtering)
high_priority = df_demands[df_demands['priority'] == 'High']
large_shipments = df_demands[df_demands['pallets'] > 100]

# Multiple conditions
high_volume = df_demands[
    (df_demands['priority'] == 'High') & 
    (df_demands['pallets'] > 150)
]

# Using isin()
specific_sources = df_demands[
    df_demands['source'].isin(['Mumbai', 'Delhi'])
]
```

### Real Quantyf Example: Filter Active Routes

```python
# Sample routes data
df_routes = pd.DataFrame({
    'route_id': range(1, 6),
    'origin': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
    'destination': ['Delhi', 'Kolkata', 'Mumbai', 'Bangalore', 'Chennai'],
    'status': ['active', 'inactive', 'active', 'active', 'maintenance'],
    'distance_km': [1400, 1450, 840, 350, 1670],
    'avg_cost': [35000, 36250, 21000, 8750, 41750]
})

# Filter active routes under 1000 km
efficient_routes = df_routes[
    (df_routes['status'] == 'active') & 
    (df_routes['distance_km'] < 1000)
]

print("Efficient Active Routes:")
print(efficient_routes[['origin', 'destination', 'distance_km', 'avg_cost']])
```

---

## 4. Adding and Modifying Data

### Adding New Columns

```python
# Add calculated column
df_routes['cost_per_km'] = df_routes['avg_cost'] / df_routes['distance_km']

# Add column with constant value
df_routes['currency'] = 'INR'

# Conditional column (like Excel IF)
df_routes['category'] = df_routes['distance_km'].apply(
    lambda x: 'Short' if x < 500 else ('Medium' if x < 1200 else 'Long')
)

# Using np.where (more efficient)
import numpy as np
df_routes['is_expensive'] = np.where(
    df_routes['cost_per_km'] > 25,
    'Yes',
    'No'
)
```

### Real Quantyf Example: Calculate Transportation Costs

```python
# Load vehicle data
df_vehicles = pd.DataFrame({
    'vehicle_type': ['Small Truck', 'Medium Truck', 'Large Truck', 'Container'],
    'capacity_pallets': [50, 100, 150, 200],
    'cost_per_km': [15, 22, 30, 40],
    'fixed_cost': [500, 800, 1200, 1500]
})

# Calculate total cost for a 1000 km journey
distance = 1000

df_vehicles['variable_cost'] = df_vehicles['cost_per_km'] * distance
df_vehicles['total_cost'] = df_vehicles['fixed_cost'] + df_vehicles['variable_cost']
df_vehicles['cost_per_pallet'] = df_vehicles['total_cost'] / df_vehicles['capacity_pallets']

print(df_vehicles[['vehicle_type', 'total_cost', 'cost_per_pallet']])
```

### Updating Existing Data

```python
# Update single value
df_routes.loc[0, 'status'] = 'active'

# Update based on condition
df_routes.loc[df_routes['distance_km'] > 1500, 'category'] = 'Very Long'

# Update multiple columns
df_routes.loc[df_routes['status'] == 'maintenance', ['status', 'avg_cost']] = [
    'inactive', 0
]

# Apply function to column
df_routes['origin'] = df_routes['origin'].str.upper()
```

---

## 5. Aggregations and Grouping

### Basic Aggregations

```python
# Sum, mean, min, max
total_pallets = df_demands['pallets'].sum()
avg_pallets = df_demands['pallets'].mean()
min_pallets = df_demands['pallets'].min()
max_pallets = df_demands['pallets'].max()

print(f"Total: {total_pallets}, Average: {avg_pallets:.2f}")

# Multiple aggregations at once
stats = df_demands['pallets'].agg(['sum', 'mean', 'min', 'max', 'std'])
print(stats)
```

### GroupBy Operations (Critical for Analytics!)

```python
# Group by single column
demand_by_source = df_demands.groupby('source')['pallets'].sum()
print("Total pallets by source:")
print(demand_by_source)

# Group by multiple columns
demand_summary = df_demands.groupby(['source', 'destination'])['pallets'].agg([
    'sum', 'mean', 'count'
])
print(demand_summary)

# Multiple aggregations on different columns
summary = df_demands.groupby('source').agg({
    'pallets': ['sum', 'mean'],
    'demand_id': 'count'
})
print(summary)
```

### Real Quantyf Example: Analyze Route Economics

```python
# Sample data with multiple routes and shipments
df_shipments = pd.DataFrame({
    'route': ['Mumbai-Delhi', 'Mumbai-Delhi', 'Delhi-Kolkata', 
              'Delhi-Kolkata', 'Mumbai-Delhi', 'Delhi-Kolkata'],
    'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-01',
                            '2025-01-02', '2025-01-03', '2025-01-03']),
    'pallets': [100, 150, 120, 90, 180, 110],
    'cost': [25000, 37500, 27000, 20250, 45000, 24750]
})

# Calculate route-level metrics
route_metrics = df_shipments.groupby('route').agg({
    'pallets': ['sum', 'mean'],
    'cost': ['sum', 'mean'],
    'date': 'count'
}).round(2)

route_metrics.columns = [
    'total_pallets', 'avg_pallets',
    'total_cost', 'avg_cost',
    'num_shipments'
]

# Calculate cost per pallet
route_metrics['cost_per_pallet'] = (
    route_metrics['total_cost'] / route_metrics['total_pallets']
).round(2)

print("Route Economics Analysis:")
print(route_metrics)
```

---

## 6. Merging and Joining DataFrames

### Types of Joins

```python
# Create sample dataframes
df_demands = pd.DataFrame({
    'demand_id': [1, 2, 3, 4],
    'source': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai'],
    'destination': ['Delhi', 'Kolkata', 'Mumbai', 'Bangalore'],
    'pallets': [100, 150, 120, 90]
})

df_costs = pd.DataFrame({
    'route': ['Mumbai-Delhi', 'Delhi-Kolkata', 'Chennai-Bangalore'],
    'cost': [25000, 36000, 8500],
    'distance_km': [1400, 1450, 350]
})

# Create route column in demands for joining
df_demands['route'] = df_demands['source'] + '-' + df_demands['destination']

# Inner join (only matching rows)
df_merged = pd.merge(
    df_demands,
    df_costs,
    on='route',
    how='inner'
)
print("Inner Join:")
print(df_merged)

# Left join (all rows from left DataFrame)
df_left = pd.merge(
    df_demands,
    df_costs,
    on='route',
    how='left'
)
print("\nLeft Join:")
print(df_left)

# Calculate total cost
df_merged['total_cost'] = (df_merged['pallets'] * 
                           df_merged['cost'] / 100)  # Assuming cost is per 100 pallets
```

### Real Quantyf Example: Combine Demand with Distance Matrix

```python
# Demands
df_demands = pd.DataFrame({
    'source_id': ['MUM_01', 'DEL_01', 'BLR_01'],
    'dest_id': ['DEL_01', 'KOL_01', 'MUM_01'],
    'pallets': [150, 200, 100]
})

# Distance matrix
df_distances = pd.DataFrame({
    'from_id': ['MUM_01', 'DEL_01', 'BLR_01'],
    'to_id': ['DEL_01', 'KOL_01', 'MUM_01'],
    'distance_km': [1400, 1450, 840],
    'travel_time_hrs': [24, 26, 16]
})

# Merge on multiple columns
df_complete = pd.merge(
    df_demands,
    df_distances,
    left_on=['source_id', 'dest_id'],
    right_on=['from_id', 'to_id'],
    how='left'
)

# Calculate metrics
COST_PER_PALLET_KM = 0.25
df_complete['total_cost'] = (
    df_complete['pallets'] * 
    df_complete['distance_km'] * 
    COST_PER_PALLET_KM
)

print("Complete Demand Analysis:")
print(df_complete[['source_id', 'dest_id', 'pallets', 
                   'distance_km', 'total_cost']])
```

---

## 7. Sorting and Ranking

```python
# Sort by single column
df_sorted = df_routes.sort_values('distance_km')

# Sort by multiple columns
df_sorted = df_routes.sort_values(
    ['status', 'distance_km'],
    ascending=[True, False]
)

# Add rank
df_routes['cost_rank'] = df_routes['avg_cost'].rank(ascending=False)

# Percentile rank
df_routes['cost_percentile'] = df_routes['avg_cost'].rank(pct=True)

print(df_routes[['origin', 'destination', 'avg_cost', 'cost_rank']])
```

---

## 8. Practice Exercises

### Exercise 1: Route Cost Analysis

Create a DataFrame with route data and calculate various metrics:

```python
# Sample data
routes_data = {
    'route_id': range(1, 6),
    'origin': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
    'destination': ['Delhi', 'Kolkata', 'Mumbai', 'Bangalore', 'Chennai'],
    'distance_km': [1400, 1450, 840, 350, 1670],
    'num_shipments': [45, 38, 62, 89, 23],
    'total_cost': [1575000, 1377000, 1302000, 779250, 959850]
}

df_routes = pd.DataFrame(routes_data)

# Tasks:
# 1. Calculate average cost per shipment
# 2. Calculate cost per kilometer
# 3. Find the most efficient route (lowest cost per km)
# 4. Calculate what percentage each route contributes to total cost
# 5. Categorize routes as 'High Volume' (>50 shipments) or 'Low Volume'

# Your code here!
```

### Exercise 2: Demand Aggregation

```python
# Sample demand data
demands_data = {
    'demand_id': range(1, 11),
    'date': pd.date_range('2025-01-01', periods=10),
    'source': ['Mumbai', 'Delhi', 'Mumbai', 'Bangalore', 'Delhi',
               'Mumbai', 'Chennai', 'Delhi', 'Mumbai', 'Bangalore'],
    'destination': ['Delhi', 'Kolkata', 'Delhi', 'Mumbai', 'Chennai',
                   'Bangalore', 'Kolkata', 'Mumbai', 'Chennai', 'Delhi'],
    'pallets': [100, 150, 120, 90, 180, 110, 95, 160, 140, 105]
}

df_demands = pd.DataFrame(demands_data)

# Tasks:
# 1. Calculate total pallets by source
# 2. Calculate average pallets by destination
# 3. Find the busiest route (source-destination pair)
# 4. Calculate daily total demand
# 5. Find sources that ship more than 300 total pallets

# Your code here!
```

### Exercise 3: Merging Supply and Demand

```python
# Center capacities
capacities_data = {
    'center_id': ['MUM_01', 'DEL_01', 'BLR_01', 'CHE_01'],
    'capacity': [500, 750, 600, 400],
    'utilization': [0.85, 0.72, 0.91, 0.65]
}

# Incoming demands
demands_data = {
    'center_id': ['MUM_01', 'DEL_01', 'BLR_01', 'KOL_01'],
    'incoming_pallets': [425, 540, 550, 200]
}

df_capacity = pd.DataFrame(capacities_data)
df_demand = pd.DataFrame(demands_data)

# Tasks:
# 1. Merge the datasets
# 2. Calculate current usage (capacity * utilization)
# 3. Calculate available capacity
# 4. Check if incoming demand exceeds available capacity
# 5. Calculate new utilization after incoming demand

# Your code here!
```

---

## 9. Solutions

<details>
<summary>Click to see solutions</summary>

### Solution 1: Route Cost Analysis

```python
# 1. Average cost per shipment
df_routes['avg_cost_per_shipment'] = df_routes['total_cost'] / df_routes['num_shipments']

# 2. Cost per kilometer
df_routes['cost_per_km'] = df_routes['total_cost'] / df_routes['distance_km']

# 3. Most efficient route
most_efficient = df_routes.loc[df_routes['cost_per_km'].idxmin()]
print(f"Most efficient: {most_efficient['origin']}-{most_efficient['destination']}")

# 4. Percentage contribution
df_routes['pct_of_total'] = (df_routes['total_cost'] / df_routes['total_cost'].sum()) * 100

# 5. Volume categorization
df_routes['volume_category'] = df_routes['num_shipments'].apply(
    lambda x: 'High Volume' if x > 50 else 'Low Volume'
)

print(df_routes)
```

### Solution 2: Demand Aggregation

```python
# 1. Total pallets by source
source_totals = df_demands.groupby('source')['pallets'].sum()
print("Total by source:\n", source_totals)

# 2. Average pallets by destination
dest_avg = df_demands.groupby('destination')['pallets'].mean()
print("\nAverage by destination:\n", dest_avg)

# 3. Busiest route
df_demands['route'] = df_demands['source'] + '-' + df_demands['destination']
route_totals = df_demands.groupby('route')['pallets'].sum()
busiest = route_totals.idxmax()
print(f"\nBusiest route: {busiest} with {route_totals[busiest]} pallets")

# 4. Daily total
daily_demand = df_demands.groupby('date')['pallets'].sum()
print("\nDaily demand:\n", daily_demand)

# 5. High-volume sources
high_volume_sources = source_totals[source_totals > 300]
print("\nHigh volume sources:\n", high_volume_sources)
```

### Solution 3: Merging Supply and Demand

```python
# 1. Merge datasets
df_merged = pd.merge(df_capacity, df_demand, on='center_id', how='left')

# Handle centers with no incoming demand
df_merged['incoming_pallets'] = df_merged['incoming_pallets'].fillna(0)

# 2. Current usage
df_merged['current_usage'] = df_merged['capacity'] * df_merged['utilization']

# 3. Available capacity
df_merged['available_capacity'] = df_merged['capacity'] - df_merged['current_usage']

# 4. Check if demand exceeds capacity
df_merged['exceeds_capacity'] = (
    df_merged['incoming_pallets'] > df_merged['available_capacity']
)

# 5. New utilization
df_merged['new_usage'] = df_merged['current_usage'] + df_merged['incoming_pallets']
df_merged['new_utilization'] = df_merged['new_usage'] / df_merged['capacity']

print(df_merged[[
    'center_id', 'capacity', 'current_usage', 
    'available_capacity', 'incoming_pallets', 
    'exceeds_capacity', 'new_utilization'
]])
```

</details>

---

## 🎯 Key Takeaways

1. ✅ DataFrames are like Excel sheets in Python
2. ✅ Use filtering to select specific data
3. ✅ GroupBy is essential for aggregations
4. ✅ Merge to combine multiple datasets
5. ✅ Apply functions to transform data
6. ✅ Pandas is the foundation of Quantyf's data processing

---

## 📚 Next Steps

You're now ready for **Tutorial 03: Advanced Pandas & Data Cleaning**!

In the next tutorial, you'll learn:
- Handling missing data
- Data type conversions
- String operations
- Date/time handling
- Performance optimization
- Real Quantyf data cleaning workflows

---

## 📖 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

Happy Learning! 🚀

