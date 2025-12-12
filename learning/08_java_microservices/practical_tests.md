# Java/Spring Boot Microservices - Practical Tests

## Test Scenarios and Exercises

This document contains practical tests and exercises to verify your understanding of microservices architecture and Spring Boot implementation.

---

## Test 1: Service Creation

### Objective
Create a complete microservice from scratch.

### Requirements
1. Create a **Notification Service** with the following:
   - REST endpoints for sending emails and SMS
   - Entity: `Notification` with fields: id, recipient, message, type, status, createdAt
   - Service layer with business logic
   - Repository layer for data access
   - Eureka client registration
   - H2 in-memory database

### Expected Endpoints
```
POST   /api/notifications/email
POST   /api/notifications/sms
GET    /api/notifications/{id}
GET    /api/notifications
DELETE /api/notifications/{id}
```

### Test Cases
```java
// Test 1: Create email notification
POST /api/notifications/email
Body: {
    "recipient": "user@example.com",
    "message": "Welcome to our service"
}
Expected: 201 Created

// Test 2: Get notification by ID
GET /api/notifications/1
Expected: 200 OK with notification data

// Test 3: Get all notifications
GET /api/notifications
Expected: 200 OK with list of notifications
```

---

## Test 2: Service-to-Service Communication

### Objective
Implement communication between Order Service and User Service using Feign.

### Requirements
1. Update Order Service to:
   - Call User Service to validate user exists before creating order
   - Use Feign client for HTTP communication
   - Implement circuit breaker pattern
   - Add retry logic (3 attempts with 1s delay)
   - Handle fallback when User Service is unavailable

### Implementation Checklist
- [ ] Create Feign client interface for User Service
- [ ] Configure circuit breaker with Resilience4j
- [ ] Implement fallback method
- [ ] Add retry configuration
- [ ] Test with User Service running
- [ ] Test with User Service down (verify fallback)

### Test Cases
```java
// Test 1: Create order with valid user
POST /api/orders
Body: {
    "userId": 1,
    "totalAmount": 100.00
}
Expected: 201 Created

// Test 2: Create order with invalid user
POST /api/orders
Body: {
    "userId": 999,
    "totalAmount": 100.00
}
Expected: 404 Not Found or fallback behavior

// Test 3: Create order when User Service is down
// Stop User Service, then:
POST /api/orders
Body: {
    "userId": 1,
    "totalAmount": 100.00
}
Expected: Order created with fallback user validation
```

---

## Test 3: API Gateway Configuration

### Objective
Configure API Gateway with routing, authentication, and rate limiting.

### Requirements
1. Configure routes for:
   - User Service: `/api/users/**`
   - Order Service: `/api/orders/**`
   - Notification Service: `/api/notifications/**`

2. Implement authentication filter:
   - Validate JWT token in Authorization header
   - Extract user ID from token
   - Add user ID to request headers
   - Return 401 if token is invalid

3. Add rate limiting:
   - 10 requests per second per IP
   - Burst capacity: 20 requests

### Test Cases
```java
// Test 1: Access without token
GET http://localhost:8080/api/users/1
Expected: 401 Unauthorized

// Test 2: Access with valid token
GET http://localhost:8080/api/users/1
Headers: Authorization: Bearer <valid-jwt-token>
Expected: 200 OK

// Test 3: Rate limiting
// Send 25 requests rapidly
GET http://localhost:8080/api/users/1
Headers: Authorization: Bearer <valid-jwt-token>
Expected: First 20 succeed, then 429 Too Many Requests
```

---

## Test 4: Circuit Breaker Implementation

### Objective
Implement and test circuit breaker pattern.

### Requirements
1. Configure circuit breaker for User Service client:
   - Sliding window size: 10
   - Minimum calls: 5
   - Failure rate threshold: 50%
   - Wait duration in open state: 5 seconds

2. Test circuit breaker states:
   - Closed: Normal operation
   - Open: After failures exceed threshold
   - Half-open: After wait duration

### Test Scenario
```java
// Step 1: Make 5 successful calls (circuit closed)
for (int i = 0; i < 5; i++) {
    GET /api/users/1
    Expected: 200 OK
}

// Step 2: Make 5 failed calls (circuit opens)
// Stop User Service
for (int i = 0; i < 5; i++) {
    GET /api/users/1
    Expected: Fallback response
}

// Step 3: Verify circuit is open
GET /api/users/1
Expected: Immediate fallback (circuit open)

// Step 4: Wait 5 seconds, then test half-open
// Start User Service
Thread.sleep(5000);
GET /api/users/1
Expected: Attempts to call service (half-open state)
```

---

## Test 5: Distributed Transaction (Saga Pattern)

### Objective
Implement Saga pattern for distributed transaction.

### Requirements
1. Create Order Saga that:
   - Creates order
   - Reserves inventory (Inventory Service)
   - Processes payment (Payment Service)
   - Sends notification (Notification Service)
   - Implements compensating transactions on failure

### Saga Steps
```
1. Create Order → Order Service
2. Reserve Inventory → Inventory Service
3. Process Payment → Payment Service
4. Send Notification → Notification Service

If any step fails:
- Rollback previous steps
- Cancel order
- Release inventory
- Refund payment
```

