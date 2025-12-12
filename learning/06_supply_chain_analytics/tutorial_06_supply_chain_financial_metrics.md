# Tutorial 06: Supply Chain Financial Metrics & Cost Analysis

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Understand key financial metrics in supply chain management
- Calculate transportation and logistics costs
- Analyze route profitability and efficiency
- Implement cost optimization strategies
- Apply real Quantyf optimization concepts

---

## 🎯 Why Supply Chain Financial Analytics?

Supply chain costs typically represent **60-80% of total product cost**. Understanding and optimizing these costs can:
- **Increase profitability** by 15-30%
- **Improve cash flow** through better inventory management
- **Enhance competitiveness** with lower prices or higher margins
- **Enable data-driven decisions** for network design

**Quantyf's mission**: Minimize total supply chain costs while meeting delivery requirements.

---

## 1. Core Cost Components

### 1.1 Transportation Costs

```python
import pandas as pd
import numpy as np

def calculate_transportation_cost(distance_km, pallets, cost_per_pallet_km, 
                                  fixed_cost=500):
    """
    Calculate total transportation cost.
    
    Components:
    - Fixed cost: Vehicle preparation, paperwork, loading/unloading
    - Variable cost: Fuel, driver wages, maintenance per km
    """
    variable_cost = distance_km * pallets * cost_per_pallet_km
    total_cost = fixed_cost + variable_cost
    
    return {
        'fixed_cost': fixed_cost,
        'variable_cost': variable_cost,
        'total_cost': total_cost,
        'cost_per_km': total_cost / distance_km if distance_km > 0 else 0,
        'cost_per_pallet': total_cost / pallets if pallets > 0 else 0
    }

# Example: Mumbai to Delhi route
route_cost = calculate_transportation_cost(
    distance_km=1400,
    pallets=150,
    cost_per_pallet_km=0.25,
    fixed_cost=500
)

print("Transportation Cost Breakdown:")
for key, value in route_cost.items():
    print(f"  {key}: ₹{value:,.2f}")
```

Output:
```
Transportation Cost Breakdown:
  fixed_cost: ₹500.00
  variable_cost: ₹52,500.00
  total_cost: ₹53,000.00
  cost_per_km: ₹37.86
  cost_per_pallet: ₹353.33
```

### 1.2 Warehousing & Handling Costs

```python
def calculate_handling_cost(pallets, centers_visited, 
                            cost_per_pallet_handling=50,
                            cost_per_center=200):
    """
    Calculate handling costs at sort centers.
    
    Components:
    - Per pallet handling: Loading, unloading, inspection
    - Per center fixed cost: Administrative overhead
    """
    pallet_handling = pallets * cost_per_pallet_handling
    center_costs = centers_visited * cost_per_center
    total = pallet_handling + center_costs
    
    return {
        'pallet_handling_cost': pallet_handling,
        'center_fixed_costs': center_costs,
        'total_handling_cost': total
    }

# Example: Shipment through 2 sort centers
handling = calculate_handling_cost(
    pallets=150,
    centers_visited=2,
    cost_per_pallet_handling=50,
    cost_per_center=200
)

print("\nHandling Cost Breakdown:")
for key, value in handling.items():
    print(f"  {key}: ₹{value:,.2f}")
```

### 1.3 Inventory Holding Costs

```python
def calculate_inventory_holding_cost(inventory_value, holding_rate=0.25, 
                                     days_held=30):
    """
    Calculate cost of holding inventory.
    
    Components:
    - Capital cost: Interest on money tied up in inventory
    - Storage cost: Warehouse space, utilities
    - Insurance: Protection against damage/loss
    - Obsolescence: Risk of product becoming outdated
    
    Typical holding rate: 20-30% annually
    """
    annual_holding_cost = inventory_value * holding_rate
    daily_holding_cost = annual_holding_cost / 365
    total_cost = daily_holding_cost * days_held
    
    return {
        'inventory_value': inventory_value,
        'annual_holding_cost': annual_holding_cost,
        'daily_holding_cost': daily_holding_cost,
        'total_cost_for_period': total_cost,
        'days_held': days_held
    }

# Example: ₹10 lakhs inventory held for 30 days
inventory_cost = calculate_inventory_holding_cost(
    inventory_value=1000000,  # ₹10 lakhs
    holding_rate=0.25,        # 25% annual
    days_held=30
)

print("\nInventory Holding Cost:")
print(f"  Daily cost: ₹{inventory_cost['daily_holding_cost']:,.2f}")
print(f"  30-day cost: ₹{inventory_cost['total_cost_for_period']:,.2f}")
```

