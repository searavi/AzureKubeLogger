"""
Network operations and latency simulator
Simulates network conditions, latency spikes, and connectivity issues
"""

import random
import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class NetworkSimulator:
    """Simulates network operations and performance metrics"""

    def __init__(self, config):
        self.config = config
        self.baseline_latency = 15  # ms
        self.endpoints = [
            "api.service.local",
            "database.internal",
            "cache.redis.local",
            "storage.blob.azure.com",
            "monitoring.newrelic.com",
        ]
        self.regions = ["eastus", "westus", "northeurope", "southeastasia"]

        logger.info("Network simulator initialized")

    def simulate_latency_metrics(self) -> Dict[str, float]:
        """Simulate network latency measurements"""
        metrics = {}

        total_measurements = 0
        total_latency = 0
        high_latency_count = 0

        for endpoint in self.endpoints:
            measurements = random.randint(10, 30)
            endpoint_latencies = []

            for _ in range(measurements):
                # Base latency with normal variation
                latency = self.baseline_latency + random.normalvariate(0, 5)

                # Simulate occasional latency spikes
                if random.random() < 0.05:  # 5% chance of spike
                    spike_factor = random.uniform(3, 10)
                    latency *= spike_factor
                    high_latency_count += 1
                    logger.warning(
                        f"High latency detected for {endpoint}: {latency:.1f}ms"
                    )

                latency = max(1, latency)  # Ensure positive latency
                endpoint_latencies.append(latency)
                total_latency += latency
                total_measurements += 1

            # Per-endpoint metrics
            avg_latency = sum(endpoint_latencies) / len(endpoint_latencies)
            max_latency = max(endpoint_latencies)
            min_latency = min(endpoint_latencies)

            endpoint_clean = endpoint.replace(".", "_").replace("-", "_")
            metrics[f"{endpoint_clean}_avg_latency_ms"] = avg_latency
            metrics[f"{endpoint_clean}_max_latency_ms"] = max_latency
            metrics[f"{endpoint_clean}_min_latency_ms"] = min_latency

        # Overall latency metrics
        metrics["overall_avg_latency_ms"] = total_latency / total_measurements
        metrics["high_latency_events"] = high_latency_count
        metrics["latency_spike_rate"] = (high_latency_count / total_measurements) * 100

        return metrics

    def simulate_throughput_metrics(self) -> Dict[str, float]:
        """Simulate network throughput measurements"""
        metrics = {}

        # Simulate bandwidth utilization
        baseline_bandwidth_mbps = 1000  # 1 Gbps baseline
        current_utilization = random.uniform(20, 80)  # 20-80% utilization

        metrics["bandwidth_utilization_percent"] = current_utilization
        metrics["available_bandwidth_mbps"] = (
            baseline_bandwidth_mbps * (100 - current_utilization) / 100
        )

        # Simulate data transfer rates
        ingress_mbps = random.uniform(50, 300)
        egress_mbps = random.uniform(100, 500)

        metrics["ingress_traffic_mbps"] = ingress_mbps
        metrics["egress_traffic_mbps"] = egress_mbps
        metrics["total_traffic_mbps"] = ingress_mbps + egress_mbps

        # Packet metrics
        packets_sent = random.randint(10000, 100000)
        packet_loss_rate = random.uniform(0.001, 0.1)  # 0.001% to 0.1%
        packets_lost = int(packets_sent * packet_loss_rate / 100)

        metrics["packets_sent"] = packets_sent
        metrics["packets_lost"] = packets_lost
        metrics["packet_loss_rate"] = packet_loss_rate

        if packet_loss_rate > 0.05:
            logger.warning(f"High packet loss rate: {packet_loss_rate:.3f}%")

        return metrics

    def simulate_connectivity_issues(self) -> Dict[str, float]:
        """Simulate network connectivity problems"""
        metrics = {}

        # Connection timeouts
        timeout_events = 0
        dns_failures = 0
        connection_refused = 0

        # Simulate various connection issues
        if random.random() < 0.02:  # 2% chance of timeout
            timeout_events = random.randint(1, 3)
            logger.warning(f"Network timeout events: {timeout_events}")

        if random.random() < 0.01:  # 1% chance of DNS issues
            dns_failures = random.randint(1, 2)
            logger.warning(f"DNS resolution failures: {dns_failures}")

        if random.random() < 0.015:  # 1.5% chance of connection refused
            connection_refused = random.randint(1, 2)
            logger.warning(f"Connection refused events: {connection_refused}")

        metrics["timeout_events"] = timeout_events
        metrics["dns_failures"] = dns_failures
        metrics["connection_refused"] = connection_refused
        metrics["total_connection_errors"] = (
            timeout_events + dns_failures + connection_refused
        )

        # SSL/TLS metrics
        ssl_handshake_time = random.uniform(50, 200)  # ms
        ssl_errors = random.randint(0, 1) if random.random() < 0.005 else 0

        metrics["ssl_handshake_time_ms"] = ssl_handshake_time
        metrics["ssl_errors"] = ssl_errors

        return metrics

    def simulate_load_balancer_metrics(self) -> Dict[str, float]:
        """Simulate load balancer performance"""
        metrics = {}

        # Backend server status
        total_backends = random.randint(3, 8)
        healthy_backends = total_backends - random.randint(0, 1)

        metrics["total_backend_servers"] = total_backends
        metrics["healthy_backend_servers"] = healthy_backends
        metrics["backend_health_percentage"] = (healthy_backends / total_backends) * 100

        # Request distribution
        requests_per_backend = []
        for _ in range(healthy_backends):
            requests = random.randint(50, 200)
            requests_per_backend.append(requests)

        if requests_per_backend:
            metrics["total_requests"] = sum(requests_per_backend)
            metrics["avg_requests_per_backend"] = sum(requests_per_backend) / len(
                requests_per_backend
            )
            metrics["load_balance_variance"] = max(requests_per_backend) - min(
                requests_per_backend
            )
        else:
            metrics["total_requests"] = 0
            metrics["avg_requests_per_backend"] = 0
            metrics["load_balance_variance"] = 0

        # Response time metrics
        metrics["load_balancer_response_time_ms"] = random.uniform(1, 10)

        return metrics

    def simulate_cdn_metrics(self) -> Dict[str, float]:
        """Simulate CDN performance metrics"""
        metrics = {}

        # Cache performance
        total_requests = random.randint(1000, 5000)
        cache_hits = int(total_requests * random.uniform(0.70, 0.85))  # 70-85% hit rate
        cache_misses = total_requests - cache_hits

        metrics["cdn_total_requests"] = total_requests
        metrics["cdn_cache_hits"] = cache_hits
        metrics["cdn_cache_misses"] = cache_misses
        metrics["cdn_hit_rate"] = (cache_hits / total_requests) * 100

        # Response times
        metrics["cdn_cache_hit_time_ms"] = random.uniform(5, 20)
        metrics["cdn_cache_miss_time_ms"] = random.uniform(50, 200)

        # Bandwidth savings
        origin_bandwidth_gb = random.uniform(10, 50)
        cdn_bandwidth_gb = origin_bandwidth_gb * (cache_misses / total_requests)
        bandwidth_saved_gb = origin_bandwidth_gb - cdn_bandwidth_gb

        metrics["origin_bandwidth_gb"] = origin_bandwidth_gb
        metrics["cdn_bandwidth_gb"] = cdn_bandwidth_gb
        metrics["bandwidth_saved_gb"] = bandwidth_saved_gb
        metrics["bandwidth_savings_percent"] = (
            bandwidth_saved_gb / origin_bandwidth_gb
        ) * 100

        return metrics

    def simulate_operations(self) -> Dict[str, float]:
        """Run all network simulations and return combined metrics"""
        all_metrics = {}

        # Run all simulation components
        latency_metrics = self.simulate_latency_metrics()
        throughput_metrics = self.simulate_throughput_metrics()
        connectivity_metrics = self.simulate_connectivity_issues()
        lb_metrics = self.simulate_load_balancer_metrics()
        cdn_metrics = self.simulate_cdn_metrics()

        # Combine all metrics
        all_metrics.update(latency_metrics)
        all_metrics.update(throughput_metrics)
        all_metrics.update(connectivity_metrics)
        all_metrics.update(lb_metrics)
        all_metrics.update(cdn_metrics)

        # Calculate overall network health score
        latency_score = max(0, 100 - (all_metrics.get("overall_avg_latency_ms", 0) / 2))
        packet_loss_score = max(
            0, 100 - (all_metrics.get("packet_loss_rate", 0) * 1000)
        )
        connectivity_score = max(
            0, 100 - (all_metrics.get("total_connection_errors", 0) * 20)
        )

        network_health = (latency_score + packet_loss_score + connectivity_score) / 3
        all_metrics["network_health_score"] = network_health

        return all_metrics
