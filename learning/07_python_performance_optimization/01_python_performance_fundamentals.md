# Python Performance Optimization Fundamentals

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Understand Python performance bottlenecks and profiling techniques
- Master efficient data structures and algorithms
- Learn memory optimization strategies
- Implement caching and memoization patterns
- Optimize I/O operations and database queries

---

## 🎯 Why Performance Matters

Performance optimization is critical for:
- **Scalability**: Handle more users and requests
- **Cost Efficiency**: Reduce server costs and resource usage
- **User Experience**: Faster response times
- **Competitive Advantage**: Better performance than competitors

---

## 1. Profiling and Benchmarking

### Using cProfile for Performance Analysis

```python
import cProfile
import pstats
from io import StringIO

def slow_function():
    """Example slow function."""
    result = []
    for i in range(100000):
        result.append(i * 2)
    return result

# Profile the function
profiler = cProfile.Profile()
profiler.enable()
slow_function()
profiler.disable()

# Print statistics
s = StringIO()
ps = pstats.Stats(profiler, stream=s)
ps.sort_stats('cumulative')
ps.print_stats(20)
print(s.getvalue())
```

### Using timeit for Micro-benchmarks

```python
import timeit

# Compare two approaches
def approach1():
    return [i * 2 for i in range(1000)]

def approach2():
    result = []
    for i in range(1000):
        result.append(i * 2)
    return result

# Benchmark both
time1 = timeit.timeit(approach1, number=10000)
time2 = timeit.timeit(approach2, number=10000)

print(f"List comprehension: {time1:.4f}s")
print(f"Loop with append: {time2:.4f}s")
```

### Using memory_profiler

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    """Function that uses a lot of memory."""
    data = []
    for i in range(100000):
        data.append([j for j in range(100)])
    return data

# Run: python -m memory_profiler script.py
```

---

## 2. Efficient Data Structures

### Lists vs Tuples vs Sets

```python
# Lists: Mutable, ordered, allows duplicates
my_list = [1, 2, 3, 4, 5]

# Tuples: Immutable, ordered, faster than lists
my_tuple = (1, 2, 3, 4, 5)

# Sets: Mutable, unordered, unique elements, O(1) lookup
my_set = {1, 2, 3, 4, 5}

# Performance comparison
import timeit

# List lookup: O(n)
list_time = timeit.timeit('5 in my_list', 
                          setup='my_list = list(range(1000))', 
                          number=10000)

# Set lookup: O(1)
set_time = timeit.timeit('5 in my_set', 
                         setup='my_set = set(range(1000))', 
                         number=10000)

print(f"List lookup: {list_time:.4f}s")
print(f"Set lookup: {set_time:.4f}s")
```

### Dictionary Optimization

```python
# Prefer dict.get() over dict[key] with try/except
# Bad: Slow exception handling
def bad_lookup(d, key):
    try:
        return d[key]
    except KeyError:
        return None

# Good: Fast built-in method
def good_lookup(d, key):
    return d.get(key, None)

# Use dict comprehensions
# Bad: Slow
result = {}
for key, value in data.items():
    if value > 10:
        result[key] = value * 2

# Good: Fast
result = {k: v * 2 for k, v in data.items() if v > 10}
```

### Collections Module

```python
from collections import defaultdict, Counter, deque

# defaultdict: Avoid key existence checks
# Bad
d = {}
for word in words:
    if word not in d:
        d[word] = []
    d[word].append(len(word))

# Good
d = defaultdict(list)
for word in words:
    d[word].append(len(word))

# Counter: Fast counting
from collections import Counter
word_counts = Counter(words)

# deque: Fast append/pop from both ends
from collections import deque
queue = deque([1, 2, 3])
queue.append(4)      # O(1)
queue.popleft()      # O(1) - faster than list.pop(0) which is O(n)
```

---

## 3. Algorithm Optimization

### Avoid Unnecessary Loops

```python
# Bad: Nested loops O(n²)
def find_common_elements(list1, list2):
    common = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2:
                common.append(item1)
    return common

# Good: Set intersection O(n)
def find_common_elements(list1, list2):
    return list(set(list1) & set(list2))
```

### Use Generators for Large Datasets

```python
# Bad: Loads everything into memory
def read_large_file_bad(filename):
    with open(filename) as f:
        return f.readlines()  # Loads entire file

