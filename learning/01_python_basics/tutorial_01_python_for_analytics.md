# Tutorial 01: Python Basics for Data Analysis

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Understand Python data types used in financial analytics
- Work with lists, dictionaries, and data structures
- Write functions for data processing
- Handle files and CSV data
- Use list comprehensions for efficient data manipulation

---

## 🎯 Why Python for Financial Analytics?

Python is the #1 language for financial analytics because:
- **Easy to learn** - Clean, readable syntax
- **Powerful libraries** - Pandas, NumPy, SciPy
- **Industry standard** - Used by banks, hedge funds, fintech companies
- **Fast development** - Quick prototyping and analysis
- **Open source** - Free tools and libraries

---

## 1. Python Data Types for Analytics

### Numbers - Financial Calculations

```python
# Integer - whole numbers (counts, quantities)
pallets = 100
trucks = 5
sort_centers = 3

# Float - decimal numbers (costs, distances, percentages)
cost_per_km = 2.50
distance_km = 145.75
utilization_rate = 0.85  # 85%

# Basic arithmetic
total_cost = cost_per_km * distance_km
print(f"Total Cost: ${total_cost:.2f}")  # Output: Total Cost: $364.38

# Financial calculations
revenue = 50000
expenses = 32000
profit = revenue - expenses
profit_margin = (profit / revenue) * 100
print(f"Profit Margin: {profit_margin:.1f}%")  # Output: Profit Margin: 36.0%
```

### Strings - Text Data

```python
# Customer and location data
customer_name = "ABC Corporation"
origin_city = "Mumbai"
destination_city = "Delhi"

# String operations
route_name = f"{origin_city} -> {destination_city}"
print(route_name)  # Output: Mumbai -> Delhi

# String methods
center_code = "  MUM_SC_01  "
center_code_clean = center_code.strip().upper()
print(center_code_clean)  # Output: MUM_SC_01

# Check if string contains text
if "MUM" in center_code_clean:
    print("Mumbai center detected")
```

### Boolean - Logical Operations

```python
# Decision making in analytics
is_direct_route = True
is_consolidation_needed = False
has_capacity = True

# Logical operations
can_ship = has_capacity and (is_direct_route or is_consolidation_needed)
print(f"Can ship: {can_ship}")  # Output: Can ship: True

# Comparisons
demand = 150
vehicle_capacity = 200

is_under_capacity = demand < vehicle_capacity
print(f"Under capacity: {is_under_capacity}")  # Output: Under capacity: True
```

---

## 2. Lists - Working with Collections

### Basic List Operations

```python
# List of costs for different routes
route_costs = [2500, 3200, 1800, 4100, 2900]

# Access elements
first_cost = route_costs[0]  # 2500
last_cost = route_costs[-1]   # 2900

# List operations
route_costs.append(3500)  # Add new cost
route_costs.remove(1800)  # Remove specific cost
route_costs.sort()        # Sort in ascending order

print(f"Minimum cost: ${min(route_costs)}")
print(f"Maximum cost: ${max(route_costs)}")
print(f"Average cost: ${sum(route_costs) / len(route_costs):.2f}")
```

### List Comprehensions - Efficient Data Processing

```python
# Calculate costs with 10% markup
original_costs = [2500, 3200, 1800, 4100, 2900]
marked_up_costs = [cost * 1.10 for cost in original_costs]

print(marked_up_costs)
# Output: [2750.0, 3520.0, 1980.0, 4510.0, 3190.0]

# Filter routes under $3000
affordable_routes = [cost for cost in original_costs if cost < 3000]
print(affordable_routes)
# Output: [2500, 1800, 2900]

# Calculate percentage savings
baseline = 3000
savings = [(baseline - cost) / baseline * 100 
           for cost in original_costs if cost < baseline]
print(f"Savings: {savings}")
# Output: Savings: [16.67, 40.0, 3.33]
```

### Real Quantyf Example: Processing Demand Data

