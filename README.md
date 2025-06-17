# Scalable Backend System for E-Commerce

A microservices-based, event-driven payment processing system built with FastAPI, Kafka, and PostgreSQL. This system is designed to handle high-volume transaction processing with scalability, reliability, and real-time processing capabilities.

## 🏗️ Architecture Overview

The system consists of three main microservices:

- **API Service**: RESTful API for transaction management
- **Payment Processor**: Asynchronous transaction processing service
- **Transaction Generator**: Load testing and demo transaction generator

### Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Message Queue**: Apache Kafka
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (optional)
- **Database Migration**: Alembic

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git

### Running with Docker Compose

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Scalable-Backend-System-for-E-Commerce
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Verify services are running**
   ```bash
   docker-compose ps
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - API Base URL: http://localhost:8000/api/v1

### Running Locally (Development)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   export POSTGRES_HOST=localhost
   export POSTGRES_DB=transactions
   export POSTGRES_USER=admin
   export POSTGRES_PASSWORD=secret
   export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
   ```

3. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start services individually**
   ```bash
   # Terminal 1: Start API service
   python -m uvicorn src.api_service.main:app --host 0.0.0.0 --port 8000 --reload

   # Terminal 2: Start payment processor
   python src/payment_processor/main.py

   # Terminal 3: Start transaction generator
   python src/transaction_generator/main.py
   ```

## 📊 System Components

### 1. API Service (`src/api_service/main.py`)

**Purpose**: Provides RESTful API endpoints for transaction management

**Features**:
- Create new transactions
- Retrieve transaction status
- List transactions with pagination
- Async database operations
- Kafka message publishing

**Endpoints**:
- `POST /api/v1/transactions` - Create a new transaction
- `GET /api/v1/transactions/{transaction_id}` - Get transaction details
- `GET /api/v1/transactions` - List transactions (with pagination)

### 2. Payment Processor (`src/payment_processor/main.py`)

**Purpose**: Processes transactions asynchronously from Kafka queue

**Features**:
- Kafka consumer for transaction processing
- Simulated payment processing with configurable success rate
- Database status updates
- Error handling and logging
- Async processing with artificial delays

### 3. Transaction Generator (`src/transaction_generator/main.py`)

**Purpose**: Generates test transactions for load testing and demonstration

**Features**:
- Random transaction generation
- Configurable generation intervals
- HTTP client for API communication
- Continuous operation with error handling

## 🗄️ Database Schema

### Transaction Model

```python
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True, nullable=False)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(SQLAEnum(TransactionStatus), default=TransactionStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error_message = Column(String, nullable=True)
```

### Transaction Statuses

- `PENDING`: Transaction created, waiting for processing
- `PROCESSING`: Transaction is being processed
- `COMPLETED`: Transaction processed successfully
- `FAILED`: Transaction processing failed

## 🔄 Message Flow

1. **Transaction Creation**: Client sends POST request to API service
2. **Database Storage**: Transaction is stored in PostgreSQL with PENDING status
3. **Kafka Publishing**: API service publishes transaction to Kafka topic
4. **Processing**: Payment processor consumes message and processes transaction
5. **Status Update**: Payment processor updates transaction status in database
6. **Response**: Client can query transaction status via API

## 📝 API Documentation

### Create Transaction

```bash
curl -X POST "http://localhost:8000/api/v1/transactions" \
     -H "Content-Type: application/json" \
     -d '{
       "sender": "user123",
       "receiver": "user456",
       "amount": 100.00,
       "currency": "USD"
     }'
```

**Response**:
```json
{
  "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
  "sender": "user123",
  "receiver": "user456",
  "amount": 100.0,
  "currency": "USD",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "error_message": null
}
```

### Get Transaction

```bash
curl "http://localhost:8000/api/v1/transactions/{transaction_id}"
```

### List Transactions

```bash
curl "http://localhost:8000/api/v1/transactions?skip=0&limit=10"
```

## 🐳 Docker Configuration

### Services

- **Zookeeper**: Kafka coordination service
- **Kafka**: Message broker for event streaming
- **PostgreSQL**: Primary database
- **API Service**: REST API container
- **Payment Processor**: Transaction processing container
- **Transaction Generator**: Load testing container

### Environment Variables

All services use environment variables for configuration:

- `POSTGRES_HOST`: PostgreSQL host address
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses

## ☸️ Kubernetes Deployment

Kubernetes manifests are provided in the `k8s/` directory:

- `00-namespace.yaml`: Creates dedicated namespace
- `01-api-service.yaml`: API service deployment
- `02-payment-processor.yaml`: Payment processor deployment
- `03-transaction-generator.yaml`: Transaction generator deployment

### Deploy to Kubernetes

```bash
kubectl apply -f k8s/
```

## 🔧 Configuration

### Transaction Generator Settings

Modify `src/transaction_generator/main.py` for different load patterns:

```python
MIN_AMOUNT = 10.0          # Minimum transaction amount
MAX_AMOUNT = 1000.0        # Maximum transaction amount
CURRENCIES = ["USD", "EUR", "GBP", "JPY"]  # Supported currencies
TRANSACTION_INTERVAL = 1.0  # Seconds between transactions
```

### Payment Processor Settings

Modify `src/payment_processor/main.py` for processing behavior:

```python
# Success rate (90% success, 10% failure)
success = random.random() < 0.9

# Processing delay (2 seconds)
await asyncio.sleep(2)
```

## 📈 Monitoring and Observability

### Health Checks

All services include health check endpoints and Docker health checks for monitoring.

### Logging

Services use structured logging with different log levels:
- INFO: Normal operation
- ERROR: Error conditions
- DEBUG: Detailed debugging information

### Metrics

The system is prepared for Prometheus metrics integration with the `prometheus-client` package.

## 🧪 Testing

### Running Tests

```bash
pytest
```

### Load Testing

The transaction generator can be used for load testing:

```bash
# Increase transaction frequency
export TRANSACTION_INTERVAL=0.1
```

## 🔒 Security Considerations

- Database credentials should be managed via secrets in production
- API authentication and authorization should be implemented
- Network security between services should be configured
- Input validation is implemented using Pydantic models

## 🚀 Production Deployment

### Recommendations

1. **Database**: Use managed PostgreSQL service
2. **Kafka**: Use managed Kafka service (AWS MSK, Confluent Cloud)
3. **Monitoring**: Implement comprehensive monitoring and alerting
4. **Security**: Add authentication, authorization, and encryption
5. **Scaling**: Use Kubernetes for auto-scaling
6. **Backup**: Implement database backup and recovery procedures

### Environment Variables for Production

```bash
# Database
POSTGRES_HOST=your-production-db-host
POSTGRES_DB=transactions
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-secure-password

# Kafka
KAFKA_BOOTSTRAP_SERVERS=your-kafka-brokers

# Security
JWT_SECRET_KEY=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include logs and error messages

---

**Note**: This is a demonstration system. For production use, implement proper security, monitoring, and error handling according to your specific requirements. 