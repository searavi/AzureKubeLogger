# Azure Kubernetes Infrastructure Telemetry Worker

A Python-based telemetry simulation service that generates realistic monitoring scenarios for Azure Kubernetes infrastructure and sends comprehensive metrics to New Relic.

## Overview

This service simulates production-grade infrastructure telemetry for:
- Kubernetes cluster operations (pod lifecycle, scheduling, failures)
- PostgreSQL database performance metrics
- Azure Blob Storage operations
- Network latency and connectivity monitoring
- System resource utilization

## Features

- **Real Infrastructure Simulation**: Generates authentic telemetry patterns
- **New Relic Integration**: Full APM and infrastructure monitoring
- **Configurable Monitoring**: Adjustable intervals and simulation parameters
- **Production Ready**: Graceful shutdown, error handling, structured logging
- **Multi-Component Architecture**: Modular simulators for different infrastructure layers

## Architecture

```
├── main.py                    # Service entry point
├── telemetry_worker.py        # Main orchestration worker
├── config.py                  # Configuration management
├── newrelic.ini              # New Relic agent configuration
└── simulators/
    ├── kubernetes_simulator.py   # K8s operations simulation
    ├── database_simulator.py     # PostgreSQL metrics simulation
    ├── storage_simulator.py      # Azure Blob Storage simulation
    ├── network_simulator.py      # Network latency simulation
    └── system_monitor.py         # Real system metrics
```

## Installation

1. Install dependencies:
```bash
pip install newrelic psutil python-dotenv
```

2. Configure environment variables:
```bash
export NEW_RELIC_LICENSE_KEY="your-license-key"
export NEW_RELIC_APP_NAME="Azure-K8s-Telemetry-Worker"
export MONITORING_INTERVAL=30
```

3. Set up PostgreSQL database (optional):
```bash
export DATABASE_URL="postgresql://user:pass@host:port/db"
```

## Usage

Start the telemetry worker:
```bash
python main.py
```

The service will begin generating telemetry data and sending it to New Relic every 30 seconds (configurable).

## Configuration

Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `NEW_RELIC_LICENSE_KEY` | - | New Relic license key (required) |
| `NEW_RELIC_APP_NAME` | Azure-K8s-Telemetry-Worker | Application name in New Relic |
| `MONITORING_INTERVAL` | 30 | Seconds between telemetry cycles |
| `LOG_LEVEL` | INFO | Logging verbosity level |
| `ENABLE_K8S_SIMULATION` | true | Enable Kubernetes metrics |
| `ENABLE_DB_SIMULATION` | true | Enable database metrics |
| `ENABLE_STORAGE_SIMULATION` | true | Enable storage metrics |
| `ENABLE_NETWORK_SIMULATION` | true | Enable network metrics |

## Metrics Generated

### Kubernetes Metrics
- Pod scheduling and failure events
- Resource usage (CPU, memory)
- Cluster health scores
- Service discovery latency

### Database Metrics
- Query performance timing
- Connection pool utilization
- Transaction success rates
- Index and cache hit ratios

### Storage Metrics
- Upload/download operations
- API call performance
- Security access patterns
- Storage tier distribution

### Network Metrics
- Endpoint latency measurements
- Packet loss and throughput
- Load balancer health
- CDN performance

### System Metrics
- Real CPU, memory, disk usage
- Network interface statistics
- Process monitoring
- Application performance

## New Relic Dashboard

The service creates comprehensive dashboards in New Relic showing:
- Infrastructure performance trends
- Application health metrics
- Custom events and alerts
- Operational anomalies

## Deployment

For Kubernetes deployment:
1. Build container image
2. Set environment variables as secrets
3. Deploy as Deployment with appropriate resource limits
4. Configure service mesh integration if needed

## License

This project simulates production infrastructure for monitoring and observability testing.