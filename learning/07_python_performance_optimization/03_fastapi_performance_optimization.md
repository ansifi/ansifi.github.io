# FastAPI Performance Optimization

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Master async/await patterns for concurrent operations
- Optimize database queries with async ORMs
- Implement efficient dependency injection
- Use background tasks and task queues
- Optimize response serialization
- Implement caching strategies
- Monitor and profile FastAPI applications

---

## 🎯 FastAPI Performance Advantages

- **Async/Await**: Native support for concurrent operations
- **Type Hints**: Better performance through type checking
- **Pydantic**: Fast data validation
- **Automatic Docs**: OpenAPI/Swagger generation
- **High Performance**: Comparable to Node.js and Go

---

## 1. Async/Await Patterns

### Basic Async Endpoints

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# Synchronous: Blocks thread
@app.get("/sync")
def sync_endpoint():
    time.sleep(1)  # Blocks!
    return {"message": "Hello"}

# Asynchronous: Non-blocking
@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(1)  # Doesn't block!
    return {"message": "Hello"}
```

### Concurrent Requests

```python
import httpx
import asyncio

async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Sequential: Slow
@app.get("/sequential")
async def sequential():
    data1 = await fetch_data("https://api1.com")
    data2 = await fetch_data("https://api2.com")
    data3 = await fetch_data("https://api3.com")
    return {"data1": data1, "data2": data2, "data3": data3}

# Concurrent: Fast
@app.get("/concurrent")
async def concurrent():
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com")
    )
    return {
        "data1": results[0],
        "data2": results[1],
        "data3": results[2]
    }
```

### Database Operations with Async

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Async database operations
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        return user
```

---

## 2. Database Query Optimization

### Async ORM Best Practices

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Bad: N+1 queries
@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    # This triggers another query
    posts = await db.execute(select(Post).where(Post.user_id == user_id))
    return {"user": user, "posts": posts.scalars().all()}

# Good: Eager loading
@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return {"user": user, "posts": user.posts}
```

### Connection Pooling

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,           # Number of connections
    max_overflow=10,        # Additional connections
    pool_pre_ping=True,     # Verify connections
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=False
)
```

### Batch Operations

```python
# Bad: Individual inserts
@app.post("/users/batch")
async def create_users_bad(users: list[UserCreate], db: AsyncSession):
    for user_data in users:
        user = User(**user_data.dict())
        db.add(user)
        await db.commit()  # One commit per user!

# Good: Batch insert
@app.post("/users/batch")
async def create_users_good(users: list[UserCreate], db: AsyncSession):
    user_objects = [User(**user.dict()) for user in users]
    db.add_all(user_objects)
    await db.commit()  # Single commit
    return {"created": len(user_objects)}
```

---

## 3. Dependency Injection Optimization

### Efficient Dependencies

```python
from fastapi import Depends
from functools import lru_cache

# Bad: Recreated every request
def get_db():
    return database.connect()

# Good: Dependency with caching
@lru_cache()
def get_settings():
    return Settings()

# Async dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Usage
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

### Shared Dependencies

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    # Validate token once
    user = await validate_token(token.credentials)
    if not user:
        raise HTTPException(status_code=401)
    return user

@app.get("/profile")
async def get_profile(user: User = Depends(get_current_user)):
    return user

@app.get("/posts")
async def get_posts(user: User = Depends(get_current_user)):
    return await get_user_posts(user.id)
```

---

## 4. Response Optimization

### Response Models

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    
    class Config:
        from_attributes = True  # For SQLAlchemy models

# Fast serialization
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await get_user_from_db(user_id)
    return user  # Automatically serialized
```

### Streaming Responses

```python
from fastapi.responses import StreamingResponse
import asyncio

async def generate_large_data():
    for i in range(1000):
        yield f"data chunk {i}\n"
        await asyncio.sleep(0.01)

@app.get("/stream")
async def stream_data():
    return StreamingResponse(
        generate_large_data(),
        media_type="text/plain"
    )
```

### JSON Response Optimization

```python
from fastapi.responses import JSONResponse
from orjson import dumps

# Use orjson for faster JSON serialization
app = FastAPI()

@app.get("/fast-json")
async def fast_json():
    data = {"message": "Hello", "items": list(range(1000))}
    return JSONResponse(content=data)
```

---

## 5. Background Tasks

### Simple Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Simulate email sending
    print(f"Sending email to {email}: {message}")

@app.post("/send-email")
async def send_email_endpoint(
    email: str,
    message: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, message)
    return {"message": "Email queued"}
```

### Task Queue with Celery

```python
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_large_file(file_path: str):
    # Long-running task
    return process_file(file_path)

@app.post("/process-file")
async def process_file_endpoint(file_path: str):
    task = process_large_file.delay(file_path)
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "status": task.status,
        "result": task.result if task.ready() else None
    }
```

