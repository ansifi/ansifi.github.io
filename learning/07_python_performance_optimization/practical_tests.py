"""
Practical Tests for Python/Django/FastAPI Performance Optimization

Run these tests to verify your understanding and measure performance improvements.
"""

import time
import cProfile
import pstats
from io import StringIO
from functools import lru_cache
from collections import defaultdict, Counter
import asyncio
import httpx


# ============================================================================
# Test 1: List Comprehension vs Loop Performance
# ============================================================================

def test_list_comprehension_performance():
    """Test performance difference between list comprehension and loops."""
    data = list(range(100000))
    
    # Method 1: Loop with append
    start = time.time()
    result1 = []
    for x in data:
        if x % 2 == 0:
            result1.append(x * 2)
    time1 = time.time() - start
    
    # Method 2: List comprehension
    start = time.time()
    result2 = [x * 2 for x in data if x % 2 == 0]
    time2 = time.time() - start
    
    assert result1 == result2, "Results should be identical"
    print(f"Loop with append: {time1:.4f}s")
    print(f"List comprehension: {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")
    return time1/time2 > 1.0  # List comprehension should be faster


# ============================================================================
# Test 2: Dictionary Lookup Performance
# ============================================================================

def test_dict_lookup_performance():
    """Test performance of dictionary vs list lookups."""
    size = 10000
    my_list = list(range(size))
    my_dict = {i: i for i in range(size)}
    lookup_value = size - 1
    
    # List lookup: O(n)
    start = time.time()
    for _ in range(1000):
        _ = lookup_value in my_list
    list_time = time.time() - start
    
    # Dict lookup: O(1)
    start = time.time()
    for _ in range(1000):
        _ = lookup_value in my_dict
    dict_time = time.time() - start
    
    print(f"List lookup (1000x): {list_time:.4f}s")
    print(f"Dict lookup (1000x): {dict_time:.4f}s")
    print(f"Speedup: {list_time/dict_time:.2f}x")
    return dict_time < list_time


# ============================================================================
# Test 3: Caching Performance
# ============================================================================

def fibonacci_uncached(n):
    """Uncached Fibonacci calculation."""
    if n < 2:
        return n
    return fibonacci_uncached(n-1) + fibonacci_uncached(n-2)


@lru_cache(maxsize=128)
def fibonacci_cached(n):
    """Cached Fibonacci calculation."""
    if n < 2:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)


def test_caching_performance():
    """Test performance improvement with caching."""
    n = 30
    
    # Uncached
    start = time.time()
    result1 = fibonacci_uncached(n)
    time1 = time.time() - start
    
    # Cached
    start = time.time()
    result2 = fibonacci_cached(n)
    time2 = time.time() - start
    
    assert result1 == result2, "Results should be identical"
    print(f"Uncached Fibonacci({n}): {time1:.4f}s")
    print(f"Cached Fibonacci({n}): {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")
    return time2 < time1


# ============================================================================
# Test 4: Generator vs List Performance
# ============================================================================

def test_generator_performance():
    """Test memory efficiency of generators."""
    import sys
    
    # List: Loads everything into memory
    def create_list(n):
        return [i**2 for i in range(n)]
    
    # Generator: Memory efficient
    def create_generator(n):
        return (i**2 for i in range(n))
    
    n = 1000000
    
    # Memory usage
    my_list = create_list(n)
    my_gen = create_generator(n)
    
    list_size = sys.getsizeof(my_list)
    gen_size = sys.getsizeof(my_gen)
    
    print(f"List memory: {list_size:,} bytes")
    print(f"Generator memory: {gen_size:,} bytes")
    print(f"Memory savings: {(list_size/gen_size):.0f}x")
    
    return gen_size < list_size


# ============================================================================
# Test 5: String Concatenation Performance
# ============================================================================

