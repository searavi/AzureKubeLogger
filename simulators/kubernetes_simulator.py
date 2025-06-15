"""
Kubernetes operations simulator
Simulates pod lifecycle, scheduling, crashes, and other K8s events
"""

import random
import time
import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class KubernetesSimulator:
    """Simulates Kubernetes cluster operations and events"""

    def __init__(self, config):
        self.config = config
        self.pod_states = {}
        self.namespace_stats = {
            "default": {"pods": 0, "services": 5},
            "kube-system": {"pods": 0, "services": 12},
            "monitoring": {"pods": 0, "services": 3},
            "ingress": {"pods": 0, "services": 2},
        }

        # Initialize some baseline pods
        self._initialize_baseline_pods()

    def _initialize_baseline_pods(self):
        """Initialize baseline pod configuration"""
        baseline_pods = [
            {"name": "api-server", "namespace": "default", "replicas": 3},
            {"name": "web-frontend", "namespace": "default", "replicas": 5},
            {"name": "worker-service", "namespace": "default", "replicas": 8},
            {"name": "redis-cache", "namespace": "default", "replicas": 2},
            {"name": "prometheus", "namespace": "monitoring", "replicas": 1},
            {"name": "grafana", "namespace": "monitoring", "replicas": 1},
            {"name": "nginx-ingress", "namespace": "ingress", "replicas": 3},
        ]

        for pod_config in baseline_pods:
            for i in range(pod_config["replicas"]):
                pod_name = f"{pod_config['name']}-{i}"
                self.pod_states[pod_name] = {
                    "namespace": pod_config["namespace"],
                    "state": "Running",
                    "restart_count": random.randint(0, 5),
                    "cpu_usage": random.uniform(10, 80),
                    "memory_usage": random.uniform(100, 800),
                    "created_at": datetime.utcnow()
                    - timedelta(days=random.randint(1, 30)),
                }

    def simulate_pod_scheduling(self) -> Dict[str, float]:
        """Simulate pod scheduling operations"""
        metrics = {}

        # Simulate new pod creation
        if random.random() < 0.1:  # 10% chance of new pod
            new_pod_name = f"dynamic-pod-{int(time.time())}"
            scheduling_time = random.uniform(1.5, 8.0)  # 1.5-8 seconds

            self.pod_states[new_pod_name] = {
                "namespace": random.choice(list(self.namespace_stats.keys())),
                "state": "Pending",
                "restart_count": 0,
                "cpu_usage": 0,
                "memory_usage": 0,
                "created_at": datetime.utcnow(),
            }

            logger.info(f"Scheduled new pod: {new_pod_name}")
            metrics["pod_scheduling_time_seconds"] = scheduling_time
            metrics["pods_scheduled_total"] = 1
        else:
            metrics["pods_scheduled_total"] = 0

        return metrics

    def simulate_pod_failures(self) -> Dict[str, float]:
        """Simulate pod crashes and failures"""
        metrics = {}
        failures = 0

        running_pods = [
            name
            for name, state in self.pod_states.items()
            if state["state"] == "Running"
        ]

        # Simulate random pod failures
        for pod_name in running_pods:
            if random.random() < 0.02:  # 2% chance of failure per cycle
                self.pod_states[pod_name]["state"] = "Failed"
                self.pod_states[pod_name]["restart_count"] += 1
                failures += 1

                logger.warning(f"Pod failed: {pod_name}")

                # Simulate restart after failure
                if random.random() < 0.8:  # 80% chance of successful restart
                    self.pod_states[pod_name]["state"] = "Running"
                    logger.info(f"Pod restarted: {pod_name}")

        metrics["pod_failures_total"] = failures
        metrics["pod_restart_rate"] = failures / max(len(running_pods), 1)

        return metrics

    def simulate_resource_usage(self) -> Dict[str, float]:
        """Simulate pod resource usage"""
        metrics = {}

        total_cpu = 0
        total_memory = 0
        pod_count = 0

        for pod_name, pod_state in self.pod_states.items():
            if pod_state["state"] == "Running":
                # Simulate realistic CPU and memory fluctuations
                cpu_change = random.uniform(-5, 15)
                memory_change = random.uniform(-20, 50)

                pod_state["cpu_usage"] = max(
                    5, min(95, pod_state["cpu_usage"] + cpu_change)
                )
                pod_state["memory_usage"] = max(
                    50, min(1000, pod_state["memory_usage"] + memory_change)
                )

                total_cpu += pod_state["cpu_usage"]
                total_memory += pod_state["memory_usage"]
                pod_count += 1

        if pod_count > 0:
            metrics["average_cpu_usage_percent"] = total_cpu / pod_count
            metrics["average_memory_usage_mb"] = total_memory / pod_count
            metrics["total_running_pods"] = pod_count
        else:
            metrics["average_cpu_usage_percent"] = 0
            metrics["average_memory_usage_mb"] = 0
            metrics["total_running_pods"] = 0

        return metrics

    def simulate_networking(self) -> Dict[str, float]:
        """Simulate network-related metrics"""
        metrics = {}

        # Simulate service discovery latency
        metrics["service_discovery_latency_ms"] = random.uniform(5, 50)

        # Simulate DNS resolution time
        metrics["dns_resolution_time_ms"] = random.uniform(1, 15)

        # Simulate ingress controller metrics
        metrics["ingress_request_rate"] = random.uniform(100, 1000)
        metrics["ingress_error_rate"] = random.uniform(0.1, 5.0)

        return metrics

    def simulate_operations(self) -> Dict[str, float]:
        """Run all Kubernetes simulations and return combined metrics"""
        all_metrics = {}

        # Run all simulation components
        scheduling_metrics = self.simulate_pod_scheduling()
        failure_metrics = self.simulate_pod_failures()
        resource_metrics = self.simulate_resource_usage()
        network_metrics = self.simulate_networking()

        # Combine all metrics
        all_metrics.update(scheduling_metrics)
        all_metrics.update(failure_metrics)
        all_metrics.update(resource_metrics)
        all_metrics.update(network_metrics)

        # Add cluster-wide metrics
        all_metrics["cluster_health_score"] = random.uniform(85, 99)
        all_metrics["api_server_latency_ms"] = random.uniform(10, 100)

        return all_metrics
