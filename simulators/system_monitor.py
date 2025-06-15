"""
System resource monitoring
Monitors CPU, memory, disk, and other system metrics using psutil
"""

import psutil
import random
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class SystemMonitor:
    """Monitors system resources and performance metrics"""

    def __init__(self, config):
        self.config = config
        self.process = psutil.Process()
        logger.info("System monitor initialized")

    def get_cpu_metrics(self) -> Dict[str, float]:
        """Get CPU usage and performance metrics"""
        metrics = {}

        try:
            # Overall CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics["cpu_usage_percent"] = cpu_percent

            # Per-core CPU usage
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            metrics["cpu_core_count"] = len(cpu_per_core)
            metrics["cpu_max_core_usage"] = max(cpu_per_core) if cpu_per_core else 0
            metrics["cpu_min_core_usage"] = min(cpu_per_core) if cpu_per_core else 0
            metrics["cpu_avg_core_usage"] = (
                sum(cpu_per_core) / len(cpu_per_core) if cpu_per_core else 0
            )

            # CPU frequency
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                metrics["cpu_frequency_mhz"] = cpu_freq.current
                metrics["cpu_max_frequency_mhz"] = cpu_freq.max

            # Load averages (Linux/Unix)
            try:
                load_avg = psutil.getloadavg()
                metrics["load_avg_1min"] = load_avg[0]
                metrics["load_avg_5min"] = load_avg[1]
                metrics["load_avg_15min"] = load_avg[2]
            except AttributeError:
                # getloadavg not available on Windows
                pass

            # CPU times
            cpu_times = psutil.cpu_times()
            metrics["cpu_time_user"] = cpu_times.user
            metrics["cpu_time_system"] = cpu_times.system
            metrics["cpu_time_idle"] = cpu_times.idle

        except Exception as e:
            logger.error(f"Error getting CPU metrics: {e}")

        return metrics

    def get_memory_metrics(self) -> Dict[str, float]:
        """Get memory usage metrics"""
        metrics = {}

        try:
            # Virtual memory
            vm = psutil.virtual_memory()
            metrics["memory_total_gb"] = vm.total / (1024**3)
            metrics["memory_used_gb"] = vm.used / (1024**3)
            metrics["memory_available_gb"] = vm.available / (1024**3)
            metrics["memory_usage_percent"] = vm.percent
            metrics["memory_free_gb"] = vm.free / (1024**3)

            # Swap memory
            swap = psutil.swap_memory()
            metrics["swap_total_gb"] = swap.total / (1024**3)
            metrics["swap_used_gb"] = swap.used / (1024**3)
            metrics["swap_free_gb"] = swap.free / (1024**3)
            metrics["swap_usage_percent"] = swap.percent

            # Process memory
            process_memory = self.process.memory_info()
            metrics["process_memory_rss_mb"] = process_memory.rss / (1024**2)
            metrics["process_memory_vms_mb"] = process_memory.vms / (1024**2)
            metrics["process_memory_percent"] = self.process.memory_percent()

        except Exception as e:
            logger.error(f"Error getting memory metrics: {e}")

        return metrics

    def get_disk_metrics(self) -> Dict[str, float]:
        """Get disk usage and I/O metrics"""
        metrics = {}

        try:
            # Disk usage for root partition
            disk_usage = psutil.disk_usage("/")
            metrics["disk_total_gb"] = disk_usage.total / (1024**3)
            metrics["disk_used_gb"] = disk_usage.used / (1024**3)
            metrics["disk_free_gb"] = disk_usage.free / (1024**3)
            metrics["disk_usage_percent"] = (disk_usage.used / disk_usage.total) * 100

            # Disk I/O
            disk_io = psutil.disk_io_counters()
            if disk_io:
                metrics["disk_read_bytes"] = disk_io.read_bytes
                metrics["disk_write_bytes"] = disk_io.write_bytes
                metrics["disk_read_count"] = disk_io.read_count
                metrics["disk_write_count"] = disk_io.write_count
                metrics["disk_read_time_ms"] = disk_io.read_time
                metrics["disk_write_time_ms"] = disk_io.write_time

        except Exception as e:
            logger.error(f"Error getting disk metrics: {e}")

        return metrics

    def get_network_interface_metrics(self) -> Dict[str, float]:
        """Get network interface statistics"""
        metrics = {}

        try:
            # Network I/O
            net_io = psutil.net_io_counters()
            if net_io:
                metrics["network_bytes_sent"] = net_io.bytes_sent
                metrics["network_bytes_recv"] = net_io.bytes_recv
                metrics["network_packets_sent"] = net_io.packets_sent
                metrics["network_packets_recv"] = net_io.packets_recv
                metrics["network_errors_in"] = net_io.errin
                metrics["network_errors_out"] = net_io.errout
                metrics["network_drops_in"] = net_io.dropin
                metrics["network_drops_out"] = net_io.dropout

            # Network connections count
            connections = psutil.net_connections()
            connection_states = {}
            for conn in connections:
                state = conn.status
                connection_states[state] = connection_states.get(state, 0) + 1

            metrics["network_connections_total"] = len(connections)
            for state, count in connection_states.items():
                metrics[f"network_connections_{state.lower()}"] = count

        except Exception as e:
            logger.error(f"Error getting network metrics: {e}")

        return metrics

    def get_process_metrics(self) -> Dict[str, float]:
        """Get process-specific metrics"""
        metrics = {}

        try:
            # Process CPU usage
            metrics["process_cpu_percent"] = self.process.cpu_percent()

            # Process threads
            metrics["process_thread_count"] = self.process.num_threads()

            # Process file descriptors (Unix)
            try:
                metrics["process_open_files"] = self.process.num_fds()
            except AttributeError:
                # num_fds not available on Windows
                pass

            # Process status
            metrics["process_status"] = 1 if self.process.is_running() else 0

            # Process create time
            create_time = self.process.create_time()
            metrics["process_uptime_seconds"] = psutil.time.time() - create_time

        except Exception as e:
            logger.error(f"Error getting process metrics: {e}")

        return metrics

    def get_system_info_metrics(self) -> Dict[str, float]:
        """Get general system information metrics"""
        metrics = {}

        try:
            # System uptime
            boot_time = psutil.boot_time()
            uptime_seconds = psutil.time.time() - boot_time
            metrics["system_uptime_seconds"] = uptime_seconds
            metrics["system_uptime_hours"] = uptime_seconds / 3600

            # Number of processes
            metrics["system_process_count"] = len(psutil.pids())

            # System users
            users = psutil.users()
            metrics["system_user_count"] = len(users)

        except Exception as e:
            logger.error(f"Error getting system info metrics: {e}")

        return metrics

    def simulate_application_metrics(self) -> Dict[str, float]:
        """Simulate application-specific metrics"""
        metrics = {}

        # Simulate application performance metrics
        metrics["app_response_time_ms"] = random.uniform(50, 500)
        metrics["app_requests_per_second"] = random.uniform(10, 100)
        metrics["app_error_rate_percent"] = random.uniform(0, 5)

        # Simulate cache metrics
        metrics["app_cache_hit_rate"] = random.uniform(70, 95)
        metrics["app_cache_size_mb"] = random.uniform(50, 200)

        # Simulate queue metrics
        metrics["app_queue_depth"] = random.randint(0, 50)
        metrics["app_queue_processing_rate"] = random.uniform(5, 20)

        return metrics

    def get_metrics(self) -> Dict[str, float]:
        """Get all system metrics"""
        all_metrics = {}

        # Collect all metric categories
        cpu_metrics = self.get_cpu_metrics()
        memory_metrics = self.get_memory_metrics()
        disk_metrics = self.get_disk_metrics()
        network_metrics = self.get_network_interface_metrics()
        process_metrics = self.get_process_metrics()
        system_metrics = self.get_system_info_metrics()
        app_metrics = self.simulate_application_metrics()

        # Combine all metrics
        all_metrics.update(cpu_metrics)
        all_metrics.update(memory_metrics)
        all_metrics.update(disk_metrics)
        all_metrics.update(network_metrics)
        all_metrics.update(process_metrics)
        all_metrics.update(system_metrics)
        all_metrics.update(app_metrics)

        # Calculate overall system health score
        cpu_score = max(0, 100 - all_metrics.get("cpu_usage_percent", 0))
        memory_score = max(0, 100 - all_metrics.get("memory_usage_percent", 0))
        disk_score = max(0, 100 - all_metrics.get("disk_usage_percent", 0))

        system_health = (cpu_score + memory_score + disk_score) / 3
        all_metrics["system_health_score"] = system_health

        return all_metrics