```python
# Sample demand data (pallets per route)
demands = [50, 120, 75, 200, 90, 150]

# Calculate total demand
total_demand = sum(demands)
print(f"Total demand: {total_demand} pallets")

# Find routes exceeding threshold
high_demand_threshold = 100
high_demand_routes = [d for d in demands if d > high_demand_threshold]
print(f"High demand routes: {high_demand_routes}")

# Calculate cumulative demand
cumulative = []
running_total = 0
for demand in demands:
    running_total += demand
    cumulative.append(running_total)
    
print(f"Cumulative demand: {cumulative}")
# Output: Cumulative demand: [50, 170, 245, 445, 535, 685]
```

---

## 3. Dictionaries - Structured Data

### Basic Dictionary Operations

```python
# Route information
route_info = {
    "origin": "Mumbai",
    "destination": "Delhi",
    "distance_km": 1400,
    "cost": 35000,
    "vehicle_type": "Truck"
}

# Access values
print(route_info["origin"])  # Mumbai
print(route_info.get("cost"))  # 35000

# Add/Update values
route_info["duration_hours"] = 24
route_info["cost"] = 32000  # Update cost

# Check if key exists
if "distance_km" in route_info:
    cost_per_km = route_info["cost"] / route_info["distance_km"]
    print(f"Cost per km: ${cost_per_km:.2f}")
```

### Dictionary Comprehensions

```python
# Create cost dictionary for multiple routes
routes = ["Mumbai-Delhi", "Delhi-Kolkata", "Kolkata-Chennai"]
costs = [35000, 18000, 22000]

# Create dictionary mapping route to cost
route_costs_dict = {route: cost for route, cost in zip(routes, costs)}
print(route_costs_dict)
# Output: {'Mumbai-Delhi': 35000, 'Delhi-Kolkata': 18000, 'Kolkata-Chennai': 22000}

# Calculate cost per character (silly example, but shows concept)
cost_efficiency = {route: cost/len(route) 
                   for route, cost in route_costs_dict.items()}
print(cost_efficiency)
```

### Real Quantyf Example: Center Data

```python
# Sort center information
centers = {
    "MUM_SC_01": {
        "name": "Mumbai Sort Center 1",
        "capacity": 500,
        "cost_per_pallet": 50,
        "utilization": 0.75
    },
    "DEL_SC_01": {
        "name": "Delhi Sort Center 1",
        "capacity": 750,
        "cost_per_pallet": 45,
        "utilization": 0.88
    }
}

# Calculate available capacity
for center_id, info in centers.items():
    available = info["capacity"] * (1 - info["utilization"])
    print(f"{center_id}: {available:.0f} pallets available")

# Find underutilized centers
underutilized = {cid: info for cid, info in centers.items() 
                 if info["utilization"] < 0.80}
print(f"\nUnderutilized centers: {list(underutilized.keys())}")
```

---

## 4. Functions - Reusable Logic

### Basic Functions

```python
def calculate_transportation_cost(distance_km, cost_per_km):
    """Calculate total transportation cost."""
    return distance_km * cost_per_km

# Usage
cost = calculate_transportation_cost(1400, 25)
print(f"Transportation cost: ${cost}")
```

### Functions with Default Parameters

```python
def calculate_total_cost(distance_km, cost_per_km, fixed_cost=500):
    """
    Calculate total cost including fixed costs.
    
    Args:
        distance_km: Distance in kilometers
        cost_per_km: Variable cost per kilometer
        fixed_cost: Fixed cost (default: 500)
    
    Returns:
        Total cost
    """
    variable_cost = distance_km * cost_per_km
    total = variable_cost + fixed_cost
    return total

# Usage
cost1 = calculate_total_cost(100, 20)      # Uses default fixed cost
cost2 = calculate_total_cost(100, 20, 1000)  # Custom fixed cost

print(f"Cost 1: ${cost1}")  # Output: Cost 1: $2500
print(f"Cost 2: ${cost2}")  # Output: Cost 2: $3000
```

### Real Quantyf Example: Route Cost Calculator

