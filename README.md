# Distributed Payment Transaction Simulator

A high-throughput distributed payment processing system simulation using Python, Kafka, PostgreSQL, Docker, and Kubernetes.

## Architecture Overview

The system consists of the following components:

- **Transaction Generator**: Simulates payment transaction requests
- **Payment Processor**: Processes transactions asynchronously via Kafka
- **Transaction Store**: PostgreSQL database for transaction history
- **API Service**: RESTful API for transaction status and history

## Tech Stack

- Python 3.9+
- Apache Kafka
- PostgreSQL
- Docker
- Kubernetes
- FastAPI (REST API)

## Project Structure

```
.
├── src/
│   ├── transaction_generator/    # Transaction generation service
│   ├── payment_processor/        # Payment processing service
│   └── api_service/             # REST API service
├── k8s/                         # Kubernetes manifests
├── docker/                      # Docker configurations
├── tests/                       # Test suite
└── docker-compose.yml           # Local development setup
```

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Local development with Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Deploy to Kubernetes:
   ```bash
   kubectl apply -f k8s/
   ```

## Environment Variables

Create a `.env` file with the following variables:

```
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
POSTGRES_HOST=postgres
POSTGRES_DB=transactions
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
```

## API Endpoints

- `POST /api/v1/transactions` - Submit new transaction
- `GET /api/v1/transactions/{transaction_id}` - Get transaction status
- `GET /api/v1/transactions` - List transactions with pagination

## Monitoring

The system includes:
- Prometheus metrics
- Grafana dashboards
- Kafka lag monitoring
- PostgreSQL performance metrics 