---

## 2. Key Performance Indicators (KPIs)

### 2.1 Cost Per Unit Metrics

```python
class SupplyChainKPIs:
    """Calculate essential supply chain KPIs."""
    
    @staticmethod
    def cost_per_pallet(total_cost, total_pallets):
        """Average cost to move one pallet."""
        return total_cost / total_pallets if total_pallets > 0 else 0
    
    @staticmethod
    def cost_per_kilometer(total_cost, total_distance):
        """Cost efficiency of transportation."""
        return total_cost / total_distance if total_distance > 0 else 0
    
    @staticmethod
    def cost_per_shipment(total_cost, number_of_shipments):
        """Average cost per delivery."""
        return total_cost / number_of_shipments if number_of_shipments > 0 else 0
    
    @staticmethod
    def cost_as_percentage_of_revenue(logistics_cost, revenue):
        """What percentage of revenue goes to logistics."""
        return (logistics_cost / revenue * 100) if revenue > 0 else 0

# Example usage
kpis = SupplyChainKPIs()

# Monthly data
monthly_data = {
    'total_cost': 2500000,      # ₹25 lakhs
    'total_pallets': 5000,
    'total_distance': 75000,    # km
    'num_shipments': 250,
    'revenue': 12000000         # ₹1.2 crores
}

print("Supply Chain KPIs:")
print(f"  Cost per pallet: ₹{kpis.cost_per_pallet(monthly_data['total_cost'], monthly_data['total_pallets']):.2f}")
print(f"  Cost per km: ₹{kpis.cost_per_kilometer(monthly_data['total_cost'], monthly_data['total_distance']):.2f}")
print(f"  Cost per shipment: ₹{kpis.cost_per_shipment(monthly_data['total_cost'], monthly_data['num_shipments']):.2f}")
print(f"  Cost as % of revenue: {kpis.cost_as_percentage_of_revenue(monthly_data['total_cost'], monthly_data['revenue']):.1f}%")
```

### 2.2 Efficiency Metrics

```python
def calculate_vehicle_utilization(actual_pallets, vehicle_capacity):
    """Measure how well we use vehicle capacity."""
    utilization = (actual_pallets / vehicle_capacity) * 100 if vehicle_capacity > 0 else 0
    wasted_capacity = vehicle_capacity - actual_pallets
    
    return {
        'utilization_pct': utilization,
        'wasted_capacity': wasted_capacity,
        'efficiency_score': 'Good' if utilization >= 80 else ('Acceptable' if utilization >= 60 else 'Poor')
    }

def calculate_route_efficiency(actual_distance, optimal_distance):
    """Measure route efficiency (how close to optimal path)."""
    efficiency = (optimal_distance / actual_distance) * 100 if actual_distance > 0 else 0
    excess_distance = actual_distance - optimal_distance
    
    return {
        'efficiency_pct': efficiency,
        'excess_distance_km': excess_distance,
        'excess_distance_pct': (excess_distance / optimal_distance) * 100 if optimal_distance > 0 else 0
    }

# Example: Vehicle utilization
truck_util = calculate_vehicle_utilization(
    actual_pallets=170,
    vehicle_capacity=200
)
print(f"\nVehicle Utilization: {truck_util['utilization_pct']:.1f}% - {truck_util['efficiency_score']}")

# Example: Route efficiency
route_eff = calculate_route_efficiency(
    actual_distance=1500,   # km taken
    optimal_distance=1400   # km optimal
)
print(f"Route Efficiency: {route_eff['efficiency_pct']:.1f}% (excess: {route_eff['excess_distance_km']} km)")
```

---

## 3. Real Quantyf Use Case: Route Cost Comparison

### 3.1 Direct vs. Consolidation Routes