```python
def calculate_route_cost(origin, destination, pallets, 
                         cost_per_pallet_km, distance_km):
    """
    Calculate total route cost based on volume and distance.
    
    This mirrors Quantyf's cost calculation logic.
    """
    # Calculate per pallet cost
    cost_per_pallet = distance_km * cost_per_pallet_km
    
    # Calculate total cost
    total_cost = pallets * cost_per_pallet
    
    # Create result dictionary
    result = {
        "route": f"{origin} -> {destination}",
        "distance_km": distance_km,
        "pallets": pallets,
        "cost_per_pallet": cost_per_pallet,
        "total_cost": total_cost,
        "cost_per_km": total_cost / distance_km if distance_km > 0 else 0
    }
    
    return result

# Example usage
route_cost = calculate_route_cost(
    origin="Mumbai",
    destination="Delhi",
    pallets=150,
    cost_per_pallet_km=0.25,
    distance_km=1400
)

print(f"Route: {route_cost['route']}")
print(f"Total Cost: ${route_cost['total_cost']:,.2f}")
print(f"Cost per pallet: ${route_cost['cost_per_pallet']:.2f}")
```

### Functions Returning Multiple Values

```python
def analyze_route_economics(total_revenue, total_cost):
    """Analyze route profitability."""
    profit = total_revenue - total_cost
    profit_margin = (profit / total_revenue) * 100 if total_revenue > 0 else 0
    is_profitable = profit > 0
    
    return profit, profit_margin, is_profitable

# Usage
profit, margin, profitable = analyze_route_economics(50000, 32000)

print(f"Profit: ${profit:,.2f}")
print(f"Margin: {margin:.1f}%")
print(f"Profitable: {profitable}")
```

---

## 5. File Handling - Working with CSV Data

### Reading CSV Files

```python
import csv

def read_route_costs(filename):
    """Read route costs from CSV file."""
    routes = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            route = {
                "origin": row["origin"],
                "destination": row["destination"],
                "cost": float(row["cost"]),
                "distance": float(row["distance"])
            }
            routes.append(route)
    
    return routes

# Create sample CSV file
sample_data = """origin,destination,cost,distance
Mumbai,Delhi,35000,1400
Delhi,Kolkata,18000,1450
Kolkata,Chennai,22000,1670"""

# Write sample file
with open("route_costs.csv", "w") as f:
    f.write(sample_data)

# Read the file
routes = read_route_costs("route_costs.csv")
print(f"Loaded {len(routes)} routes")

# Analyze the data
total_cost = sum(r["cost"] for r in routes)
avg_cost_per_km = sum(r["cost"]/r["distance"] for r in routes) / len(routes)

print(f"Total cost: ${total_cost:,.2f}")
print(f"Average cost per km: ${avg_cost_per_km:.2f}")
```

### Writing CSV Files

```python
def write_cost_analysis(routes, output_file):
    """Write cost analysis to CSV file."""
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['route', 'cost', 'distance', 'cost_per_km', 'category']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for route in routes:
            cost_per_km = route["cost"] / route["distance"]
            
            # Categorize routes
            if cost_per_km < 20:
                category = "Low Cost"
            elif cost_per_km < 30:
                category = "Medium Cost"
            else:
                category = "High Cost"
            
            writer.writerow({
                "route": f"{route['origin']}-{route['destination']}",
                "cost": route["cost"],
                "distance": route["distance"],
                "cost_per_km": round(cost_per_km, 2),
                "category": category
            })

# Write analysis
write_cost_analysis(routes, "cost_analysis.csv")
print("Cost analysis written to cost_analysis.csv")
```

---

## 6. Practice Exercises

### Exercise 1: Transportation Cost Calculator

Create a function that calculates transportation costs with these rules:
- Base cost: $500
- Per km cost: $2.50
- Volume discount: 5% off if > 100 pallets, 10% off if > 200 pallets
- Express surcharge: +20% if express delivery

```python
def calculate_transport_cost(distance_km, pallets, is_express=False):
    """
    Calculate transportation cost with discounts and surcharges.
    
    Your implementation here!
    """
    pass

# Test cases
print(calculate_transport_cost(100, 50))        # Expected: ~750
print(calculate_transport_cost(100, 150, False)) # Expected: ~713 (with 5% discount)
print(calculate_transport_cost(100, 250, True))  # Expected: ~810 (10% discount, 20% surcharge)
```

### Exercise 2: Route Analyzer

