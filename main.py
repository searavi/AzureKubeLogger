#!/usr/bin/env python3
"""
Azure Kubernetes Infrastructure Telemetry Worker Service
Main entry point for the telemetry simulation service
"""

import os
import sys
import logging
import signal
import threading
import time
from dotenv import load_dotenv
from telemetry_worker import TelemetryWorker
from config import Config

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("telemetry_worker.log"),
    ],
)

logger = logging.getLogger(__name__)


class TelemetryService:
    """Main service class for managing the telemetry worker"""

    def __init__(self):
        self.worker = None
        self.running = False
        self.shutdown_event = threading.Event()

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown()

    def shutdown(self):
        """Gracefully shutdown the service"""
        self.running = False
        self.shutdown_event.set()

        if self.worker:
            logger.info("Stopping telemetry worker...")
            self.worker.stop()

        logger.info("Telemetry service shutdown complete")
        sys.exit(0)

    def start(self):
        """Start the telemetry service"""
        logger.info("Starting Azure Kubernetes Telemetry Worker Service")

        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        try:
            # Initialize configuration
            config = Config()
            config.validate()

            # Initialize and start telemetry worker
            self.worker = TelemetryWorker(config)
            self.running = True

            logger.info("Telemetry worker initialized successfully")
            logger.info(f"Monitoring interval: {config.MONITORING_INTERVAL}s")
            logger.info(f"New Relic enabled: {config.NEW_RELIC_ENABLED}")

            # Start the worker in a separate thread
            worker_thread = threading.Thread(target=self.worker.run, daemon=True)
            worker_thread.start()

            # Keep main thread alive
            while self.running and not self.shutdown_event.is_set():
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.shutdown()
        except Exception as e:
            logger.error(f"Critical error in telemetry service: {e}", exc_info=True)
            self.shutdown()


if __name__ == "__main__":
    service = TelemetryService()
    service.start()