```python
class RouteAnalyzer:
    """Analyze different routing strategies."""
    
    def __init__(self, cost_per_km=25, cost_per_stop=200, 
                 cost_per_pallet_handling=50):
        self.cost_per_km = cost_per_km
        self.cost_per_stop = cost_per_stop
        self.cost_per_pallet_handling = cost_per_pallet_handling
    
    def direct_route_cost(self, origin, destination, distance, pallets):
        """Calculate cost for direct shipment."""
        transport_cost = distance * self.cost_per_km
        stop_cost = self.cost_per_stop * 2  # Origin + destination
        handling_cost = pallets * self.cost_per_pallet_handling * 2
        
        total = transport_cost + stop_cost + handling_cost
        
        return {
            'route_type': 'Direct',
            'route': f"{origin} → {destination}",
            'distance': distance,
            'transport_cost': transport_cost,
            'stop_cost': stop_cost,
            'handling_cost': handling_cost,
            'total_cost': total,
            'cost_per_pallet': total / pallets if pallets > 0 else 0
        }
    
    def consolidation_route_cost(self, origin, hub, destination, 
                                  dist_to_hub, dist_from_hub, pallets):
        """Calculate cost for route through consolidation hub."""
        # Transport costs
        transport_cost = (dist_to_hub + dist_from_hub) * self.cost_per_km
        
        # Stop costs (origin, hub, destination)
        stop_cost = self.cost_per_stop * 3
        
        # Handling costs (load at origin, unload & reload at hub, unload at dest)
        handling_cost = pallets * self.cost_per_pallet_handling * 4
        
        total = transport_cost + stop_cost + handling_cost
        
        return {
            'route_type': 'Consolidation',
            'route': f"{origin} → {hub} → {destination}",
            'distance': dist_to_hub + dist_from_hub,
            'transport_cost': transport_cost,
            'stop_cost': stop_cost,
            'handling_cost': handling_cost,
            'total_cost': total,
            'cost_per_pallet': total / pallets if pallets > 0 else 0
        }

# Analyze routes
analyzer = RouteAnalyzer(
    cost_per_km=25,
    cost_per_stop=200,
    cost_per_pallet_handling=50
)

# Direct route: Mumbai → Chennai
direct = analyzer.direct_route_cost(
    origin="Mumbai",
    destination="Chennai",
    distance=1340,
    pallets=100
)

# Consolidation: Mumbai → Bangalore → Chennai
consolidation = analyzer.consolidation_route_cost(
    origin="Mumbai",
    hub="Bangalore",
    destination="Chennai",
    dist_to_hub=840,
    dist_from_hub=350,
    pallets=100
)

# Compare
print("\n=== Route Comparison ===")
print(f"\nDirect Route:")
print(f"  Route: {direct['route']}")
print(f"  Distance: {direct['distance']} km")
print(f"  Total Cost: ₹{direct['total_cost']:,.2f}")
print(f"  Cost per pallet: ₹{direct['cost_per_pallet']:.2f}")

print(f"\nConsolidation Route:")
print(f"  Route: {consolidation['route']}")
print(f"  Distance: {consolidation['distance']} km")
print(f"  Total Cost: ₹{consolidation['total_cost']:,.2f}")
print(f"  Cost per pallet: ₹{consolidation['cost_per_pallet']:.2f}")

# Savings analysis
savings = direct['total_cost'] - consolidation['total_cost']
savings_pct = (savings / direct['total_cost']) * 100

print(f"\n{'✅ Consolidation Saves' if savings > 0 else '❌ Direct is Cheaper'}:")
print(f"  Savings: ₹{abs(savings):,.2f} ({abs(savings_pct):.1f}%)")
```

---

## 4. Optimization Metrics - What Quantyf Optimizes

### 4.1 Total Supply Chain Cost Minimization

