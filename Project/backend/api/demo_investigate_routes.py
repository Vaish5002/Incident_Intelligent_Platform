"""
Demo Investigation API - Intelligent endpoint that adapts to incident description
Returns contextually appropriate mock data based on failure type
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
import random
import re

router = APIRouter(prefix="/api", tags=["Demo Investigation"])


class InvestigationRequest(BaseModel):
    repo_url: str
    incident_description: str


# Storage for investigation descriptions (so we can return contextual results)
investigation_store = {}


@router.post("/investigate")
async def investigate(request: InvestigationRequest):
    """
    Start investigation - returns mock results for demo
    Stores description for contextual response generation
    """
    try:
        logger.info(f"Investigation started: {request.incident_description}")
        
        # Generate investigation ID
        investigation_id = random.randint(1000, 9999)
        
        # Store the description for later contextual response
        investigation_store[investigation_id] = {
            "description": request.incident_description,
            "repo_url": request.repo_url
        }
        
        # Return immediate success with investigation ID
        return {
            "success": True,
            "investigation_id": investigation_id,
            "status": "processing",
            "message": "Investigation started successfully",
            "data": {
                "repo_url": request.repo_url,
                "description": request.incident_description
            }
        }
        
    except Exception as e:
        logger.error(f"Investigation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/investigations/{investigation_id}")
async def get_investigation(investigation_id: int):
    """
    Get investigation results - returns contextually appropriate mock RCA data
    based on the incident description provided during investigation creation
    """
    try:
        logger.info(f"Fetching results for investigation {investigation_id}")
        
        # Get stored investigation details
        stored_investigation = investigation_store.get(investigation_id, {})
        description = stored_investigation.get("description", "")
        
        # Detect failure type from description
        failure_type = detect_failure_type(description)
        logger.info(f"Detected failure type: {failure_type} from description: {description}")
        
        # Generate contextually appropriate RCA
        investigation_data = generate_contextual_rca(failure_type, description)
        
        # Return complete investigation data
        return {
            "success": True,
            "investigation_id": investigation_id,
            "status": "completed",
            "data": {
                "investigation": {
                    "id": investigation_id,
                    "status": "completed",
                    **investigation_data
                },
                "root_cause": investigation_data["root_cause"],
                "severity": investigation_data["severity"]
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch investigation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def detect_failure_type(description: str) -> str:
    """
    Detect failure type from incident description
    """
    description_lower = description.lower()
    
    if any(keyword in description_lower for keyword in ['database', 'db', 'connection', 'pool', 'timeout', 'sql']):
        return "database_timeout"
    elif any(keyword in description_lower for keyword in ['memory', 'leak', 'heap', 'oom', 'outofmemory']):
        return "memory_leak"
    elif any(keyword in description_lower for keyword in ['cpu', 'compute', 'processor', 'spike', '100%']):
        return "cpu_spike"
    elif any(keyword in description_lower for keyword in ['api', 'rate limit', '429', 'throttl', 'quota']):
        return "api_rate_limit"
    elif any(keyword in description_lower for keyword in ['cache', 'redis', 'miss', 'storm', 'invalidation']):
        return "cache_miss"
    elif any(keyword in description_lower for keyword in ['network', 'partition', 'connectivity', 'service-to-service']):
        return "network_partition"
    elif any(keyword in description_lower for keyword in ['disk', 'i/o', 'io', 'storage', 'iops']):
        return "disk_io"
    else:
        return "database_timeout"  # Default


def generate_contextual_rca(failure_type: str, description: str) -> dict:
    """
    Generate contextually appropriate RCA based on failure type
    """
    
    # Common base for all types
    rca_templates = {
        "database_timeout": {
            "severity": "CRITICAL",
            "risk_score": 92,
            "confidence": "96%",
            "correlation_count": 127,
            "incident_type": "Database Connection Issue",
            "timeline": [
                {"time": "09:00 AM", "event": "Deployment - Build #4523", "type": "deployment"},
                {"time": "09:00 AM", "event": "Config change: DB pool 50 → 10", "type": "config_change"},
                {"time": "09:15 AM", "event": "First database timeout errors", "type": "error"},
                {"time": "09:30 AM", "event": "Payment service failures", "type": "error"},
                {"time": "09:45 AM", "event": "1,247 users affected", "type": "impact"}
            ],
            "log_patterns": [
                "Database Timeout: Connection pool exhausted",
                "Failed to acquire connection after 30s",
                "Pool Exhausted: 0/10 connections available"
            ],
            "probable_root_cause": {
                "description": "Database connection pool size reduced from 50 to 10",
                "commit": "abc123",
                "file": "config/database.yml",
                "author": "dev@company.com",
                "confidence": "96%",
                "riskyCodeChanges": [
                    {"file": "config/database.yml", "change": "DB_POOL_SIZE: 50 → 10", "risk": "HIGH"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback commit abc123 (DB pool configuration)", "impact": "Restore service within 5 minutes"},
                {"priority": "SHORT-TERM", "action": "Increase database pool size to 50 connections", "impact": "Handle normal traffic load"},
                {"priority": "MEDIUM-TERM", "action": "Add connection pool monitoring alerts", "impact": "Early warning system (threshold: 80%)"},
                {"priority": "LONG-TERM", "action": "Implement auto-scaling for DB connections", "impact": "Dynamic resource allocation"}
            ],
            "risk_factors": [
                "High user impact (1,247 users)",
                "Revenue loss ($12,500)",
                "Service degradation (87% failure rate)",
                "Critical system affected (Payment service)"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0415-047", "description": "Database pool exhausted", "similarity": 0.95, "resolution": "Increased pool size to 50", "outcome": "Resolved in 15 minutes"},
                {"id": "INC-2026-0322-089", "description": "Connection timeout spike", "similarity": 0.87, "resolution": "Added connection monitoring", "outcome": "Prevented future occurrences"}
            ],
            "root_cause": "Database connection pool size was reduced from 50 to 10 connections in commit abc123, causing connection exhaustion under normal load. This configuration change was deployed at 9:00 AM, and first timeout errors appeared at 9:15 AM."
        },
        
        "memory_leak": {
            "severity": "HIGH",
            "risk_score": 88,
            "confidence": "94%",
            "correlation_count": 156,
            "incident_type": "Memory Leak / Resource Exhaustion",
            "timeline": [
                {"time": "08:00 AM", "event": "Deployment - Build #4521", "type": "deployment"},
                {"time": "08:30 AM", "event": "Memory usage at 2GB baseline", "type": "normal"},
                {"time": "10:00 AM", "event": "Memory reached 4GB", "type": "warning"},
                {"time": "12:00 PM", "event": "Memory reached 7GB", "type": "critical"},
                {"time": "12:30 PM", "event": "First OOM errors, container restarts", "type": "error"}
            ],
            "log_patterns": [
                "java.lang.OutOfMemoryError: Java heap space",
                "Container killed due to memory limit exceeded",
                "Heap dump generated: heap-12-30-2026.hprof"
            ],
            "probable_root_cause": {
                "description": "Unclosed database connections in payment processing loop causing memory leak",
                "commit": "def456",
                "file": "src/payment/processor.java",
                "author": "dev@company.com",
                "confidence": "94%",
                "riskyCodeChanges": [
                    {"file": "src/payment/processor.java", "change": "Added connection pool in loop without proper closure", "risk": "HIGH"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback commit def456 and restart all containers", "impact": "Stop memory leak immediately"},
                {"priority": "SHORT-TERM", "action": "Add try-finally blocks to ensure connection closure", "impact": "Prevent resource leaks"},
                {"priority": "MEDIUM-TERM", "action": "Implement memory usage monitoring and alerts", "impact": "Early warning system (threshold: 70%)"},
                {"priority": "LONG-TERM", "action": "Conduct heap dump analysis and optimize object lifecycle", "impact": "Reduce baseline memory footprint"}
            ],
            "risk_factors": [
                "Progressive degradation over 4 hours",
                "Container restarts causing session loss",
                "Heap exhaustion affecting all services",
                "Production stability compromised"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0401-023", "description": "Memory leak in connection handling", "similarity": 0.92, "resolution": "Added proper resource cleanup", "outcome": "Resolved permanently"}
            ],
            "root_cause": "Unclosed database connections in payment processing loop (commit def456) causing memory leak. Heap size grew from 2GB to 8GB over 4 hours, leading to OutOfMemoryError and container restarts."
        },
        
        "cpu_spike": {
            "severity": "CRITICAL",
            "risk_score": 90,
            "confidence": "97%",
            "correlation_count": 143,
            "incident_type": "CPU Saturation / Performance Degradation",
            "timeline": [
                {"time": "14:00 PM", "event": "Deployment - Build #4525", "type": "deployment"},
                {"time": "14:05 PM", "event": "CPU utilization jumped to 98%", "type": "critical"},
                {"time": "14:10 PM", "event": "API response times degraded to 25s", "type": "error"},
                {"time": "14:15 PM", "event": "Request queue backing up", "type": "error"},
                {"time": "14:20 PM", "event": "85% of requests timing out", "type": "impact"}
            ],
            "log_patterns": [
                "CPU utilization: 99.2% (all cores)",
                "Request timeout after 30s",
                "Thread pool exhausted: 200/200 threads busy"
            ],
            "probable_root_cause": {
                "description": "Inefficient sorting algorithm with O(n²) complexity in order processing",
                "commit": "ghi789",
                "file": "src/order/sorting.java",
                "author": "dev@company.com",
                "confidence": "97%",
                "riskyCodeChanges": [
                    {"file": "src/order/sorting.java", "change": "Replaced optimized sort with nested loop", "risk": "CRITICAL"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback commit ghi789 to restore performance", "impact": "Restore normal CPU levels within 2 minutes"},
                {"priority": "SHORT-TERM", "action": "Replace O(n²) algorithm with O(n log n) implementation", "impact": "Reduce CPU usage by 90%"},
                {"priority": "MEDIUM-TERM", "action": "Add performance profiling to CI/CD pipeline", "impact": "Catch performance regressions before production"},
                {"priority": "LONG-TERM", "action": "Implement caching layer for frequently accessed data", "impact": "Further reduce compute requirements"}
            ],
            "risk_factors": [
                "All cores at maximum utilization",
                "85% request timeout rate",
                "Response time degraded 100x (250ms → 25s)",
                "Revenue-generating APIs affected"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0320-067", "description": "Algorithm inefficiency CPU spike", "similarity": 0.93, "resolution": "Optimized algorithm complexity", "outcome": "CPU usage reduced 85%"}
            ],
            "root_cause": "Inefficient O(n²) sorting algorithm introduced in commit ghi789 (file: src/order/sorting.java). Under production load, this caused CPU saturation at 99%, degrading API response times from 250ms to 25+ seconds."
        },
        
        "api_rate_limit": {
            "severity": "HIGH",
            "risk_score": 82,
            "confidence": "91%",
            "correlation_count": 98,
            "incident_type": "External API Rate Limiting",
            "timeline": [
                {"time": "10:00 AM", "event": "Black Friday traffic spike started", "type": "normal"},
                {"time": "10:15 AM", "event": "Payment API requests: 150/min (limit: 100/min)", "type": "warning"},
                {"time": "10:20 AM", "event": "First 429 Too Many Requests errors", "type": "error"},
                {"time": "10:30 AM", "event": "40% of checkouts failing", "type": "impact"},
                {"time": "10:45 AM", "event": "Emergency rate limiting applied", "type": "mitigation"}
            ],
            "log_patterns": [
                "HTTP 429: Too Many Requests from payment-gateway.example.com",
                "Rate limit exceeded: 150/100 requests per minute",
                "Retry-After: 60 seconds"
            ],
            "probable_root_cause": {
                "description": "Traffic spike exceeded payment gateway API quota without retry backoff",
                "commit": "jkl012",
                "file": "src/payment/gateway-client.java",
                "author": "dev@company.com",
                "confidence": "91%",
                "riskyCodeChanges": [
                    {"file": "src/payment/gateway-client.java", "change": "Removed exponential backoff retry logic", "risk": "HIGH"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Implement exponential backoff with jitter for 429 responses", "impact": "Reduce failed checkout rate immediately"},
                {"priority": "SHORT-TERM", "action": "Request quota increase from payment gateway vendor", "impact": "Handle Black Friday traffic levels"},
                {"priority": "MEDIUM-TERM", "action": "Add circuit breaker pattern to prevent cascade failures", "impact": "Graceful degradation under load"},
                {"priority": "LONG-TERM", "action": "Implement payment gateway failover to secondary provider", "impact": "High availability for payment processing"}
            ],
            "risk_factors": [
                "40% checkout failure rate",
                "Peak traffic period (Black Friday)",
                "Revenue loss estimated $25,000/hour",
                "External dependency bottleneck"
            ],
            "similar_incidents": [
                {"id": "INC-2025-1125-034", "description": "Payment API rate limiting during Cyber Monday", "similarity": 0.89, "resolution": "Implemented retry backoff + quota increase", "outcome": "Zero failures during next sale event"}
            ],
            "root_cause": "Payment gateway API rate limit (100 requests/minute) exceeded during Black Friday traffic spike. Commit jkl012 removed exponential backoff retry logic, causing immediate failures instead of graceful retries. 40% of checkout attempts failed."
        },
        
        "cache_miss": {
            "severity": "CRITICAL",
            "risk_score": 89,
            "confidence": "93%",
            "correlation_count": 167,
            "incident_type": "Cache Miss Storm / Database Overload",
            "timeline": [
                {"time": "03:00 AM", "event": "Scheduled Redis maintenance started", "type": "maintenance"},
                {"time": "03:05 AM", "event": "All cache keys cleared", "type": "config_change"},
                {"time": "03:10 AM", "event": "Cache miss rate: 100%", "type": "error"},
                {"time": "03:12 AM", "event": "Database queries: 10,000/sec (normal: 100/sec)", "type": "critical"},
                {"time": "03:15 AM", "event": "Database connection pool exhausted", "type": "impact"}
            ],
            "log_patterns": [
                "Cache miss for key: product_catalog_*",
                "Database connection timeout",
                "Query execution time: 15,000ms (normal: 50ms)"
            ],
            "probable_root_cause": {
                "description": "Mass cache expiry during maintenance without warming strategy",
                "commit": "mno345",
                "file": "config/redis-maintenance.sh",
                "author": "ops@company.com",
                "confidence": "93%",
                "riskyCodeChanges": [
                    {"file": "config/redis-maintenance.sh", "change": "Added FLUSHALL command without cache warming", "risk": "CRITICAL"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Implement cache warming script for top 1000 keys", "impact": "Restore cache hit rate to 95%+ within 10 minutes"},
                {"priority": "SHORT-TERM", "action": "Stagger cache key TTLs to prevent mass expiry", "impact": "Distribute cache refresh load over time"},
                {"priority": "MEDIUM-TERM", "action": "Add cache hit rate monitoring and alerts", "impact": "Early warning when hit rate drops below 80%"},
                {"priority": "LONG-TERM", "action": "Implement multi-layer caching (L1: in-memory, L2: Redis)", "impact": "Resilience against cache layer failures"}
            ],
            "risk_factors": [
                "100% cache miss rate",
                "Database overload (100x normal query rate)",
                "Response time degraded 300x (50ms → 15s)",
                "All services affected"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0215-078", "description": "Redis restart causing cache miss storm", "similarity": 0.94, "resolution": "Implemented cache warming + TTL staggering", "outcome": "No similar incidents since"}
            ],
            "root_cause": "Scheduled Redis maintenance (commit mno345) cleared all cache keys without warming strategy. 100% cache miss rate caused database query storm (100/sec → 10,000/sec), exhausting connection pool and degrading response times 300x."
        },
        
        "network_partition": {
            "severity": "CRITICAL",
            "risk_score": 95,
            "confidence": "98%",
            "correlation_count": 134,
            "incident_type": "Network Partition / Service Communication Failure",
            "timeline": [
                {"time": "10:00 AM", "event": "Kubernetes network policy applied", "type": "config_change"},
                {"time": "10:02 AM", "event": "Payment service cannot reach order service", "type": "error"},
                {"time": "10:05 AM", "event": "TCP connection timeouts (30s)", "type": "error"},
                {"time": "10:08 AM", "event": "Service mesh reporting 85% failure rate", "type": "critical"},
                {"time": "10:15 AM", "event": "Distributed transactions failing", "type": "impact"}
            ],
            "log_patterns": [
                "Connection refused: order-service:8080",
                "TCP connection timeout after 30s",
                "Service mesh: route not found for order-service.prod.svc"
            ],
            "probable_root_cause": {
                "description": "Kubernetes network policy blocking service-to-service communication",
                "commit": "pqr678",
                "file": "k8s/network-policies.yaml",
                "author": "ops@company.com",
                "confidence": "98%",
                "riskyCodeChanges": [
                    {"file": "k8s/network-policies.yaml", "change": "Added restrictive ingress rules blocking payment→order communication", "risk": "CRITICAL"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback network policy pqr678 to restore connectivity", "impact": "Restore service communication within 1 minute"},
                {"priority": "SHORT-TERM", "action": "Update network policy to allow payment→order traffic", "impact": "Implement security without breaking functionality"},
                {"priority": "MEDIUM-TERM", "action": "Add circuit breaker pattern for service-to-service calls", "impact": "Graceful degradation during network issues"},
                {"priority": "LONG-TERM", "action": "Implement network policy testing in staging environment", "impact": "Catch connectivity issues before production"}
            ],
            "risk_factors": [
                "Complete communication failure between services",
                "85% distributed transaction failure rate",
                "Data consistency issues",
                "Multiple microservices affected"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0305-091", "description": "Firewall rule blocking service mesh traffic", "similarity": 0.91, "resolution": "Corrected firewall rules + added connectivity tests", "outcome": "Prevented recurrence"}
            ],
            "root_cause": "Kubernetes network policy (commit pqr678, file: k8s/network-policies.yaml) applied at 10:00 AM blocked communication between payment service and order service. TCP connections timing out after 30s, causing 85% distributed transaction failure rate and data inconsistency."
        },
        
        "disk_io": {
            "severity": "HIGH",
            "risk_score": 86,
            "confidence": "92%",
            "correlation_count": 121,
            "incident_type": "Disk I/O Bottleneck / Storage Performance Degradation",
            "timeline": [
                {"time": "01:00 AM", "event": "Data migration job started", "type": "maintenance"},
                {"time": "01:30 AM", "event": "Disk IOPS reached 10,000/sec (capacity)", "type": "warning"},
                {"time": "02:00 AM", "event": "Disk queue depth at 256", "type": "critical"},
                {"time": "02:15 AM", "event": "Database query latency 10x normal", "type": "error"},
                {"time": "02:30 AM", "event": "Write operations backing up", "type": "impact"}
            ],
            "log_patterns": [
                "Disk utilization: 99.8%",
                "I/O wait time: 45% (normal: 2%)",
                "Query execution time: 2,500ms (normal: 250ms)"
            ],
            "probable_root_cause": {
                "description": "Unoptimized data migration job saturating disk I/O capacity",
                "commit": "stu901",
                "file": "jobs/data-migration.py",
                "author": "data@company.com",
                "confidence": "92%",
                "riskyCodeChanges": [
                    {"file": "jobs/data-migration.py", "change": "Removed batch processing, reading entire dataset into memory", "risk": "HIGH"}
                ]
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Pause data migration job to free I/O capacity", "impact": "Restore normal disk performance within 5 minutes"},
                {"priority": "SHORT-TERM", "action": "Rewrite migration job with batch processing and throttling", "impact": "Limit I/O impact to 20% of capacity"},
                {"priority": "MEDIUM-TERM", "action": "Optimize frequently-run queries with indexing", "impact": "Reduce baseline I/O by 40%"},
                {"priority": "LONG-TERM", "action": "Scale to faster storage tier (SSD → NVMe) or increase IOPS", "impact": "Handle growth and future migrations"}
            ],
            "risk_factors": [
                "Disk at 99% utilization",
                "Query performance degraded 10x",
                "Write operations backing up",
                "Transaction log growth"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0228-056", "description": "Bulk data import saturating disk I/O", "similarity": 0.90, "resolution": "Implemented throttling + batch processing", "outcome": "Completed without impact"}
            ],
            "root_cause": "Unoptimized data migration job (commit stu901) saturated disk I/O at capacity (10,000 IOPS). Removed batch processing caused entire dataset to be read into memory, degrading database query performance 10x (250ms → 2,500ms) and backing up write operations."
        }
    }
    
    return rca_templates.get(failure_type, rca_templates["database_timeout"])