Create a function that analyzes a list of routes and returns statistics:

```python
def analyze_routes(routes_data):
    """
    Analyze routes and return statistics.
    
    Args:
        routes_data: List of dictionaries with 'cost' and 'distance' keys
    
    Returns:
        Dictionary with min_cost, max_cost, avg_cost, total_distance
    
    Your implementation here!
    """
    pass

# Test data
test_routes = [
    {"cost": 2500, "distance": 100},
    {"cost": 3500, "distance": 150},
    {"cost": 1800, "distance": 75}
]

stats = analyze_routes(test_routes)
print(stats)
# Expected: {'min_cost': 1800, 'max_cost': 3500, 'avg_cost': 2600, 'total_distance': 325}
```

### Exercise 3: Demand Aggregation

Process demand data and calculate aggregates by destination:

```python
def aggregate_demand_by_destination(demands):
    """
    Aggregate pallets by destination.
    
    Args:
        demands: List of dicts with 'destination' and 'pallets' keys
    
    Returns:
        Dictionary mapping destination to total pallets
    
    Your implementation here!
    """
    pass

# Test data
test_demands = [
    {"destination": "Delhi", "pallets": 50},
    {"destination": "Mumbai", "pallets": 75},
    {"destination": "Delhi", "pallets": 100},
    {"destination": "Chennai", "pallets": 60},
    {"destination": "Mumbai", "pallets": 25}
]

result = aggregate_demand_by_destination(test_demands)
print(result)
# Expected: {'Delhi': 150, 'Mumbai': 100, 'Chennai': 60}
```

---

## 7. Solutions

<details>
<summary>Click to see solutions</summary>

### Solution 1: Transportation Cost Calculator

```python
def calculate_transport_cost(distance_km, pallets, is_express=False):
    """Calculate transportation cost with discounts and surcharges."""
    # Base costs
    base_cost = 500
    per_km_cost = 2.50
    
    # Calculate base transportation cost
    transport_cost = base_cost + (distance_km * per_km_cost)
    
    # Apply volume discounts
    if pallets > 200:
        transport_cost *= 0.90  # 10% discount
    elif pallets > 100:
        transport_cost *= 0.95  # 5% discount
    
    # Apply express surcharge
    if is_express:
        transport_cost *= 1.20  # 20% surcharge
    
    return round(transport_cost, 2)
```

### Solution 2: Route Analyzer

```python
def analyze_routes(routes_data):
    """Analyze routes and return statistics."""
    if not routes_data:
        return {}
    
    costs = [route["cost"] for route in routes_data]
    distances = [route["distance"] for route in routes_data]
    
    return {
        "min_cost": min(costs),
        "max_cost": max(costs),
        "avg_cost": round(sum(costs) / len(costs), 2),
        "total_distance": sum(distances),
        "total_cost": sum(costs),
        "avg_cost_per_km": round(sum(costs) / sum(distances), 2)
    }
```

### Solution 3: Demand Aggregation

```python
def aggregate_demand_by_destination(demands):
    """Aggregate pallets by destination."""
    aggregated = {}
    
    for demand in demands:
        destination = demand["destination"]
        pallets = demand["pallets"]
        
        if destination in aggregated:
            aggregated[destination] += pallets
        else:
            aggregated[destination] = pallets
    
    return aggregated
```

</details>

---

## 🎯 Key Takeaways

1. ✅ Python data types (int, float, string, bool) for financial calculations
2. ✅ Lists and list comprehensions for data processing
3. ✅ Dictionaries for structured data
4. ✅ Functions for reusable logic
5. ✅ File handling for CSV data
6. ✅ Real-world applications in supply chain analytics

---

## 📚 Next Steps

You're now ready for **Tutorial 02: Pandas DataFrame Operations**!

In the next tutorial, you'll learn:
- Creating and manipulating DataFrames
- Data filtering and selection
- Aggregations and grouping
- Merging and joining datasets
- Real Quantyf data processing examples

---

## 📖 Additional Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python - Python Basics](https://realpython.com/tutorials/basics/)
- [W3Schools Python Tutorial](https://www.w3schools.com/python/)

Happy Learning! 🚀

