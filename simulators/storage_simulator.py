"""
Azure Blob Storage operations simulator
Simulates file uploads, downloads, and storage metrics
"""

import random
import time
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class StorageSimulator:
    """Simulates Azure Blob Storage operations and performance metrics"""

    def __init__(self, config):
        self.config = config
        self.containers = ["app-data", "user-uploads", "backups", "logs", "images"]
        self.file_types = {
            "images": {"size_range": (100, 5000), "weight": 0.4},
            "documents": {"size_range": (50, 2000), "weight": 0.25},
            "videos": {"size_range": (10000, 100000), "weight": 0.1},
            "logs": {"size_range": (1, 100), "weight": 0.15},
            "backups": {"size_range": (1000, 50000), "weight": 0.1},
        }

        logger.info("Azure Blob Storage simulator initialized")

    def simulate_upload_operations(self) -> Dict[str, float]:
        """Simulate blob upload operations"""
        metrics = {}

        total_uploads = random.randint(10, 50)
        total_size_kb = 0
        total_upload_time = 0
        failed_uploads = 0

        for _ in range(total_uploads):
            # Select file type and size
            file_type = random.choices(
                list(self.file_types.keys()),
                weights=[props["weight"] for props in self.file_types.values()],
            )[0]

            size_range = self.file_types[file_type]["size_range"]
            file_size_kb = random.uniform(size_range[0], size_range[1])
            total_size_kb += file_size_kb

            # Simulate upload time based on file size and network conditions
            base_upload_time = file_size_kb / 1000  # Base: 1MB per second
            network_factor = random.uniform(0.5, 2.0)  # Network variance
            upload_time = base_upload_time * network_factor

            # Simulate occasional upload failures
            if random.random() < 0.03:  # 3% failure rate
                failed_uploads += 1
                upload_time *= 2  # Failed uploads take longer
                logger.warning(f"Blob upload failed for {file_type} file")

            total_upload_time += upload_time

        metrics["uploads_total"] = total_uploads
        metrics["uploads_failed"] = failed_uploads
        metrics["upload_success_rate"] = (
            (total_uploads - failed_uploads) / total_uploads
        ) * 100
        metrics["total_upload_size_kb"] = total_size_kb
        metrics["average_upload_time_seconds"] = total_upload_time / total_uploads
        metrics["upload_throughput_kbps"] = total_size_kb / max(total_upload_time, 0.1)

        return metrics

    def simulate_download_operations(self) -> Dict[str, float]:
        """Simulate blob download operations"""
        metrics = {}

        total_downloads = random.randint(20, 100)
        total_size_kb = 0
        total_download_time = 0
        cache_hits = 0

        for _ in range(total_downloads):
            # File size for downloads (typically requested files)
            file_size_kb = random.uniform(50, 5000)
            total_size_kb += file_size_kb

            # Simulate cache hits
            if random.random() < 0.4:  # 40% cache hit rate
                cache_hits += 1
                download_time = random.uniform(0.1, 0.5)  # Cache hits are fast
            else:
                # Actual download from blob storage
                base_download_time = file_size_kb / 2000  # 2MB per second
                network_factor = random.uniform(0.8, 1.5)
                download_time = base_download_time * network_factor

            total_download_time += download_time

        metrics["downloads_total"] = total_downloads
        metrics["download_cache_hits"] = cache_hits
        metrics["download_cache_hit_rate"] = (cache_hits / total_downloads) * 100
        metrics["total_download_size_kb"] = total_size_kb
        metrics["average_download_time_seconds"] = total_download_time / total_downloads
        metrics["download_throughput_kbps"] = total_size_kb / max(
            total_download_time, 0.1
        )

        return metrics

    def simulate_storage_metrics(self) -> Dict[str, float]:
        """Simulate storage capacity and usage metrics"""
        metrics = {}

        # Simulate storage usage per container
        total_storage_gb = 0
        for container in self.containers:
            container_size = random.uniform(10, 500)  # GB
            total_storage_gb += container_size
            metrics[f"{container}_storage_gb"] = container_size

        metrics["total_storage_gb"] = total_storage_gb
        metrics["storage_cost_estimate_usd"] = total_storage_gb * 0.02  # $0.02 per GB

        # Simulate blob count
        total_blobs = random.randint(10000, 100000)
        metrics["total_blob_count"] = total_blobs

        # Storage tier distribution
        hot_tier_percentage = random.uniform(20, 40)
        cool_tier_percentage = random.uniform(30, 50)
        archive_tier_percentage = 100 - hot_tier_percentage - cool_tier_percentage

        metrics["hot_tier_percentage"] = hot_tier_percentage
        metrics["cool_tier_percentage"] = cool_tier_percentage
        metrics["archive_tier_percentage"] = archive_tier_percentage

        return metrics

    def simulate_api_operations(self) -> Dict[str, float]:
        """Simulate Azure Storage API calls and performance"""
        metrics = {}

        # API call counts
        api_calls = {
            "list_blobs": random.randint(50, 200),
            "get_blob_properties": random.randint(100, 500),
            "put_blob": random.randint(20, 100),
            "delete_blob": random.randint(5, 30),
            "copy_blob": random.randint(1, 10),
        }

        total_api_calls = sum(api_calls.values())
        metrics["total_api_calls"] = total_api_calls

        for operation, count in api_calls.items():
            metrics[f"{operation}_count"] = count

        # API response times
        metrics["api_average_response_ms"] = random.uniform(50, 300)

        # API errors
        api_errors = random.randint(0, 5) if random.random() < 0.1 else 0
        metrics["api_errors"] = api_errors
        metrics["api_error_rate"] = (
            (api_errors / total_api_calls) * 100 if total_api_calls > 0 else 0
        )

        # Throttling events
        throttling_events = random.randint(0, 2) if random.random() < 0.05 else 0
        metrics["throttling_events"] = throttling_events

        if throttling_events > 0:
            logger.warning(
                f"Storage API throttling detected: {throttling_events} events"
            )

        return metrics

    def simulate_security_metrics(self) -> Dict[str, float]:
        """Simulate storage security and access metrics"""
        metrics = {}

        # Access pattern metrics
        anonymous_requests = random.randint(0, 10)
        authenticated_requests = random.randint(100, 1000)

        metrics["anonymous_requests"] = anonymous_requests
        metrics["authenticated_requests"] = authenticated_requests
        metrics["total_requests"] = anonymous_requests + authenticated_requests

        # Security violations
        unauthorized_attempts = random.randint(0, 3) if random.random() < 0.08 else 0
        metrics["unauthorized_access_attempts"] = unauthorized_attempts

        if unauthorized_attempts > 0:
            logger.warning(
                f"Unauthorized storage access attempts: {unauthorized_attempts}"
            )

        # SAS token usage
        sas_token_requests = random.randint(20, 100)
        metrics["sas_token_requests"] = sas_token_requests

        return metrics

    def simulate_operations(self) -> Dict[str, float]:
        """Run all storage simulations and return combined metrics"""
        all_metrics = {}

        # Run all simulation components
        upload_metrics = self.simulate_upload_operations()
        download_metrics = self.simulate_download_operations()
        storage_metrics = self.simulate_storage_metrics()
        api_metrics = self.simulate_api_operations()
        security_metrics = self.simulate_security_metrics()

        # Combine all metrics
        all_metrics.update(upload_metrics)
        all_metrics.update(download_metrics)
        all_metrics.update(storage_metrics)
        all_metrics.update(api_metrics)
        all_metrics.update(security_metrics)

        # Calculate overall storage performance score
        upload_success = all_metrics.get("upload_success_rate", 100)
        api_success = 100 - all_metrics.get("api_error_rate", 0)
        security_score = 100 - (all_metrics.get("unauthorized_access_attempts", 0) * 10)

        performance_score = (upload_success + api_success + security_score) / 3
        all_metrics["storage_performance_score"] = max(0, min(100, performance_score))

        return all_metrics
