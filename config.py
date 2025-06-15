"""
Configuration management for the telemetry worker
"""

import os
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class Config:
    """Configuration class for telemetry worker settings"""

    def __init__(self):
        # New Relic configuration
        self.NEW_RELIC_LICENSE_KEY = os.getenv("NEW_RELIC_LICENSE_KEY", "")
        self.NEW_RELIC_APP_NAME = os.getenv(
            "NEW_RELIC_APP_NAME", "Azure-K8s-Telemetry-Worker"
        )
        self.NEW_RELIC_ENABLED = bool(self.NEW_RELIC_LICENSE_KEY)

        # Monitoring configuration
        self.MONITORING_INTERVAL = int(
            os.getenv("MONITORING_INTERVAL", "30")
        )  # seconds
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

        # Simulation parameters
        self.ENABLE_K8S_SIMULATION = (
            os.getenv("ENABLE_K8S_SIMULATION", "true").lower() == "true"
        )
        self.ENABLE_DB_SIMULATION = (
            os.getenv("ENABLE_DB_SIMULATION", "true").lower() == "true"
        )
        self.ENABLE_STORAGE_SIMULATION = (
            os.getenv("ENABLE_STORAGE_SIMULATION", "true").lower() == "true"
        )
        self.ENABLE_NETWORK_SIMULATION = (
            os.getenv("ENABLE_NETWORK_SIMULATION", "true").lower() == "true"
        )
        self.ENABLE_SYSTEM_MONITORING = (
            os.getenv("ENABLE_SYSTEM_MONITORING", "true").lower() == "true"
        )

        # Simulation variance settings
        self.ERROR_RATE_VARIANCE = float(
            os.getenv("ERROR_RATE_VARIANCE", "0.05")
        )  # 5% variance
        self.PERFORMANCE_VARIANCE = float(
            os.getenv("PERFORMANCE_VARIANCE", "0.2")
        )  # 20% variance

        # Database configuration (for simulation context)
        self.PGHOST = os.getenv("PGHOST", "localhost")
        self.PGDATABASE = os.getenv("PGDATABASE", "telemetry_db")
        self.PGUSER = os.getenv("PGUSER", "telemetry_user")
        self.PGPORT = os.getenv("PGPORT", "5432")

        # Azure configuration
        self.AZURE_SUBSCRIPTION_ID = os.getenv(
            "AZURE_SUBSCRIPTION_ID", "simulated-subscription"
        )
        self.AZURE_RESOURCE_GROUP = os.getenv(
            "AZURE_RESOURCE_GROUP", "k8s-telemetry-rg"
        )
        self.AZURE_CLUSTER_NAME = os.getenv("AZURE_CLUSTER_NAME", "telemetry-cluster")

        # Worker configuration
        self.WORKER_ID = os.getenv("WORKER_ID", f"worker-{os.getpid()}")
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

        logger.info("Configuration initialized")

    def validate(self):
        """Validate configuration settings"""
        errors = []

        # Validate monitoring interval
        if self.MONITORING_INTERVAL < 1:
            errors.append("MONITORING_INTERVAL must be at least 1 second")

        # Validate variance settings
        if not 0 <= self.ERROR_RATE_VARIANCE <= 1:
            errors.append("ERROR_RATE_VARIANCE must be between 0 and 1")

        if not 0 <= self.PERFORMANCE_VARIANCE <= 1:
            errors.append("PERFORMANCE_VARIANCE must be between 0 and 1")

        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.LOG_LEVEL not in valid_log_levels:
            errors.append(f"LOG_LEVEL must be one of: {', '.join(valid_log_levels)}")

        # New Relic warnings
        if not self.NEW_RELIC_ENABLED:
            logger.warning("New Relic integration disabled - no license key provided")

        if errors:
            for error in errors:
                logger.error(f"Configuration error: {error}")
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")

        logger.info("Configuration validation successful")

    def get_simulation_config(self) -> Dict[str, Any]:
        """Get simulation-specific configuration"""
        return {
            "k8s_enabled": self.ENABLE_K8S_SIMULATION,
            "db_enabled": self.ENABLE_DB_SIMULATION,
            "storage_enabled": self.ENABLE_STORAGE_SIMULATION,
            "network_enabled": self.ENABLE_NETWORK_SIMULATION,
            "system_enabled": self.ENABLE_SYSTEM_MONITORING,
            "error_variance": self.ERROR_RATE_VARIANCE,
            "performance_variance": self.PERFORMANCE_VARIANCE,
        }

    def get_newrelic_config(self) -> Dict[str, str]:
        """Get New Relic configuration"""
        return {
            "license_key": self.NEW_RELIC_LICENSE_KEY,
            "app_name": self.NEW_RELIC_APP_NAME,
            "enabled": str(self.NEW_RELIC_ENABLED).lower(),
        }

    def __str__(self):
        """String representation of configuration (excluding sensitive data)"""
        return f"""
Telemetry Worker Configuration:
- App Name: {self.NEW_RELIC_APP_NAME}
- Environment: {self.ENVIRONMENT}
- Worker ID: {self.WORKER_ID}
- Monitoring Interval: {self.MONITORING_INTERVAL}s
- Log Level: {self.LOG_LEVEL}
- New Relic Enabled: {self.NEW_RELIC_ENABLED}
- K8s Simulation: {self.ENABLE_K8S_SIMULATION}
- DB Simulation: {self.ENABLE_DB_SIMULATION}
- Storage Simulation: {self.ENABLE_STORAGE_SIMULATION}
- Network Simulation: {self.ENABLE_NETWORK_SIMULATION}
- System Monitoring: {self.ENABLE_SYSTEM_MONITORING}
"""
