"""
Database operations simulator
Simulates PostgreSQL operations with realistic timing and error patterns
"""

import random
import time
import logging
import os
from typing import Dict, List

logger = logging.getLogger(__name__)

class DatabaseSimulator:
    """Simulates database operations and performance metrics"""
    
    def __init__(self, config):
        self.config = config
        self.connection_pool_size = 20
        self.active_connections = random.randint(5, 15)
        self.query_types = [
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 
            'JOIN', 'AGGREGATE', 'INDEX_SCAN'
        ]
        
        # Database configuration from environment
        self.db_host = os.getenv('PGHOST', 'localhost')
        self.db_name = os.getenv('PGDATABASE', 'app_db')
        self.db_user = os.getenv('PGUSER', 'app_user')
        
        logger.info(f"Database simulator initialized for {self.db_host}:{self.db_name}")
        
    def simulate_query_performance(self) -> Dict[str, float]:
        """Simulate database query performance metrics"""
        metrics = {}
        
        # Simulate different types of queries with realistic timing
        query_metrics = {
            'SELECT': {'min': 2, 'max': 50, 'weight': 0.6},
            'INSERT': {'min': 5, 'max': 100, 'weight': 0.15},
            'UPDATE': {'min': 10, 'max': 200, 'weight': 0.1},
            'DELETE': {'min': 8, 'max': 150, 'weight': 0.05},
            'JOIN': {'min': 20, 'max': 500, 'weight': 0.08},
            'AGGREGATE': {'min': 50, 'max': 1000, 'weight': 0.02}
        }
        
        total_queries = 0
        total_time = 0
        slow_queries = 0
        
        # Simulate query execution over the monitoring period
        for query_type, config in query_metrics.items():
            # Number of queries based on weight
            query_count = int(random.uniform(10, 100) * config['weight'])
            total_queries += query_count
            
            for _ in range(query_count):
                # Query execution time with occasional spikes
                if random.random() < 0.05:  # 5% chance of slow query
                    exec_time = random.uniform(config['max'], config['max'] * 3)
                    slow_queries += 1
                else:
                    exec_time = random.uniform(config['min'], config['max'])
                    
                total_time += exec_time
                
            # Per-query-type metrics
            avg_time = total_time / max(query_count, 1)
            metrics[f'{query_type.lower()}_avg_time_ms'] = avg_time
            metrics[f'{query_type.lower()}_count'] = query_count
            
        # Overall metrics
        metrics['total_queries'] = total_queries
        metrics['average_query_time_ms'] = total_time / max(total_queries, 1)
        metrics['slow_queries_count'] = slow_queries
        metrics['slow_query_percentage'] = (slow_queries / max(total_queries, 1)) * 100
        
        return metrics
        
    def simulate_connection_management(self) -> Dict[str, float]:
        """Simulate database connection pool metrics"""
        metrics = {}
        
        # Simulate connection pool fluctuations
        connection_change = random.randint(-3, 5)
        self.active_connections = max(1, min(self.connection_pool_size, 
                                           self.active_connections + connection_change))
        
        metrics['active_connections'] = self.active_connections
        metrics['connection_pool_utilization'] = (self.active_connections / self.connection_pool_size) * 100
        metrics['max_connections'] = self.connection_pool_size
        
        # Simulate connection errors
        if random.random() < 0.02:  # 2% chance of connection issues
            metrics['connection_errors'] = random.randint(1, 5)
            logger.warning("Database connection errors detected")
        else:
            metrics['connection_errors'] = 0
            
        # Connection wait time
        if self.active_connections > self.connection_pool_size * 0.8:
            metrics['connection_wait_time_ms'] = random.uniform(10, 100)
        else:
            metrics['connection_wait_time_ms'] = random.uniform(0, 5)
            
        return metrics
        
    def simulate_transaction_metrics(self) -> Dict[str, float]:
        """Simulate database transaction performance"""
        metrics = {}
        
        # Transaction counts
        transactions = random.randint(50, 300)
        commits = int(transactions * random.uniform(0.92, 0.98))
        rollbacks = transactions - commits
        
        metrics['transactions_total'] = transactions
        metrics['transactions_committed'] = commits
        metrics['transactions_rolled_back'] = rollbacks
        metrics['transaction_success_rate'] = (commits / transactions) * 100
        
        # Transaction timing
        metrics['transaction_avg_time_ms'] = random.uniform(50, 500)
        
        # Lock metrics
        metrics['lock_waits'] = random.randint(0, 10)
        metrics['deadlocks'] = random.randint(0, 2) if random.random() < 0.1 else 0
        
        return metrics
        
    def simulate_maintenance_operations(self) -> Dict[str, float]:
        """Simulate database maintenance and background operations"""
        metrics = {}
        
        # Vacuum operations
        if random.random() < 0.1:  # 10% chance of vacuum operation
            metrics['vacuum_operations'] = 1
            metrics['vacuum_duration_ms'] = random.uniform(1000, 10000)
        else:
            metrics['vacuum_operations'] = 0
            
        # Index usage and maintenance
        metrics['index_scans'] = random.randint(100, 1000)
        metrics['sequential_scans'] = random.randint(10, 100)
        metrics['index_hit_ratio'] = random.uniform(85, 99)
        
        # Cache performance
        metrics['buffer_cache_hit_ratio'] = random.uniform(90, 99.5)
        metrics['shared_buffer_usage_mb'] = random.uniform(100, 512)
        
        return metrics
        
    def simulate_error_conditions(self) -> Dict[str, float]:
        """Simulate various database error conditions"""
        metrics = {}
        
        # Query errors
        if random.random() < 0.05:  # 5% chance of query errors
            metrics['query_errors'] = random.randint(1, 10)
            error_types = ['syntax_error', 'constraint_violation', 'timeout', 'permission_denied']
            error_type = random.choice(error_types)
            logger.warning(f"Database query error: {error_type}")
        else:
            metrics['query_errors'] = 0
            
        # Disk space simulation
        disk_usage = random.uniform(60, 95)
        metrics['disk_usage_percentage'] = disk_usage
        
        if disk_usage > 90:
            logger.warning(f"High disk usage: {disk_usage:.1f}%")
            
        # Replication lag (if applicable)
        if random.random() < 0.3:  # 30% chance of having replication
            metrics['replication_lag_ms'] = random.uniform(0, 1000)
            
        return metrics
        
    def simulate_operations(self) -> Dict[str, float]:
        """Run all database simulations and return combined metrics"""
        all_metrics = {}
        
        # Run all simulation components
        query_metrics = self.simulate_query_performance()
        connection_metrics = self.simulate_connection_management()
        transaction_metrics = self.simulate_transaction_metrics()
        maintenance_metrics = self.simulate_maintenance_operations()
        error_metrics = self.simulate_error_conditions()
        
        # Combine all metrics
        all_metrics.update(query_metrics)
        all_metrics.update(connection_metrics)
        all_metrics.update(transaction_metrics)
        all_metrics.update(maintenance_metrics)
        all_metrics.update(error_metrics)
        
        # Add overall database health score
        error_factor = all_metrics.get('query_errors', 0) + all_metrics.get('connection_errors', 0)
        performance_factor = 100 - (all_metrics.get('average_query_time_ms', 50) / 10)
        health_score = max(0, min(100, performance_factor - error_factor))
        
        all_metrics['database_health_score'] = health_score
        
        return all_metrics
