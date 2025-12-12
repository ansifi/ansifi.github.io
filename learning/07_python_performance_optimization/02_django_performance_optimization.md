# Django Performance Optimization

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Optimize Django ORM queries and avoid N+1 problems
- Use select_related and prefetch_related effectively
- Implement database query optimization techniques
- Optimize Django templates and middleware
- Use caching strategies effectively
- Monitor and profile Django applications

---

## 🎯 Common Django Performance Issues

1. **N+1 Query Problem**: Multiple database queries in loops
2. **Unnecessary Queries**: Fetching data not needed
3. **Inefficient Aggregations**: Multiple queries instead of one
4. **Template Rendering**: Slow template processing
5. **Middleware Overhead**: Unnecessary middleware execution

---

## 1. ORM Query Optimization

### Understanding QuerySet Evaluation

```python
# QuerySet is lazy - no database hit yet
users = User.objects.filter(is_active=True)

# Database query happens here
for user in users:
    print(user.email)

# Each iteration hits database - BAD!
for user in users:
    print(user.profile.bio)  # N+1 problem!
```

### select_related: Foreign Key Optimization

```python
# Bad: N+1 queries
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # One query per user!

# Good: Single query with JOIN
users = User.objects.select_related('profile').all()
for user in users:
    print(user.profile.bio)  # No additional queries!

# Multiple foreign keys
posts = Post.objects.select_related('author', 'category').all()
```

### prefetch_related: Reverse Foreign Key & Many-to-Many

```python
# Bad: Multiple queries for related objects
authors = Author.objects.all()
for author in authors:
    print(author.posts.all())  # One query per author!

# Good: Prefetch related objects
authors = Author.objects.prefetch_related('posts').all()
for author in authors:
    print(author.posts.all())  # No additional queries!

# Nested prefetch
authors = Author.objects.prefetch_related(
    'posts',
    'posts__comments',
    'posts__tags'
).all()
```

### only() and defer(): Fetch Only Needed Fields

```python
# Bad: Fetch all fields
users = User.objects.all()  # Fetches all columns

# Good: Fetch only needed fields
users = User.objects.only('id', 'email', 'username')

# Defer heavy fields
users = User.objects.defer('bio', 'avatar')  # Skip these fields
```

### values() and values_list(): Get Dictionaries/Tuples

```python
# Bad: Full model instances when only need data
users = User.objects.all()
emails = [user.email for user in users]

# Good: Direct values
emails = User.objects.values_list('email', flat=True)

# Multiple fields as dict
user_data = User.objects.values('id', 'email', 'username')
```

---

## 2. Aggregation and Annotation

### Efficient Aggregations

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Bad: Multiple queries
total_users = User.objects.count()
active_users = User.objects.filter(is_active=True).count()
total_posts = Post.objects.count()

# Good: Single query with aggregation
from django.db.models import Count, Q

stats = User.objects.aggregate(
    total=Count('id'),
    active=Count('id', filter=Q(is_active=True))
)

# Annotate querysets
users_with_post_count = User.objects.annotate(
    post_count=Count('posts')
).filter(post_count__gt=5)
```

### Subquery Optimization

```python
from django.db.models import OuterRef, Subquery

# Bad: Multiple queries
users = User.objects.all()
for user in users:
    user.latest_post = Post.objects.filter(author=user).latest('created_at')

# Good: Subquery
latest_posts = Post.objects.filter(
    author=OuterRef('pk')
).order_by('-created_at')[:1]

users = User.objects.annotate(
    latest_post_title=Subquery(
        latest_posts.values('title')
    )
)
```

---

## 3. Database Indexing

### Model Field Indexing

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    created_at = models.DateTimeField(db_index=True)
    
    # Composite index
    class Meta:
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
```

### Query Optimization with Indexes

```python
# Ensure queries use indexes
# Good: Uses index on created_at
recent_posts = Post.objects.filter(created_at__gte=last_week)

# Bad: Can't use index (function on column)
recent_posts = Post.objects.filter(
    created_at__year=2024
)  # Consider adding a year field or use range
```

---

## 4. Caching Strategies

### Per-View Caching

```python
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    return render(request, 'template.html')

# Vary cache by headers
@vary_on_headers('User-Agent')
@cache_page(60 * 15)
def my_view(request):
    return render(request, 'template.html')
```

### Template Fragment Caching

```django
{% load cache %}

{% cache 500 sidebar %}
    <div class="sidebar">
        {% for item in sidebar_items %}
            {{ item }}
        {% endfor %}
    </div>
{% endcache %}
```

### Low-Level Caching API

```python
from django.core.cache import cache

# Set cache
cache.set('my_key', 'my_value', timeout=3600)

# Get cache
value = cache.get('my_key')

# Get or set pattern
def get_or_set_user_data(user_id):
    cache_key = f'user_data_{user_id}'
    data = cache.get(cache_key)
    
    if data is None:
        data = expensive_operation(user_id)
        cache.set(cache_key, data, timeout=3600)
    
    return data
```