---

## 6. Caching Strategies

### In-Memory Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

cache = {}
cache_ttl = {}

def get_cached(key: str, ttl: int = 300):
    if key in cache:
        if datetime.now() < cache_ttl[key]:
            return cache[key]
        else:
            del cache[key]
            del cache_ttl[key]
    return None

def set_cached(key: str, value: any, ttl: int = 300):
    cache[key] = value
    cache_ttl[key] = datetime.now() + timedelta(seconds=ttl)

@app.get("/cached-data/{key}")
async def get_cached_data(key: str):
    cached = get_cached(key)
    if cached:
        return cached
    
    # Expensive operation
    data = await expensive_operation(key)
    set_cached(key, data)
    return data
```

### Redis Caching

```python
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost:6379")

@app.get("/redis-cached/{key}")
async def get_redis_cached(key: str):
    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)
    
    data = await expensive_operation(key)
    await redis_client.setex(
        key,
        300,  # TTL in seconds
        json.dumps(data)
    )
    return data
```

### Response Caching Middleware

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = await redis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/cached-endpoint")
@cache(expire=60)  # Cache for 60 seconds
async def cached_endpoint():
    return {"data": await expensive_operation()}
```

---

## 7. Request/Response Optimization

### Compression

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/large-response")
async def large_response():
    return {"data": list(range(10000))}  # Automatically compressed
```

### Pagination

```python
from fastapi import Query

@app.get("/items")
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    items = await db.execute(
        select(Item).offset(skip).limit(limit)
    )
    total = await db.scalar(select(func.count(Item.id)))
    
    return {
        "items": items.scalars().all(),
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

### Field Selection

```python
from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    fields: Optional[str] = Query(None)
):
    user = await get_user_from_db(user_id)
    
    if fields:
        field_list = fields.split(",")
        return {
            field: getattr(user, field)
            for field in field_list
            if hasattr(user, field)
        }
    
    return user
```

---

## 8. Monitoring and Profiling

### Request Timing Middleware

```python
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(TimingMiddleware)
```

### Logging

```python
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {process_time:.3f}s"
    )
    return response
```

### APM Integration

```python
# Using Sentry
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

---

## 9. Practice Exercises

### Exercise 1: Convert to Async

Convert this synchronous endpoint to async:

```python
@app.get("/data")
def get_data():
    data1 = requests.get("https://api1.com").json()
    data2 = requests.get("https://api2.com").json()
    return {"data1": data1, "data2": data2}
```

### Exercise 2: Optimize Database Query

Optimize this endpoint to avoid N+1 queries:

```python
@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    posts = []
    for post in user.posts:
        comments = await db.execute(
            select(Comment).where(Comment.post_id == post.id)
        )
        posts.append({"post": post, "comments": comments.scalars().all()})
    return posts
```

### Exercise 3: Implement Caching

Add caching to this expensive endpoint:

```python
@app.get("/expensive-calculation/{input_value}")
async def expensive_calculation(input_value: int):
    # Simulate expensive operation
    result = sum(i**2 for i in range(input_value * 1000))
    return {"result": result}
```

---

## 10. Solutions

<details>
<summary>Click to see solutions</summary>

### Solution 1: Convert to Async

```python
import httpx

@app.get("/data")
async def get_data():
    async with httpx.AsyncClient() as client:
        data1, data2 = await asyncio.gather(
            client.get("https://api1.com"),
            client.get("https://api2.com")
        )
        return {
            "data1": data1.json(),
            "data2": data2.json()
        }
```

### Solution 2: Optimize Database Query

```python
from sqlalchemy.orm import selectinload

@app.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.posts).selectinload(Post.comments)
        )
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return [
        {"post": post, "comments": post.comments}
        for post in user.posts
    ]
```

### Solution 3: Implement Caching

```python
from functools import lru_cache
import hashlib

cache = {}

@app.get("/expensive-calculation/{input_value}")
async def expensive_calculation(input_value: int):
    cache_key = f"calc_{input_value}"
    
    if cache_key in cache:
        return {"result": cache[cache_key], "cached": True}
    
    result = sum(i**2 for i in range(input_value * 1000))
    cache[cache_key] = result
    return {"result": result, "cached": False}
```

</details>

---

## 🎯 Key Takeaways

1. ✅ Use async/await for I/O-bound operations
2. ✅ Use asyncio.gather() for concurrent operations
3. ✅ Optimize database queries with selectinload
4. ✅ Use connection pooling for databases
5. ✅ Implement caching for expensive operations
6. ✅ Use background tasks for long-running operations
7. ✅ Monitor and profile your application

---

## 📚 Next Steps

Next: **Java/Spring Boot Microservices Architecture** - Learn microservices patterns, service discovery, API gateways, and distributed systems.