```python
def calculate_total_supply_chain_cost(routes_df):
    """
    Calculate total cost across entire supply chain network.
    This is what Quantyf's FICO optimizer minimizes.
    """
    # Transportation costs
    transport_costs = (routes_df['distance_km'] * 
                      routes_df['cost_per_km'] * 
                      routes_df['num_trucks']).sum()
    
    # Handling costs at sort centers
    handling_costs = (routes_df['pallets'] * 
                     routes_df['handling_cost_per_pallet']).sum()
    
    # Fixed costs
    fixed_costs = routes_df['fixed_cost'].sum()
    
    total_cost = transport_costs + handling_costs + fixed_costs
    
    return {
        'transport_costs': transport_costs,
        'handling_costs': handling_costs,
        'fixed_costs': fixed_costs,
        'total_cost': total_cost,
        'avg_cost_per_route': total_cost / len(routes_df) if len(routes_df) > 0 else 0
    }

# Sample network data
routes_data = pd.DataFrame({
    'route_id': range(1, 6),
    'distance_km': [1400, 840, 350, 1450, 1670],
    'pallets': [150, 120, 80, 200, 95],
    'cost_per_km': [25, 25, 25, 25, 25],
    'handling_cost_per_pallet': [50, 50, 50, 50, 50],
    'fixed_cost': [500, 500, 500, 500, 500],
    'num_trucks': [2, 1, 1, 2, 1]
})

total_costs = calculate_total_supply_chain_cost(routes_data)

print("\n=== Total Network Costs ===")
print(f"Transportation: ₹{total_costs['transport_costs']:,.2f}")
print(f"Handling: ₹{total_costs['handling_costs']:,.2f}")
print(f"Fixed: ₹{total_costs['fixed_costs']:,.2f}")
print(f"TOTAL: ₹{total_costs['total_cost']:,.2f}")
```

### 4.2 Constraint Satisfaction

```python
def check_constraints(solution_df, constraints):
    """
    Verify that solution meets all business constraints.
    Quantyf's optimizer ensures these are satisfied.
    """
    violations = []
    
    # Check capacity constraints
    for idx, row in solution_df.iterrows():
        if row['pallets'] > constraints['max_vehicle_capacity']:
            violations.append({
                'route': idx,
                'type': 'Capacity',
                'issue': f"Pallets ({row['pallets']}) exceed capacity ({constraints['max_vehicle_capacity']})"
            })
    
    # Check time window constraints
    for idx, row in solution_df.iterrows():
        if row['travel_time_hrs'] > constraints['max_travel_time']:
            violations.append({
                'route': idx,
                'type': 'Time',
                'issue': f"Travel time ({row['travel_time_hrs']}h) exceeds max ({constraints['max_travel_time']}h)"
            })
    
    # Check budget constraint
    total_cost = solution_df['cost'].sum()
    if total_cost > constraints['budget']:
        violations.append({
            'route': 'Overall',
            'type': 'Budget',
            'issue': f"Total cost (₹{total_cost:,.0f}) exceeds budget (₹{constraints['budget']:,.0f})"
        })
    
    return {
        'is_feasible': len(violations) == 0,
        'num_violations': len(violations),
        'violations': violations
    }

# Example solution
solution = pd.DataFrame({
    'route_id': [1, 2, 3],
    'pallets': [180, 150, 220],  # Route 3 exceeds capacity!
    'travel_time_hrs': [24, 16, 30],  # Route 3 exceeds time!
    'cost': [45000, 32000, 55000]
})

constraints = {
    'max_vehicle_capacity': 200,
    'max_travel_time': 28,
    'budget': 150000
}

validation = check_constraints(solution, constraints)

print("\n=== Constraint Validation ===")
print(f"Feasible: {'✅ Yes' if validation['is_feasible'] else '❌ No'}")
print(f"Violations: {validation['num_violations']}")

if not validation['is_feasible']:
    print("\nConstraint Violations:")
    for v in validation['violations']:
        print(f"  - Route {v['route']} ({v['type']}): {v['issue']}")
```

---

## 5. Cost-Benefit Analysis

### 5.1 ROI Calculation for Optimization