### Cache Backends

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Or use Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

---

## 5. Template Optimization

### Template Fragment Caching

```django
{% load cache %}

{% cache 300 user_profile user.id %}
    <div class="profile">
        <h2>{{ user.name }}</h2>
        <p>{{ user.bio }}</p>
    </div>
{% endcache %}
```

### Reduce Template Complexity

```django
{# Bad: Complex logic in template #}
{% for item in items %}
    {% if item.status == 'active' and item.price > 100 %}
        {% if item.category.name == 'electronics' %}
            {{ item.name }}
        {% endif %}
    {% endif %}
{% endfor %}

{# Good: Prepare data in view #}
# In view
filtered_items = [
    item for item in items 
    if item.status == 'active' 
    and item.price > 100 
    and item.category.name == 'electronics'
]

# In template
{% for item in filtered_items %}
    {{ item.name }}
{% endfor %}
```

### Use {% include %} Wisely

```django
{# Bad: Include in loop #}
{% for item in items %}
    {% include 'item_detail.html' %}
{% endfor %}

{# Good: Pass context efficiently #}
{% for item in items %}
    {% include 'item_detail.html' with item=item only %}
{% endfor %}
```

---

## 6. Middleware Optimization

### Optimize Middleware Order

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Custom middleware last
    'myapp.middleware.CustomMiddleware',
]
```

### Conditional Middleware Execution

```python
class ConditionalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for static files
        if request.path.startswith('/static/'):
            return self.get_response(request)
        
        # Your middleware logic
        response = self.get_response(request)
        return response
```

---

## 7. Database Connection Pooling

### Configure Connection Pooling

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Reuse connections for 10 minutes
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

---

## 8. Monitoring and Profiling

### Django Debug Toolbar

```python
# settings.py (development only!)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

### django-silk for Profiling

```python
# settings.py
INSTALLED_APPS = [
    'silk',
    # ...
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    # ...
]

# View profiling
@silk_profile(name='View Blog Post')
def blog_post(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post.html', {'post': post})
```

### Query Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

---

## 9. Practice Exercises

### Exercise 1: Fix N+1 Query Problem

Optimize this view:

```python
def user_posts_view(request):
    users = User.objects.all()
    context = {
        'users': users,
        'posts': []
    }
    for user in users:
        user_posts = Post.objects.filter(author=user)
        context['posts'].extend(user_posts)
    return render(request, 'users.html', context)
```

### Exercise 2: Optimize Aggregation

Optimize this function:

```python
def get_statistics():
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'total_posts': total_posts,
        'published_posts': published_posts,
    }
```

### Exercise 3: Implement Caching

Add caching to this expensive view:

```python
def expensive_dashboard(request):
    # Expensive operations
    stats = calculate_complex_statistics()
    recommendations = generate_recommendations(request.user)
    trends = analyze_trends()
    
    return render(request, 'dashboard.html', {
        'stats': stats,
        'recommendations': recommendations,
        'trends': trends,
    })
```

---

## 10. Solutions

<details>
<summary>Click to see solutions</summary>

### Solution 1: Fix N+1 Query Problem

```python
def user_posts_view(request):
    users = User.objects.prefetch_related('posts').all()
    context = {
        'users': users,
    }
    return render(request, 'users.html', context)

# In template, access posts directly
# {% for user in users %}
#     {% for post in user.posts.all %}
#         {{ post.title }}
#     {% endfor %}
# {% endfor %}
```

### Solution 2: Optimize Aggregation

```python
from django.db.models import Count, Q

def get_statistics():
    user_stats = User.objects.aggregate(
        total=Count('id'),
        active=Count('id', filter=Q(is_active=True))
    )
    
    post_stats = Post.objects.aggregate(
        total=Count('id'),
        published=Count('id', filter=Q(status='published'))
    )
    
    return {
        'total_users': user_stats['total'],
        'active_users': user_stats['active'],
        'total_posts': post_stats['total'],
        'published_posts': post_stats['published'],
    }
```

### Solution 3: Implement Caching

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def expensive_dashboard(request):
    cache_key = f'dashboard_{request.user.id}'
    data = cache.get(cache_key)
    
    if data is None:
        data = {
            'stats': calculate_complex_statistics(),
            'recommendations': generate_recommendations(request.user),
            'trends': analyze_trends(),
        }
        cache.set(cache_key, data, timeout=60 * 15)
    
    return render(request, 'dashboard.html', data)
```

</details>

---

## 🎯 Key Takeaways

1. ✅ Always use select_related for ForeignKey
2. ✅ Use prefetch_related for reverse ForeignKey and ManyToMany
3. ✅ Use only() and defer() to limit fields
4. ✅ Aggregate in database, not in Python
5. ✅ Add database indexes for frequently queried fields
6. ✅ Cache expensive operations
7. ✅ Profile before optimizing

---

## 📚 Next Steps

Next: **FastAPI Performance Optimization** - Learn async/await patterns, dependency injection, and high-performance API design.