def test_string_concatenation():
    """Test performance of different string concatenation methods."""
    words = ["word"] * 10000
    
    # Method 1: += operator
    start = time.time()
    result1 = ""
    for word in words:
        result1 += word
    time1 = time.time() - start
    
    # Method 2: join()
    start = time.time()
    result2 = "".join(words)
    time2 = time.time() - start
    
    assert result1 == result2, "Results should be identical"
    print(f"+= operator: {time1:.4f}s")
    print(f"join() method: {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")
    return time2 < time1


# ============================================================================
# Test 6: Collections Module Performance
# ============================================================================

def test_collections_performance():
    """Test performance of collections module."""
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"] * 1000
    
    # Method 1: Manual counting
    start = time.time()
    counts1 = {}
    for word in words:
        if word in counts1:
            counts1[word] += 1
        else:
            counts1[word] = 1
    time1 = time.time() - start
    
    # Method 2: Counter
    start = time.time()
    counts2 = Counter(words)
    time2 = time.time() - start
    
    assert counts1 == dict(counts2), "Results should be identical"
    print(f"Manual counting: {time1:.4f}s")
    print(f"Counter: {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")
    return time2 < time1


# ============================================================================
# Test 7: Async Performance
# ============================================================================

async def fetch_url_async(url: str):
    """Simulate async URL fetch."""
    await asyncio.sleep(0.1)  # Simulate network delay
    return f"Data from {url}"


async def test_async_performance():
    """Test async vs sync performance."""
    urls = [f"https://api{i}.com" for i in range(10)]
    
    # Sequential async (bad)
    start = time.time()
    results1 = []
    for url in urls:
        result = await fetch_url_async(url)
        results1.append(result)
    time1 = time.time() - start
    
    # Concurrent async (good)
    start = time.time()
    results2 = await asyncio.gather(*[fetch_url_async(url) for url in urls])
    time2 = time.time() - start
    
    assert len(results1) == len(results2)
    print(f"Sequential async: {time1:.4f}s")
    print(f"Concurrent async: {time2:.4f}s")
    print(f"Speedup: {time1/time2:.2f}x")
    return time2 < time1


# ============================================================================
# Test 8: Profiling Example
# ============================================================================

def slow_function():
    """Function with performance issues."""
    result = []
    for i in range(10000):
        for j in range(100):
            result.append(i * j)
    return result


def test_profiling():
    """Demonstrate profiling."""
    profiler = cProfile.Profile()
    profiler.enable()
    slow_function()
    profiler.disable()
    
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(10)
    
    print("Top 10 functions by cumulative time:")
    print(s.getvalue())
    return True


# ============================================================================
# Test Runner
# ============================================================================

def run_all_tests():
    """Run all performance tests."""
    print("=" * 70)
    print("Python Performance Optimization - Practical Tests")
    print("=" * 70)
    
    tests = [
        ("List Comprehension", test_list_comprehension_performance),
        ("Dictionary Lookup", test_dict_lookup_performance),
        ("Caching", test_caching_performance),
        ("Generator", test_generator_performance),
        ("String Concatenation", test_string_concatenation),
        ("Collections Module", test_collections_performance),
        ("Profiling", test_profiling),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"Test: {name}")
        print(f"{'='*70}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            results.append((name, result, None))
            print(f"✓ {name}: PASSED")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"✗ {name}: FAILED - {e}")
    
    # Async test separately
    print(f"\n{'='*70}")
    print("Test: Async Performance")
    print(f"{'='*70}")
    try:
        result = asyncio.run(test_async_performance())
        results.append(("Async Performance", result, None))
        print("✓ Async Performance: PASSED")
    except Exception as e:
        results.append(("Async Performance", False, str(e)))
        print(f"✗ Async Performance: FAILED - {e}")
    
    # Summary
    print(f"\n{'='*70}")
    print("Test Summary")
    print(f"{'='*70}")
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for name, result, error in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if error:
            print(f"  Error: {error}")


if __name__ == "__main__":
    run_all_tests()