# Good: Generator - memory efficient
def read_large_file_good(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Usage
for line in read_large_file_good('large_file.txt'):
    process(line)
```

### List Comprehensions vs Loops

```python
# List comprehension: Faster and more Pythonic
squares = [x**2 for x in range(1000)]

# Generator expression: Memory efficient
squares_gen = (x**2 for x in range(1000))

# Filter and map: Use comprehensions instead
# Bad
result = list(map(lambda x: x * 2, filter(lambda x: x > 10, numbers)))

# Good
result = [x * 2 for x in numbers if x > 10]
```

---

## 4. Memory Optimization

### Use __slots__ for Classes

```python
# Bad: Dynamic attribute dictionary
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Good: Fixed attributes, less memory
class User:
    __slots__ = ['name', 'email']
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Memory savings: ~40-50% for classes with many instances
```

### String Optimization

```python
# Bad: String concatenation in loop
result = ""
for word in words:
    result += word  # Creates new string each time

# Good: Join method
result = "".join(words)

# For many strings, use list then join
parts = []
for word in words:
    parts.append(word)
result = "".join(parts)
```

### Garbage Collection

```python
import gc

# Disable automatic GC for critical sections
gc.disable()
# ... critical performance code ...
gc.enable()

# Force collection
gc.collect()

# Check memory usage
import sys
size = sys.getsizeof(my_object)
```

---

## 5. Caching and Memoization

### functools.lru_cache

```python
from functools import lru_cache
import time

# Without caching
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# With caching
@lru_cache(maxsize=128)
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

# Performance comparison
start = time.time()
fibonacci(30)
print(f"Without cache: {time.time() - start:.4f}s")

start = time.time()
fibonacci_cached(30)
print(f"With cache: {time.time() - start:.4f}s")
```

### Custom Caching Decorator

```python
from functools import wraps
from datetime import datetime, timedelta

def cache_with_ttl(ttl_seconds=60):
    """Cache decorator with time-to-live."""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            
            if key in cache:
                result, timestamp = cache[key]
                if datetime.now() - timestamp < timedelta(seconds=ttl_seconds):
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, datetime.now())
            return result
        
        return wrapper
    return decorator

@cache_with_ttl(ttl_seconds=300)
def expensive_api_call(user_id):
    # Simulate expensive operation
    time.sleep(1)
    return f"Data for user {user_id}"
```

---

## 6. I/O Optimization

### Async I/O with asyncio

```python
import asyncio
import aiohttp

# Synchronous: Slow
def fetch_urls_sync(urls):
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.text)
    return results

# Asynchronous: Fast
async def fetch_urls_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
    return results

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

# Usage
urls = ['http://example.com'] * 10
results = asyncio.run(fetch_urls_async(urls))
```

### Batch Processing

```python
# Process items in batches instead of one-by-one
def process_in_batches(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        process_batch(batch)

def process_batch(batch):
    # Process entire batch at once
    pass
```

---

## 7. Practice Exercises

### Exercise 1: Optimize List Processing

Optimize this function to be faster:

```python
def process_data(data):
    """Process data and return filtered results."""
    result = []
    for item in data:
        if item > 10:
            result.append(item * 2)
    return result

# Your optimized version here
```

### Exercise 2: Implement Caching

Create a caching decorator that caches function results based on arguments:

```python
# Your implementation here
@cache_decorator
def expensive_calculation(n):
    # Simulate expensive operation
    return sum(i**2 for i in range(n))
```

### Exercise 3: Optimize Database Query

Optimize this N+1 query problem:

```python
# Bad: N+1 queries
def get_user_posts_bad(user_ids):
    posts = []
    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        user_posts = Post.objects.filter(user=user)
        posts.extend(user_posts)
    return posts

# Your optimized version here
```

---

## 8. Solutions

<details>
<summary>Click to see solutions</summary>

### Solution 1: Optimize List Processing

```python
def process_data(data):
    """Optimized version using list comprehension."""
    return [item * 2 for item in data if item > 10]
```

### Solution 2: Implement Caching

```python
from functools import wraps

def cache_decorator(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper
```

### Solution 3: Optimize Database Query

```python
# Good: Single query with select_related/prefetch_related
def get_user_posts_good(user_ids):
    return Post.objects.filter(user_id__in=user_ids).select_related('user')
```

</details>

---

## 🎯 Key Takeaways

1. ✅ Always profile before optimizing
2. ✅ Choose the right data structure for the job
3. ✅ Use generators for large datasets
4. ✅ Cache expensive computations
5. ✅ Optimize I/O operations with async
6. ✅ Use list comprehensions and built-in functions

---

## 📚 Next Steps

Next: **Django Performance Optimization** - Learn to optimize Django ORM queries, middleware, and templates.

