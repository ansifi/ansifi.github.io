# Microservices Architecture Fundamentals

## 📚 Learning Objectives

By the end of this tutorial, you will:
- Understand microservices architecture principles
- Learn service decomposition strategies
- Master inter-service communication patterns
- Implement service discovery and API gateways
- Handle distributed data management
- Implement resilience patterns (circuit breakers, retries)
- Understand deployment and monitoring strategies

---

## 🎯 What are Microservices?

Microservices architecture is an approach where:
- **Single Responsibility**: Each service handles one business capability
- **Independent Deployment**: Services can be deployed independently
- **Technology Diversity**: Each service can use different technologies
- **Decentralized Data**: Each service manages its own database
- **Fault Isolation**: Failure in one service doesn't crash the entire system

---

## 1. Monolith vs Microservices

### Monolithic Architecture

```
┌─────────────────────────────────┐
│      Monolithic Application     │
│  ┌──────┐ ┌──────┐ ┌──────┐    │
│  │ User │ │Order │ │Payment│   │
│  │Service│ │Service│ │Service│  │
│  └──────┘ └──────┘ └──────┘    │
│         Shared Database         │
└─────────────────────────────────┘
```

**Pros:**
- Simple to develop and deploy
- Easy to test
- Performance (no network calls)

**Cons:**
- Tight coupling
- Difficult to scale
- Technology lock-in
- Single point of failure

### Microservices Architecture

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│   User   │  │  Order   │  │ Payment  │
│ Service  │  │ Service  │  │ Service  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
│   User   │  │  Order   │  │ Payment  │
│  Database │  │ Database  │  │ Database │
└──────────┘  └──────────┘  └──────────┘
```

**Pros:**
- Independent scaling
- Technology diversity
- Fault isolation
- Team autonomy

**Cons:**
- Increased complexity
- Network latency
- Data consistency challenges
- Operational overhead

---

## 2. Service Decomposition Strategies

### Domain-Driven Design (DDD)

```java
// User Service - Bounded Context: User Management
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody UserDTO userDTO) {
        User user = userService.createUser(userDTO);
        return ResponseEntity.ok(user);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUser(id));
    }
}

// Order Service - Bounded Context: Order Management
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @Autowired
    private OrderService orderService;
    
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody OrderDTO orderDTO) {
        Order order = orderService.createOrder(orderDTO);
        return ResponseEntity.ok(order);
    }
}
```

### Decomposition by Business Capability

```
E-Commerce Application:
├── User Service (Authentication, Profiles)
├── Product Service (Catalog, Inventory)
├── Order Service (Order Management)
├── Payment Service (Payment Processing)
├── Shipping Service (Shipping, Tracking)
└── Notification Service (Emails, SMS)
```

### Decomposition by Data

```java
// Each service owns its data
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String email;
    private String name;
    
    // No direct reference to Order entity
    // Use userId for relationships
}
```

---

## 3. Inter-Service Communication

### Synchronous Communication: REST

```java
// Order Service calling User Service
@Service
public class OrderService {
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Value("${user.service.url}")
    private String userServiceUrl;
    
    public Order createOrder(OrderDTO orderDTO) {
        // Call User Service to validate user
        ResponseEntity<User> response = restTemplate.getForEntity(
            userServiceUrl + "/api/users/" + orderDTO.getUserId(),
            User.class
        );
        
        User user = response.getBody();
        if (user == null) {
            throw new UserNotFoundException();
        }
        
        // Create order
        Order order = new Order();
        order.setUserId(user.getId());
        // ... set other fields
        
        return orderRepository.save(order);
    }
}
```

### Synchronous Communication: Feign Client

```java
// Feign Client for User Service
@FeignClient(name = "user-service", url = "${user.service.url}")
public interface UserServiceClient {
    
    @GetMapping("/api/users/{id}")
    User getUser(@PathVariable Long id);
    
    @PostMapping("/api/users")
    User createUser(@RequestBody UserDTO userDTO);
}

// Usage in Order Service
@Service
public class OrderService {
    
    @Autowired
    private UserServiceClient userServiceClient;
    
    public Order createOrder(OrderDTO orderDTO) {
        User user = userServiceClient.getUser(orderDTO.getUserId());
        // ... create order
    }
}
```

### Asynchronous Communication: Message Queue

```java
// Order Service - Publisher
@Service
public class OrderService {
    
    @Autowired
    private RabbitTemplate rabbitTemplate;
    
    public Order createOrder(OrderDTO orderDTO) {
        Order order = orderRepository.save(order);
        
        // Publish order created event
        OrderCreatedEvent event = new OrderCreatedEvent(
            order.getId(),
            order.getUserId(),
            order.getTotalAmount()
        );
        
        rabbitTemplate.convertAndSend("order.exchange", "order.created", event);
        
        return order;
    }
}

// Payment Service - Consumer
@Component
public class OrderEventListener {
    
    @RabbitListener(queues = "order.created.queue")
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Process payment for order
        paymentService.processPayment(event.getOrderId(), event.getAmount());
    }
}
```

---

## 4. Service Discovery

### Eureka Server

```java
// Eureka Server
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}

// application.yml
server:
  port: 8761

eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
```

### Eureka Client

```java
// User Service - Eureka Client
@SpringBootApplication
@EnableEurekaClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

// application.yml
spring:
  application:
    name: user-service

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
```

### Service Discovery with Feign

```java
// Order Service using Feign with Eureka
@FeignClient(name = "user-service")  // Service name from Eureka
public interface UserServiceClient {
    
    @GetMapping("/api/users/{id}")
    User getUser(@PathVariable Long id);
}
```

---

## 5. API Gateway

### Spring Cloud Gateway

```java
@SpringBootApplication
public class ApiGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}

// application.yml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service  # Load balanced via Eureka
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
        
        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
```

### Gateway Filters

```java
@Component
public class AuthenticationFilter implements GatewayFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        
        String authHeader = request.getHeaders().getFirst("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }
        
        // Validate token
        String token = authHeader.substring(7);
        if (!isValidToken(token)) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }
        
        return chain.filter(exchange);
    }
}
```

---

## 6. Distributed Data Management

### Database per Service Pattern

```java
// User Service - Own Database
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String email;
    private String name;
}

// Order Service - Own Database
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long userId;  // Reference, not foreign key
    private BigDecimal totalAmount;
}
```

### Saga Pattern for Distributed Transactions

```java
// Order Saga Orchestrator
@Service
public class OrderSagaOrchestrator {
    
    @Autowired
    private OrderService orderService;
    
    @Autowired
    private PaymentService paymentService;
    
    @Autowired
    private InventoryService inventoryService;
    
    @Transactional
    public Order createOrder(OrderDTO orderDTO) {
        // Step 1: Create order
        Order order = orderService.createOrder(orderDTO);
        
        try {
            // Step 2: Reserve inventory
            inventoryService.reserveInventory(orderDTO.getItems());
            
            // Step 3: Process payment
            paymentService.processPayment(order.getId(), order.getTotalAmount());
            
            // Step 4: Confirm order
            orderService.confirmOrder(order.getId());
            
        } catch (Exception e) {
            // Compensating transactions
            orderService.cancelOrder(order.getId());
            inventoryService.releaseInventory(orderDTO.getItems());
            throw e;
        }
        
        return order;
    }
}
```

---

## 7. Resilience Patterns

### Circuit Breaker with Resilience4j

```java
// Order Service with Circuit Breaker
@Service
public class OrderService {
    
    @Autowired
    private UserServiceClient userServiceClient;
    
    @CircuitBreaker(name = "userService", fallbackMethod = "getUserFallback")
    public User getUser(Long userId) {
        return userServiceClient.getUser(userId);
    }
    
    public User getUserFallback(Long userId, Exception e) {
        // Fallback: Return cached user or default user
        return new User(userId, "Unknown User", "unknown@example.com");
    }
}

// Configuration
resilience4j:
  circuitbreaker:
    instances:
      userService:
        registerHealthIndicator: true
        slidingWindowSize: 10
        minimumNumberOfCalls: 5
        permittedNumberOfCallsInHalfOpenState: 3
        automaticTransitionFromOpenToHalfOpenEnabled: true
        waitDurationInOpenState: 5s
        failureRateThreshold: 50
```

### Retry Pattern

```java
@Retry(name = "userService")
@CircuitBreaker(name = "userService")
public User getUser(Long userId) {
    return userServiceClient.getUser(userId);
}

// Configuration
resilience4j:
  retry:
    instances:
      userService:
        maxAttempts: 3
        waitDuration: 1s
        retryExceptions:
          - java.net.ConnectException
          - java.net.SocketTimeoutException
```

### Bulkhead Pattern

```java
@Bulkhead(name = "userService", type = Bulkhead.Type.THREADPOOL)
public CompletableFuture<User> getUserAsync(Long userId) {
    return CompletableFuture.supplyAsync(() -> 
        userServiceClient.getUser(userId)
    );
}
```

---

## 8. Configuration Management

### Spring Cloud Config Server

```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}

// application.yml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/your-org/config-repo
```

### Config Client

```java
@SpringBootApplication
@EnableConfigServer
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

// bootstrap.yml
spring:
  application:
    name: user-service
  cloud:
    config:
      uri: http://localhost:8888
```

---

## 9. Practice Exercises

### Exercise 1: Create Microservice

Create a Product Service with:
- REST endpoints for CRUD operations
- Own database
- Eureka client registration

### Exercise 2: Implement Service Communication

Implement communication between Order Service and Product Service:
- Use Feign client
- Add circuit breaker
- Implement retry logic

### Exercise 3: Create API Gateway

Create an API Gateway that:
- Routes requests to multiple services
- Implements authentication filter
- Adds rate limiting

---

## 🎯 Key Takeaways

1. ✅ Decompose by business capability or domain
2. ✅ Each service owns its database
3. ✅ Use synchronous (REST) or asynchronous (MQ) communication
4. ✅ Implement service discovery (Eureka)
5. ✅ Use API Gateway for routing and cross-cutting concerns
6. ✅ Implement resilience patterns (circuit breaker, retry)
7. ✅ Handle distributed transactions with Saga pattern

---

## 📚 Next Steps

Next: **Spring Boot Microservices Implementation** - Deep dive into Spring Boot microservices with practical examples.

