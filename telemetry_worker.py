"""
Main telemetry worker that orchestrates all simulation components
"""

import time
import threading
import logging
import json
import random
from datetime import datetime
from typing import Dict, Any

# Import New Relic components
try:
    import newrelic.agent
    from newrelic.api.application import application_instance
    from newrelic.api.transaction import current_transaction
except ImportError:
    logging.warning("New Relic agent not available. Install with: pip install newrelic")
    newrelic = None

from simulators.kubernetes_simulator import KubernetesSimulator
from simulators.database_simulator import DatabaseSimulator
from simulators.storage_simulator import StorageSimulator
from simulators.network_simulator import NetworkSimulator
from simulators.system_monitor import SystemMonitor

logger = logging.getLogger(__name__)


class TelemetryWorker:
    """Main worker class that coordinates all telemetry simulation"""

    def __init__(self, config):
        self.config = config
        self.running = False

        # Initialize New Relic if available
        if newrelic and config.NEW_RELIC_ENABLED:
            newrelic.agent.initialize("newrelic.ini")
            self.app = application_instance()
            logger.info("New Relic agent initialized")
        else:
            self.app = None
            logger.warning("New Relic agent not initialized")

        # Initialize simulators
        self.k8s_simulator = KubernetesSimulator(config)
        self.db_simulator = DatabaseSimulator(config)
        self.storage_simulator = StorageSimulator(config)
        self.network_simulator = NetworkSimulator(config)
        self.system_monitor = SystemMonitor(config)

        logger.info("All simulators initialized successfully")

    def send_metric_to_newrelic(
        self,
        metric_name: str,
        value: float,
        metric_type: str = "gauge",
        unit: str = None,
    ):
        """Send custom metric to New Relic"""
        if not self.app:
            return

        try:
            # Send custom metric
            newrelic.agent.record_custom_metric(metric_name, value)

            # Log the metric for debugging
            logger.debug(f"Sent metric to New Relic: {metric_name} = {value}")

        except Exception as e:
            logger.error(f"Failed to send metric to New Relic: {e}")

    def send_event_to_newrelic(self, event_type: str, attributes: Dict[str, Any]):
        """Send custom event to New Relic"""
        if not self.app:
            return

        try:
            newrelic.agent.record_custom_event(event_type, attributes)
            logger.debug(f"Sent event to New Relic: {event_type}")

        except Exception as e:
            logger.error(f"Failed to send event to New Relic: {e}")

    def log_structured_event(self, event_type: str, data: Dict[str, Any]):
        """Log structured JSON event"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "service": "azure-k8s-telemetry-worker",
            "data": data,
        }

        logger.info(json.dumps(log_entry))

    def run_simulation_cycle(self):
        """Run one complete simulation cycle"""
        cycle_start = time.time()

        try:
            # 1. Kubernetes operations simulation
            k8s_metrics = self.k8s_simulator.simulate_operations()
            for metric_name, value in k8s_metrics.items():
                self.send_metric_to_newrelic(f"k8s.{metric_name}", value)

            # 2. Database operations simulation
            db_metrics = self.db_simulator.simulate_operations()
            for metric_name, value in db_metrics.items():
                self.send_metric_to_newrelic(f"database.{metric_name}", value)

            # 3. Storage operations simulation
            storage_metrics = self.storage_simulator.simulate_operations()
            for metric_name, value in storage_metrics.items():
                self.send_metric_to_newrelic(f"storage.{metric_name}", value)

            # 4. Network simulation
            network_metrics = self.network_simulator.simulate_operations()
            for metric_name, value in network_metrics.items():
                self.send_metric_to_newrelic(f"network.{metric_name}", value)

            # 5. System monitoring
            system_metrics = self.system_monitor.get_metrics()
            for metric_name, value in system_metrics.items():
                self.send_metric_to_newrelic(f"system.{metric_name}", value)

            # Combine all metrics for structured logging
            all_metrics = {
                "kubernetes": k8s_metrics,
                "database": db_metrics,
                "storage": storage_metrics,
                "network": network_metrics,
                "system": system_metrics,
            }

            self.log_structured_event("telemetry_cycle", all_metrics)

            # Send aggregated cycle event to New Relic
            cycle_duration = time.time() - cycle_start
            self.send_event_to_newrelic(
                "TelemetryCycle",
                {
                    "duration_ms": cycle_duration * 1000,
                    "metrics_collected": sum(len(m) for m in all_metrics.values()),
                },
            )

            logger.info(f"Simulation cycle completed in {cycle_duration:.2f}s")

        except Exception as e:
            logger.error(f"Error in simulation cycle: {e}", exc_info=True)
            self.send_event_to_newrelic(
                "TelemetryError",
                {"error_type": type(e).__name__, "error_message": str(e)},
            )

    def run(self):
        """Main run loop for the telemetry worker"""
        self.running = True
        logger.info("Telemetry worker started")

        cycle_count = 0

        while self.running:
            try:
                cycle_count += 1
                logger.debug(f"Starting simulation cycle #{cycle_count}")

                self.run_simulation_cycle()

                # Random jitter to simulate realistic variance
                base_interval = self.config.MONITORING_INTERVAL
                jitter = random.uniform(-0.1, 0.1) * base_interval
                sleep_time = max(1, base_interval + jitter)

                time.sleep(sleep_time)

            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
                break
            except Exception as e:
                logger.error(f"Unexpected error in worker loop: {e}", exc_info=True)
                time.sleep(5)  # Wait before retrying

        logger.info("Telemetry worker stopped")

    def stop(self):
        """Stop the telemetry worker"""
        self.running = False
        logger.info("Telemetry worker stop requested")