### Test Cases
```java
// Test 1: Successful saga
POST /api/orders/saga
Body: {
    "userId": 1,
    "items": [
        {"productId": 1, "quantity": 2}
    ]
}
Expected: Order created, inventory reserved, payment processed, notification sent

// Test 2: Failure in payment step
// Make Payment Service return error
POST /api/orders/saga
Body: {
    "userId": 1,
    "items": [
        {"productId": 1, "quantity": 2}
    ]
}
Expected: Order cancelled, inventory released, payment refunded

// Test 3: Failure in inventory step
// Make Inventory Service return insufficient stock
POST /api/orders/saga
Body: {
    "userId": 1,
    "items": [
        {"productId": 1, "quantity": 1000}
    ]
}
Expected: Order cancelled, no payment processed
```

---

## Test 6: Service Discovery

### Objective
Test service discovery with Eureka.

### Requirements
1. Start Eureka Server
2. Register three services:
   - User Service (port 8081)
   - Order Service (port 8082)
   - Notification Service (port 8083)

3. Verify services are registered:
   - Check Eureka dashboard: http://localhost:8761
   - Services should appear in "Instances currently registered with Eureka"

### Test Cases
```bash
# Test 1: Check Eureka dashboard
curl http://localhost:8761/eureka/apps

# Expected: JSON with all registered services

# Test 2: Service discovery via Feign
# Order Service should discover User Service by name
GET http://localhost:8082/api/orders/1

# Expected: Order Service calls User Service using service name
```

---

## Test 7: Configuration Management

### Objective
Implement centralized configuration with Spring Cloud Config.

### Requirements
1. Create Config Server
2. Store configuration in Git repository
3. Configure services to use Config Server
4. Test dynamic configuration refresh

### Configuration Files
```yaml
# application.yml in Git repo
user-service:
  db:
    url: jdbc:h2:mem:userdb
  features:
    email-verification: true

order-service:
  payment:
    timeout: 30
  features:
    auto-confirm: false
```

### Test Cases
```java
// Test 1: Service reads config from Config Server
// Start Config Server and User Service
GET http://localhost:8081/actuator/configprops
Expected: Configuration from Config Server

// Test 2: Refresh configuration
POST http://localhost:8081/actuator/refresh
Expected: Configuration refreshed

// Test 3: Change config in Git and refresh
// Update config in Git repo
POST http://localhost:8081/actuator/refresh
Expected: New configuration applied
```

---

## Test 8: Distributed Tracing

### Objective
Implement distributed tracing with Zipkin.

### Requirements
1. Start Zipkin server
2. Configure all services for tracing
3. Make requests across multiple services
4. Verify traces in Zipkin UI

### Test Scenario
```java
// Make request that goes through multiple services
GET http://localhost:8080/api/orders/1
// This goes: API Gateway → Order Service → User Service

// Check Zipkin UI: http://localhost:9411
// Expected: Trace showing all service calls with timing
```

---

## Test 9: Performance Testing

### Objective
Test microservices performance and scalability.

### Requirements
1. Use Apache JMeter or similar tool
2. Test endpoints under load:
   - 100 concurrent users
   - 1000 requests per second
   - Duration: 5 minutes

3. Monitor:
   - Response times
   - Error rates
   - Resource usage (CPU, memory)
   - Database connections

### Test Scenarios
```bash
# Scenario 1: Read-heavy workload
GET /api/users/{id} - 80% of requests
GET /api/orders/{id} - 15% of requests
GET /api/notifications/{id} - 5% of requests

# Scenario 2: Write-heavy workload
POST /api/users - 30% of requests
POST /api/orders - 50% of requests
POST /api/notifications - 20% of requests

# Expected Results:
# - Response time < 200ms (p95)
# - Error rate < 1%
# - No memory leaks
```

---

## Test 10: Security Implementation

### Objective
Implement security across microservices.

### Requirements
1. Implement JWT authentication
2. Secure all endpoints
3. Test authorization
4. Implement API key for service-to-service communication

### Test Cases
```java
// Test 1: Unauthenticated request
GET http://localhost:8080/api/users/1
Expected: 401 Unauthorized

// Test 2: Authenticated request with valid token
GET http://localhost:8080/api/users/1
Headers: Authorization: Bearer <valid-jwt-token>
Expected: 200 OK

// Test 3: Authenticated request with expired token
GET http://localhost:8080/api/users/1
Headers: Authorization: Bearer <expired-jwt-token>
Expected: 401 Unauthorized

// Test 4: Service-to-service communication
// Order Service calling User Service
// Should use service API key
Expected: Successful call with service authentication
```

---

## Evaluation Criteria

### For Each Test:
- **Functionality** (40%): Does it work correctly?
- **Code Quality** (30%): Clean, maintainable code?
- **Best Practices** (20%): Following microservices patterns?
- **Documentation** (10%): Clear comments and documentation?

### Overall Score:
- **90-100%**: Excellent - Production ready
- **80-89%**: Good - Minor improvements needed
- **70-79%**: Satisfactory - Needs refactoring
- **Below 70%**: Needs significant work

---

## Additional Challenges

### Challenge 1: Event-Driven Architecture
Convert synchronous communication to asynchronous using message queues (RabbitMQ/Kafka).

### Challenge 2: CQRS Pattern
Implement Command Query Responsibility Segregation for Order Service.

### Challenge 3: API Versioning
Implement API versioning strategy for backward compatibility.

### Challenge 4: Blue-Green Deployment
Set up blue-green deployment strategy for zero-downtime updates.

---

## Resources

- Spring Cloud Documentation: https://spring.io/projects/spring-cloud
- Resilience4j Documentation: https://resilience4j.readme.io/
- Eureka Documentation: https://github.com/Netflix/eureka
- Zipkin Documentation: https://zipkin.io/

Good luck with your tests! 🚀