```python
def calculate_optimization_roi(baseline_cost, optimized_cost, 
                                implementation_cost, time_period_months=12):
    """
    Calculate ROI from implementing optimization.
    Used to justify investment in tools like Quantyf.
    """
    # Monthly savings
    monthly_savings = baseline_cost - optimized_cost
    
    # Annual savings
    annual_savings = monthly_savings * 12
    
    # Payback period (months to recover implementation cost)
    payback_months = implementation_cost / monthly_savings if monthly_savings > 0 else float('inf')
    
    # ROI over time period
    total_savings_over_period = monthly_savings * time_period_months
    net_benefit = total_savings_over_period - implementation_cost
    roi_pct = (net_benefit / implementation_cost) * 100 if implementation_cost > 0 else 0
    
    return {
        'monthly_savings': monthly_savings,
        'annual_savings': annual_savings,
        'payback_months': payback_months,
        'total_savings_over_period': total_savings_over_period,
        'net_benefit': net_benefit,
        'roi_percentage': roi_pct,
        'savings_percentage': ((baseline_cost - optimized_cost) / baseline_cost) * 100 if baseline_cost > 0 else 0
    }

# Example: Before and after Quantyf
baseline_monthly_cost = 2500000  # ₹25 lakhs/month before optimization
optimized_monthly_cost = 1875000  # ₹18.75 lakhs/month after optimization
implementation_cost = 500000     # ₹5 lakhs one-time cost

roi = calculate_optimization_roi(
    baseline_cost=baseline_monthly_cost,
    optimized_cost=optimized_monthly_cost,
    implementation_cost=implementation_cost,
    time_period_months=12
)

print("\n=== Optimization ROI Analysis ===")
print(f"Monthly Savings: ₹{roi['monthly_savings']:,.2f}")
print(f"Annual Savings: ₹{roi['annual_savings']:,.2f}")
print(f"Cost Reduction: {roi['savings_percentage']:.1f}%")
print(f"Payback Period: {roi['payback_months']:.1f} months")
print(f"12-Month ROI: {roi['roi_percentage']:.1f}%")
print(f"Net Benefit (1 year): ₹{roi['net_benefit']:,.2f}")
```

---

## 6. Practice Exercises

### Exercise 1: Multi-Route Cost Analysis

Given this network data, calculate total costs and find optimization opportunities:

```python
network_data = pd.DataFrame({
    'origin': ['Mumbai', 'Mumbai', 'Delhi', 'Delhi', 'Bangalore'],
    'destination': ['Delhi', 'Bangalore', 'Kolkata', 'Chennai', 'Chennai'],
    'distance_km': [1400, 840, 1450, 2180, 350],
    'pallets': [150, 120, 180, 95, 110],
    'vehicle_capacity': [200, 200, 200, 200, 200],
    'cost_per_km': [25, 25, 25, 25, 25]
})

# Tasks:
# 1. Calculate total transportation cost for network
# 2. Calculate vehicle utilization for each route
# 3. Calculate cost per pallet for each route
# 4. Identify which routes have poor utilization (<70%)
# 5. Calculate potential savings if underutilized routes were consolidated
```

### Exercise 2: Optimization Impact Assessment

Compare two scenarios and calculate savings:

```python
# Current scenario (no optimization)
current_routes = pd.DataFrame({
    'route': ['Route A', 'Route B', 'Route C', 'Route D'],
    'cost': [45000, 52000, 38000, 61000],
    'distance_km': [1400, 1650, 1200, 1800],
    'pallets': [150, 165, 125, 185]
})

# Optimized scenario (with Quantyf)
optimized_routes = pd.DataFrame({
    'route': ['Optimized 1', 'Optimized 2', 'Optimized 3'],
    'cost': [42000, 48000, 58000],
    'distance_km': [1380, 1600, 1750],
    'pallets': [160, 170, 170]
})

# Tasks:
# 1. Calculate total cost savings
# 2. Calculate savings percentage
# 3. Calculate cost per pallet improvement
# 4. Calculate cost per km improvement
# 5. If optimization costs ₹3 lakhs, calculate payback period (assume monthly data)
```

---

## 🎯 Key Takeaways

1. ✅ **Total Cost** = Transportation + Handling + Inventory + Fixed costs
2. ✅ **KPIs** track efficiency: cost per pallet, cost per km, utilization
3. ✅ **Optimization** finds the lowest-cost solution meeting constraints
4. ✅ **ROI analysis** justifies investment in optimization tools
5. ✅ **Quantyf minimizes** total supply chain cost while meeting delivery requirements

---

## 📚 Next Steps

Continue to **Tutorial 15: Introduction to Linear Programming** to understand the math behind Quantyf's optimization!

You'll learn:
- Linear programming basics
- Objective functions and constraints
- Optimization algorithms
- How FICO Xpress works

---

## 📖 Additional Resources

- "Supply Chain Management" by Sunil Chopra
- "The Logistics and Supply Chain Toolkit" by Gwynne Richards
- Council of Supply Chain Management Professionals (CSCMP)

Happy Learning! 🚀

