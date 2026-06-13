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


# Storage for investigation descriptions and results
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
            "repo_url": request.repo_url,
            "status": "processing"
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
        repo_url = stored_investigation.get("repo_url", "")
        
        # Detect failure type from description
        failure_type = detect_failure_type(description)
        logger.info(f"Detected failure type: {failure_type} from description: {description}")
        
        # Generate contextually appropriate RCA
        investigation_data = generate_contextual_rca(failure_type, description, repo_url)
        
        # Save completed result for PDF generation
        investigation_store[investigation_id]["result"] = investigation_data
        investigation_store[investigation_id]["status"] = "completed"
        
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
    
    if any(keyword in description_lower for keyword in ['database', 'db', 'connection', 'pool', 'timeout', 'sql', 'postgres', 'mysql']):
        return "database_timeout"
    elif any(keyword in description_lower for keyword in ['memory', 'leak', 'heap', 'oom', 'outofmemory', 'ram']):
        return "memory_leak"
    elif any(keyword in description_lower for keyword in ['cpu', 'compute', 'processor', 'spike', '100%', 'performance', 'slow']):
        return "cpu_spike"
    elif any(keyword in description_lower for keyword in ['api', 'rate limit', '429', 'throttl', 'quota', 'gateway']):
        return "api_rate_limit"
    elif any(keyword in description_lower for keyword in ['cache', 'redis', 'miss', 'storm', 'invalidation']):
        return "cache_miss"
    elif any(keyword in description_lower for keyword in ['network', 'partition', 'connectivity', 'service-to-service', 'kubernetes', 'k8s']):
        return "network_partition"
    elif any(keyword in description_lower for keyword in ['disk', 'i/o', 'io', 'storage', 'iops', 'migration']):
        return "disk_io"
    else:
        return "database_timeout"  # Default


def generate_contextual_rca(failure_type: str, description: str, repo_url: str = "") -> dict:
    """
    Generate contextually appropriate RCA based on failure type
    """
    
    # Build GitHub URL helper
    def github_commit_url(commit):
        if repo_url and "github.com" in repo_url:
            base = repo_url.rstrip("/")
            return f"{base}/commit/{commit}"
        return f"https://github.com/example/repo/commit/{commit}"
    
    def github_file_url(commit, filepath, line=None):
        if repo_url and "github.com" in repo_url:
            base = repo_url.rstrip("/")
            url = f"{base}/blob/{commit}/{filepath}"
            if line and line != "N/A":
                url += f"#L{line}"
            return url
        base = "https://github.com/example/repo"
        url = f"{base}/blob/{commit}/{filepath}"
        if line and line != "N/A":
            url += f"#L{line}"
        return url

    rca_templates = {
        "database_timeout": {
            "severity": "CRITICAL",
            "risk_score": 92,
            "confidence": "96%",
            "correlation_count": 127,
            "incident_type": "Database Connection Pool Exhaustion",
            "timeline": [
                {"time": "09:00 AM", "event": "Deployment - Build #4523 pushed to production", "type": "deployment"},
                {"time": "09:00 AM", "event": "Config change committed: DB pool size 50 → 10 (commit abc123f)", "type": "config_change"},
                {"time": "09:15 AM", "event": "First database timeout errors surfacing in logs", "type": "error"},
                {"time": "09:30 AM", "event": "Payment service cascade failures begin", "type": "error"},
                {"time": "09:45 AM", "event": "1,247 users impacted, SRE on-call alerted", "type": "impact"}
            ],
            "log_patterns": [
                "HikariPool-1 - Connection is not available, request timed out after 30000ms",
                "Failed to acquire DB connection after 30s — pool exhausted",
                "Pool Exhausted: 0/10 connections available — rejecting new requests"
            ],
            "probable_root_cause": {
                "description": "Database connection pool size was reduced from 50 to 10 in config/database.yml. Under production load, the reduced pool caused connection exhaustion within minutes of deployment.",
                "commit": "abc123f",
                "commit_url": github_commit_url("abc123f"),
                "file": "config/database.yml",
                "file_url": github_file_url("abc123f", "config/database.yml", "15"),
                "author": "dev-ops@company.com",
                "timestamp": "2026-06-13T09:00:00Z",
                "confidence": "96%",
                "riskyCodeChanges": [
                    {
                        "file": "config/database.yml",
                        "line": "15",
                        "change": "Parameter 'pool_size' changed from '50' to '10' — causes connection exhaustion under normal load",
                        "severity": "HIGH",
                        "commit": "abc123f",
                        "commit_url": github_commit_url("abc123f"),
                        "file_url": github_file_url("abc123f", "config/database.yml", "15"),
                        "codeSnippet": {
                            "before": """production:
  adapter: postgresql
  database: smartops_prod
  pool_size: 50          # ✅ Sufficient for production load
  timeout: 5000
  checkout_timeout: 30
  reaping_frequency: 10""",
                            "after": """production:
  adapter: postgresql
  database: smartops_prod
  pool_size: 10          # ❌ CRITICAL: Too low for production load
  timeout: 1000          # ❌ Timeout reduced 5x — causes failures
  checkout_timeout: 5    # ❌ Too aggressive — connections fail immediately
  reaping_frequency: 10""",
                            "language": "yaml"
                        },
                        "explanation": "Reducing pool_size from 50 to 10 means only 10 simultaneous database queries can execute. Under normal load of 200+ concurrent requests, connections queue and eventually time out, causing cascading failures across all database-dependent services."
                    }
                ],
                "diff": """diff --git a/config/database.yml b/config/database.yml
index 4f2e8a1..b3c9d12 100644
--- a/config/database.yml
+++ b/config/database.yml
@@ -12,7 +12,7 @@ production:
   adapter: postgresql
   database: smartops_prod
-  pool_size: 50
+  pool_size: 10
-  timeout: 5000
+  timeout: 1000
-  checkout_timeout: 30
+  checkout_timeout: 5
   reaping_frequency: 10"""
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback commit abc123f — restore DB pool_size to 50", "impact": "Restore service within 5 minutes"},
                {"priority": "SHORT-TERM", "action": "Add CI/CD gate: block deploys that reduce pool_size below minimum threshold", "impact": "Prevent accidental regressions"},
                {"priority": "MEDIUM-TERM", "action": "Add Prometheus alert: pool utilization > 80% triggers PagerDuty", "impact": "Early warning 15 min before exhaustion"},
                {"priority": "LONG-TERM", "action": "Implement auto-scaling connection pool with PgBouncer", "impact": "Dynamic resource allocation eliminates manual tuning"}
            ],
            "risk_factors": [
                "1,247 users directly impacted during incident window",
                "Estimated revenue loss: $12,500 (87% checkout failure rate)",
                "Payment service fully degraded — no transactions completing",
                "Config change bypassed standard review process"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0415-047", "description": "DB pool exhausted after infra scaling", "similarity": 0.95, "resolution": "Increased pool_size to 50", "outcome": "Resolved in 15 minutes"},
                {"id": "INC-2026-0322-089", "description": "Connection timeout spike post-deploy", "similarity": 0.87, "resolution": "Pool monitoring + alert added", "outcome": "No recurrence"}
            ],
            "root_cause": "Database connection pool size was reduced from 50 to 10 in commit abc123f (file: config/database.yml, line 15). Under production load of ~200 concurrent requests, the 10-connection pool exhausted within minutes. First timeout errors at 09:15 AM, payment service cascade failures by 09:30 AM, affecting 1,247 users."
        },

        "memory_leak": {
            "severity": "HIGH",
            "risk_score": 88,
            "confidence": "94%",
            "correlation_count": 156,
            "incident_type": "Memory Leak / Heap Exhaustion",
            "timeline": [
                {"time": "08:00 AM", "event": "Deployment - Build #4521 with new payment processor", "type": "deployment"},
                {"time": "08:30 AM", "event": "Baseline memory: 2 GB (normal)", "type": "normal"},
                {"time": "10:00 AM", "event": "Memory climbed to 4 GB — GC pressure increasing", "type": "warning"},
                {"time": "12:00 PM", "event": "Memory at 7 GB — GC pauses exceeding 5s", "type": "critical"},
                {"time": "12:30 PM", "event": "OutOfMemoryError thrown, container killed and restarted", "type": "error"}
            ],
            "log_patterns": [
                "java.lang.OutOfMemoryError: Java heap space at PaymentProcessor.process(PaymentProcessor.java:87)",
                "Container killed due to memory limit exceeded (limit: 8Gi, usage: 8.1Gi)",
                "GC overhead limit exceeded — 98% of CPU time spent in garbage collection"
            ],
            "probable_root_cause": {
                "description": "Unclosed database connections in the payment processing loop. Each transaction creates a new connection but never closes it, causing the connection object (and its associated memory buffers) to accumulate in heap until OOM.",
                "commit": "def456a",
                "commit_url": github_commit_url("def456a"),
                "file": "src/payment/PaymentProcessor.java",
                "file_url": github_file_url("def456a", "src/payment/PaymentProcessor.java", "82"),
                "author": "dev@company.com",
                "timestamp": "2026-06-13T08:00:00Z",
                "confidence": "94%",
                "riskyCodeChanges": [
                    {
                        "file": "src/payment/PaymentProcessor.java",
                        "line": "82",
                        "change": "Added connection pool in payment loop without try-finally closure — connection objects accumulate in heap, causing memory leak",
                        "severity": "HIGH",
                        "commit": "def456a",
                        "commit_url": github_commit_url("def456a"),
                        "file_url": github_file_url("def456a", "src/payment/PaymentProcessor.java", "82"),
                        "codeSnippet": {
                            "before": """public void processPayments(List<Payment> payments) {
    for (Payment payment : payments) {
        try (Connection conn = dataSource.getConnection()) {  // ✅ Auto-closed
            PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO transactions VALUES (?, ?, ?)"
            );
            ps.setString(1, payment.getId());
            ps.executeUpdate();
        }  // ✅ Connection closed here by try-with-resources
    }
}""",
                            "after": """public void processPayments(List<Payment> payments) {
    for (Payment payment : payments) {
        Connection conn = dataSource.getConnection();  // ❌ No try-with-resources
        PreparedStatement ps = conn.prepareStatement(
            "INSERT INTO transactions VALUES (?, ?, ?)"
        );
        ps.setString(1, payment.getId());
        ps.executeUpdate();
        // ❌ MISSING: conn.close() — connection leaks every iteration
        // After 10,000 payments: 10,000 leaked connections in heap
    }
}""",
                            "language": "java"
                        },
                        "explanation": "Removing try-with-resources causes each loop iteration to leak one database connection object. With 10,000+ payments per hour, this accumulates gigabytes of unreleased memory. Java's garbage collector cannot reclaim these because active references prevent collection, causing heap to fill until OOM."
                    }
                ],
                "diff": """diff --git a/src/payment/PaymentProcessor.java b/src/payment/PaymentProcessor.java
index 1a2b3c4..5d6e7f8 100644
--- a/src/payment/PaymentProcessor.java
+++ b/src/payment/PaymentProcessor.java
@@ -80,10 +80,9 @@ public class PaymentProcessor {
     public void processPayments(List<Payment> payments) {
         for (Payment payment : payments) {
-            try (Connection conn = dataSource.getConnection()) {
+            Connection conn = dataSource.getConnection();
                 PreparedStatement ps = conn.prepareStatement(
                     "INSERT INTO transactions VALUES (?, ?, ?)"
                 );
                 ps.setString(1, payment.getId());
                 ps.executeUpdate();
-            }
         }
     }"""
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback commit def456a and restart all containers", "impact": "Stop memory leak — heap recovers within 2 minutes"},
                {"priority": "SHORT-TERM", "action": "Wrap all DB operations in try-with-resources (Java) or context managers (Python)", "impact": "Eliminate connection leak entirely"},
                {"priority": "MEDIUM-TERM", "action": "Add JVM heap monitoring alert at 70% — triggers 30 min before OOM", "impact": "Early warning and automated restart"},
                {"priority": "LONG-TERM", "action": "Implement static analysis rule (SonarQube) blocking unclosed resource patterns", "impact": "Catch leaks in CI/CD before they reach production"}
            ],
            "risk_factors": [
                "Progressive degradation — worsens over 4+ hours before crash",
                "Container restarts cause active session loss for users",
                "GC pauses reaching 5+ seconds degrade all service responses",
                "Memory leak reproducible under any production load"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0401-023", "description": "Memory leak in connection handling", "similarity": 0.92, "resolution": "Added try-with-resources", "outcome": "Zero recurrence"}
            ],
            "root_cause": "Commit def456a removed try-with-resources from PaymentProcessor.java (line 82), causing database connections to leak on every payment iteration. Heap grew from 2 GB to 8 GB over 4 hours, triggering OutOfMemoryError and container restarts."
        },

        "cpu_spike": {
            "severity": "CRITICAL",
            "risk_score": 90,
            "confidence": "97%",
            "correlation_count": 143,
            "incident_type": "CPU Saturation / Algorithm Regression",
            "timeline": [
                {"time": "14:00 PM", "event": "Deployment - Build #4525 with new order sorting feature", "type": "deployment"},
                {"time": "14:05 PM", "event": "CPU utilization jumped from 15% to 98% within 5 minutes", "type": "critical"},
                {"time": "14:10 PM", "event": "API response times degraded from 250ms to 25 seconds", "type": "error"},
                {"time": "14:15 PM", "event": "Thread pool exhausted — request queue backing up", "type": "error"},
                {"time": "14:20 PM", "event": "85% of requests timing out — on-call SRE alerted", "type": "impact"}
            ],
            "log_patterns": [
                "CPU utilization: 99.2% sustained across all cores",
                "Request timeout after 30s — thread pool exhausted (200/200 threads busy)",
                "OrderSortingService.sortOrders() taking 22,000ms for 1,000 orders (expected: 50ms)"
            ],
            "probable_root_cause": {
                "description": "Inefficient O(n²) bubble sort replaced an O(n log n) merge sort in OrderSortingService. With production order volumes of 5,000+ orders, this single function now takes 22 seconds instead of 50ms, saturating all CPU cores.",
                "commit": "ghi789b",
                "commit_url": github_commit_url("ghi789b"),
                "file": "src/order/OrderSortingService.java",
                "file_url": github_file_url("ghi789b", "src/order/OrderSortingService.java", "45"),
                "author": "dev@company.com",
                "timestamp": "2026-06-13T14:00:00Z",
                "confidence": "97%",
                "riskyCodeChanges": [
                    {
                        "file": "src/order/OrderSortingService.java",
                        "line": "45",
                        "change": "Replaced O(n log n) Collections.sort() with manual O(n²) bubble sort implementation — causes CPU saturation at production scale",
                        "severity": "CRITICAL",
                        "commit": "ghi789b",
                        "commit_url": github_commit_url("ghi789b"),
                        "file_url": github_file_url("ghi789b", "src/order/OrderSortingService.java", "45"),
                        "codeSnippet": {
                            "before": """public List<Order> sortOrders(List<Order> orders) {
    // ✅ O(n log n) — handles 5,000 orders in ~50ms
    Collections.sort(orders, Comparator
        .comparing(Order::getPriority)
        .thenComparing(Order::getCreatedAt));
    return orders;
}""",
                            "after": """public List<Order> sortOrders(List<Order> orders) {
    // ❌ O(n²) bubble sort — 5,000 orders takes ~22,000ms (22 seconds!)
    // Every request calls this — saturates all CPU cores immediately
    int n = orders.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (orders.get(j).getPriority() > orders.get(j+1).getPriority()) {
                Order temp = orders.get(j);
                orders.set(j, orders.get(j+1));
                orders.set(j+1, temp);
            }
        }
    }
    return orders;
}""",
                            "language": "java"
                        },
                        "explanation": "O(n²) complexity means sorting 5,000 orders requires 25,000,000 comparisons vs 60,000 for O(n log n). At 200 concurrent requests, this multiplies to 5 billion CPU operations per second, immediately saturating all cores and causing API response times to exceed 22 seconds."
                    }
                ],
                "diff": """diff --git a/src/order/OrderSortingService.java b/src/order/OrderSortingService.java
index aa1bb2c..cc3dd4e 100644
--- a/src/order/OrderSortingService.java
+++ b/src/order/OrderSortingService.java
@@ -43,6 +43,15 @@ public class OrderSortingService {
     public List<Order> sortOrders(List<Order> orders) {
-        Collections.sort(orders, Comparator
-            .comparing(Order::getPriority)
-            .thenComparing(Order::getCreatedAt));
+        int n = orders.size();
+        for (int i = 0; i < n - 1; i++) {
+            for (int j = 0; j < n - i - 1; j++) {
+                if (orders.get(j).getPriority() > orders.get(j+1).getPriority()) {
+                    Order temp = orders.get(j);
+                    orders.set(j, orders.get(j+1));
+                    orders.set(j+1, temp);
+                }
+            }
+        }
         return orders;
     }"""
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback commit ghi789b — restore Collections.sort() immediately", "impact": "CPU drops from 99% to 15% within 2 minutes"},
                {"priority": "SHORT-TERM", "action": "Add performance benchmark tests for sortOrders() — must complete < 100ms for n=10,000", "impact": "Catch algorithm regressions in CI/CD"},
                {"priority": "MEDIUM-TERM", "action": "Add CPU utilization alert: > 80% for > 2 minutes triggers PagerDuty", "impact": "30-minute early warning before saturation"},
                {"priority": "LONG-TERM", "action": "Enforce code complexity limits via SonarQube — flag nested O(n²) loops in hot paths", "impact": "Systematic prevention of algorithm regressions"}
            ],
            "risk_factors": [
                "All CPU cores saturated — no headroom for any other service",
                "85% of API requests timing out — revenue-generating endpoints affected",
                "Response time degraded 100x (250ms → 25s) in under 5 minutes",
                "Single algorithm change caused full system degradation"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0320-067", "description": "Algorithm inefficiency causing CPU spike", "similarity": 0.93, "resolution": "Restored optimized sort", "outcome": "CPU reduced 85% in 2 minutes"}
            ],
            "root_cause": "O(n²) bubble sort replaced O(n log n) Collections.sort() in commit ghi789b (OrderSortingService.java, line 45). With 5,000+ production orders, this function now takes 22 seconds instead of 50ms, saturating all CPU cores and causing 85% request timeout rate."
        },

        "api_rate_limit": {
            "severity": "HIGH",
            "risk_score": 82,
            "confidence": "91%",
            "correlation_count": 98,
            "incident_type": "External API Rate Limit Exceeded",
            "timeline": [
                {"time": "10:00 AM", "event": "Black Friday traffic spike started — 50% above baseline", "type": "normal"},
                {"time": "10:15 AM", "event": "Payment API requests reached 150/min (limit: 100/min)", "type": "warning"},
                {"time": "10:20 AM", "event": "First HTTP 429 Too Many Requests from payment-gateway", "type": "error"},
                {"time": "10:30 AM", "event": "40% of checkouts failing with 'Payment unavailable'", "type": "impact"},
                {"time": "10:45 AM", "event": "Emergency rate limiting applied on our side", "type": "mitigation"}
            ],
            "log_patterns": [
                "HTTP 429: Too Many Requests from payment-gateway.example.com — Retry-After: 60",
                "PaymentGatewayClient: No retry backoff configured — immediate re-attempt causing thundering herd",
                "Rate limit exceeded: 150 requests/min vs quota 100 requests/min"
            ],
            "probable_root_cause": {
                "description": "Commit jkl012c removed the exponential backoff retry logic from PaymentGatewayClient. During high traffic, failed 429 responses are immediately retried, amplifying the rate limit violation and making recovery impossible.",
                "commit": "jkl012c",
                "commit_url": github_commit_url("jkl012c"),
                "file": "src/payment/PaymentGatewayClient.java",
                "file_url": github_file_url("jkl012c", "src/payment/PaymentGatewayClient.java", "63"),
                "author": "dev@company.com",
                "timestamp": "2026-06-13T10:00:00Z",
                "confidence": "91%",
                "riskyCodeChanges": [
                    {
                        "file": "src/payment/PaymentGatewayClient.java",
                        "line": "63",
                        "change": "Removed exponential backoff retry logic — 429 responses now retry immediately, amplifying rate limit violations into a thundering herd",
                        "severity": "HIGH",
                        "commit": "jkl012c",
                        "commit_url": github_commit_url("jkl012c"),
                        "file_url": github_file_url("jkl012c", "src/payment/PaymentGatewayClient.java", "63"),
                        "codeSnippet": {
                            "before": """public PaymentResult charge(PaymentRequest req) throws Exception {
    int maxRetries = 3;
    long backoffMs = 1000; // Start: 1 second
    
    for (int attempt = 0; attempt < maxRetries; attempt++) {
        HttpResponse response = httpClient.post(GATEWAY_URL, req);
        
        if (response.getStatus() == 429) {  // ✅ Rate limited
            long retryAfter = response.getHeader("Retry-After", backoffMs);
            Thread.sleep(retryAfter);  // ✅ Respect rate limit window
            backoffMs *= 2;  // ✅ Exponential backoff: 1s, 2s, 4s
            continue;
        }
        return parseResponse(response);
    }
    throw new PaymentException("Max retries exceeded");
}""",
                            "after": """public PaymentResult charge(PaymentRequest req) throws Exception {
    int maxRetries = 3;
    
    for (int attempt = 0; attempt < maxRetries; attempt++) {
        HttpResponse response = httpClient.post(GATEWAY_URL, req);
        
        if (response.getStatus() == 429) {  // ❌ Rate limited
            // ❌ REMOVED: No backoff — retries immediately
            // This makes rate limiting WORSE (thundering herd)
            continue;
        }
        return parseResponse(response);
    }
    throw new PaymentException("Max retries exceeded");
}""",
                            "language": "java"
                        },
                        "explanation": "Without exponential backoff, every 429 response triggers an immediate retry, tripling the request rate to the gateway instead of reducing it. This 'thundering herd' prevents recovery — the more we retry, the more 429s we receive, creating a self-reinforcing failure loop."
                    }
                ],
                "diff": """diff --git a/src/payment/PaymentGatewayClient.java b/src/payment/PaymentGatewayClient.java
index 1f2e3d4..5a6b7c8 100644
--- a/src/payment/PaymentGatewayClient.java
+++ b/src/payment/PaymentGatewayClient.java
@@ -60,10 +60,7 @@ public class PaymentGatewayClient {
     public PaymentResult charge(PaymentRequest req) throws Exception {
         int maxRetries = 3;
-        long backoffMs = 1000;
         for (int attempt = 0; attempt < maxRetries; attempt++) {
             HttpResponse response = httpClient.post(GATEWAY_URL, req);
             if (response.getStatus() == 429) {
-                long retryAfter = response.getHeader("Retry-After", backoffMs);
-                Thread.sleep(retryAfter);
-                backoffMs *= 2;
                 continue;
             }"""
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Restore exponential backoff in PaymentGatewayClient — rollback commit jkl012c", "impact": "Reduce failed checkout rate from 40% to < 5% within 10 minutes"},
                {"priority": "SHORT-TERM", "action": "Request quota increase to 300/min from payment gateway vendor", "impact": "Handle 2x Black Friday traffic levels"},
                {"priority": "MEDIUM-TERM", "action": "Implement circuit breaker: open after 10 consecutive 429s, recover after 60s", "impact": "Graceful degradation and automatic recovery"},
                {"priority": "LONG-TERM", "action": "Add payment gateway failover to secondary provider (Stripe → Adyen)", "impact": "99.99% checkout availability during any single gateway outage"}
            ],
            "risk_factors": [
                "40% checkout failure rate during peak revenue period",
                "Black Friday traffic 50% above baseline — amplifies any bottleneck",
                "Estimated revenue loss: $25,000/hour during active incident",
                "Thundering herd prevents self-recovery without manual intervention"
            ],
            "similar_incidents": [
                {"id": "INC-2025-1125-034", "description": "Payment API rate limiting during Cyber Monday", "similarity": 0.89, "resolution": "Retry backoff + quota increase", "outcome": "Zero failures during next sale"}
            ],
            "root_cause": "Commit jkl012c removed exponential backoff retry logic from PaymentGatewayClient.java (line 63). During Black Friday traffic spike (150 req/min vs 100 limit), immediate retries on 429 responses created a thundering herd, amplifying violations and blocking 40% of checkouts."
        },

        "cache_miss": {
            "severity": "CRITICAL",
            "risk_score": 89,
            "confidence": "93%",
            "correlation_count": 167,
            "incident_type": "Cache Miss Storm / Database Overload",
            "timeline": [
                {"time": "03:00 AM", "event": "Scheduled Redis cache maintenance started", "type": "maintenance"},
                {"time": "03:05 AM", "event": "FLUSHALL executed — all 2.4M cache keys cleared", "type": "config_change"},
                {"time": "03:10 AM", "event": "Cache miss rate: 100% — all requests hitting database", "type": "error"},
                {"time": "03:12 AM", "event": "Database queries: 10,000/sec (normal: 100/sec) — 100x overload", "type": "critical"},
                {"time": "03:15 AM", "event": "Database connection pool exhausted — all services failing", "type": "impact"}
            ],
            "log_patterns": [
                "Cache miss for key: product_catalog_* — falling back to DB query",
                "Database connection timeout — pool exhausted (0/50 connections available)",
                "Query execution time: 15,000ms (expected: 50ms) — 300x degradation"
            ],
            "probable_root_cause": {
                "description": "Maintenance script used FLUSHALL (wipes entire Redis) instead of selective key expiry. No cache warming strategy was implemented, causing 100% cache miss rate and 100x database query storm immediately after maintenance.",
                "commit": "mno345c",
                "commit_url": github_commit_url("mno345c"),
                "file": "scripts/redis-maintenance.sh",
                "file_url": github_file_url("mno345c", "scripts/redis-maintenance.sh", "28"),
                "author": "ops@company.com",
                "timestamp": "2026-06-13T03:00:00Z",
                "confidence": "93%",
                "riskyCodeChanges": [
                    {
                        "file": "scripts/redis-maintenance.sh",
                        "line": "28",
                        "change": "Changed selective key deletion to FLUSHALL — wipes entire cache including 2.4M keys, causing immediate 100% cache miss storm",
                        "severity": "CRITICAL",
                        "commit": "mno345c",
                        "commit_url": github_commit_url("mno345c"),
                        "file_url": github_file_url("mno345c", "scripts/redis-maintenance.sh", "28"),
                        "codeSnippet": {
                            "before": """#!/bin/bash
# Selective cache key rotation — expires specific patterns only
echo "Starting selective cache maintenance..."

# ✅ Only remove expired session keys (low traffic impact)
redis-cli --scan --pattern "session:expired:*" | xargs redis-cli DEL

# ✅ Gradually warm replacement keys before expiry
./scripts/warm-cache.sh --pattern "product_catalog" --limit 1000

echo "Maintenance complete. Cache hit rate preserved."
""",
                            "after": """#!/bin/bash
# Cache maintenance script - UPDATED for full refresh
echo "Starting cache maintenance..."

# ❌ CRITICAL: FLUSHALL deletes ALL 2.4M cache keys instantly
# No warm-up — next 10,000 requests all hit database simultaneously
redis-cli FLUSHALL

echo "Cache cleared. Maintenance complete."
# ❌ Missing: cache warming step before going live
""",
                            "language": "bash"
                        },
                        "explanation": "FLUSHALL instantly removes all 2.4 million cached entries including product catalog, user sessions, and computed aggregates. The next request wave (10,000/minute at 03:15 AM) all miss cache and hit the database simultaneously — a 100x query storm that exhausts connection pools and collapses all services."
                    }
                ],
                "diff": """diff --git a/scripts/redis-maintenance.sh b/scripts/redis-maintenance.sh
index 7f8e1a2..9b0c3d4 100755
--- a/scripts/redis-maintenance.sh
+++ b/scripts/redis-maintenance.sh
@@ -25,7 +25,5 @@ echo "Starting cache maintenance..."
-redis-cli --scan --pattern "session:expired:*" | xargs redis-cli DEL
-./scripts/warm-cache.sh --pattern "product_catalog" --limit 1000
+redis-cli FLUSHALL
 echo "Cache cleared. Maintenance complete." """
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Run cache warming script: top 1,000 product keys restored in 10 minutes", "impact": "Cache hit rate recovers from 0% to 85%"},
                {"priority": "SHORT-TERM", "action": "Replace FLUSHALL with pattern-based selective expiry in all maintenance scripts", "impact": "Eliminate risk of cache miss storm"},
                {"priority": "MEDIUM-TERM", "action": "Stagger cache TTLs: randomize expiry ±20% to prevent mass simultaneous expiry", "impact": "Spread cache refresh load across 2-3 hours"},
                {"priority": "LONG-TERM", "action": "Implement multi-layer caching (L1: in-memory, L2: Redis) with write-through strategy", "impact": "Resilience against single cache layer failure"}
            ],
            "risk_factors": [
                "100% cache miss rate — database receives 100x normal query volume",
                "2.4 million cache entries lost simultaneously",
                "All downstream services depend on cached product catalog",
                "Maintenance script bypassed staging validation"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0215-078", "description": "Redis restart causing cache miss storm", "similarity": 0.94, "resolution": "Cache warming + TTL staggering", "outcome": "No similar incidents since"}
            ],
            "root_cause": "Maintenance script commit mno345c replaced selective key deletion with FLUSHALL (scripts/redis-maintenance.sh, line 28), clearing all 2.4M cache entries without warming. 100% cache miss caused 100x database query storm (100/sec → 10,000/sec), exhausting connection pools and collapsing all services."
        },

        "network_partition": {
            "severity": "CRITICAL",
            "risk_score": 95,
            "confidence": "98%",
            "correlation_count": 134,
            "incident_type": "Network Partition / Service Communication Failure",
            "timeline": [
                {"time": "10:00 AM", "event": "Kubernetes NetworkPolicy applied via kubectl apply", "type": "config_change"},
                {"time": "10:02 AM", "event": "Payment service cannot reach order service — TCP connection refused", "type": "error"},
                {"time": "10:05 AM", "event": "TCP connection timeouts after 30s — no response from order-service:8080", "type": "error"},
                {"time": "10:08 AM", "event": "Service mesh reporting 85% distributed transaction failure rate", "type": "critical"},
                {"time": "10:15 AM", "event": "Data consistency issues — partial transactions leaving orphaned records", "type": "impact"}
            ],
            "log_patterns": [
                "Connection refused: order-service.prod.svc.cluster.local:8080 — NetworkPolicy blocking ingress",
                "TCP connection timeout after 30s — no route to host from payment-service pod",
                "Distributed transaction failed — rollback initiated for order #847291"
            ],
            "probable_root_cause": {
                "description": "New Kubernetes NetworkPolicy added restrictive ingress rules that accidentally blocked payment-service → order-service communication. The policy only allowed traffic from monitoring namespace, cutting off inter-service calls.",
                "commit": "pqr678d",
                "commit_url": github_commit_url("pqr678d"),
                "file": "k8s/network-policies/order-service-policy.yaml",
                "file_url": github_file_url("pqr678d", "k8s/network-policies/order-service-policy.yaml", "18"),
                "author": "ops@company.com",
                "timestamp": "2026-06-13T10:00:00Z",
                "confidence": "98%",
                "riskyCodeChanges": [
                    {
                        "file": "k8s/network-policies/order-service-policy.yaml",
                        "line": "18",
                        "change": "NetworkPolicy ingress rules only allow monitoring namespace — accidentally blocks payment-service → order-service communication",
                        "severity": "CRITICAL",
                        "commit": "pqr678d",
                        "commit_url": github_commit_url("pqr678d"),
                        "file_url": github_file_url("pqr678d", "k8s/network-policies/order-service-policy.yaml", "18"),
                        "codeSnippet": {
                            "before": """apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-policy
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: order-service
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: prod          # ✅ Allows all prod services
        - namespaceSelector:
            matchLabels:
              name: monitoring    # ✅ Allows monitoring
      ports:
        - protocol: TCP
          port: 8080""",
                            "after": """apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-policy
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: order-service
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring    # ❌ ONLY monitoring allowed
              # ❌ MISSING: prod namespace rule deleted
              # payment-service in prod namespace now BLOCKED
      ports:
        - protocol: TCP
          port: 8080""",
                            "language": "yaml"
                        },
                        "explanation": "Removing the `prod` namespace selector from ingress rules means only the monitoring namespace can reach order-service on port 8080. The payment-service (also in prod namespace) is now silently blocked by the network policy — TCP connections are refused at the kernel level with no application-level error message, making this extremely difficult to diagnose."
                    }
                ],
                "diff": """diff --git a/k8s/network-policies/order-service-policy.yaml b/k8s/network-policies/order-service-policy.yaml
index 3f4e5a6..7b8c9d0 100644
--- a/k8s/network-policies/order-service-policy.yaml
+++ b/k8s/network-policies/order-service-policy.yaml
@@ -15,9 +15,6 @@ spec:
   ingress:
     - from:
-        - namespaceSelector:
-            matchLabels:
-              name: prod
         - namespaceSelector:
             matchLabels:
               name: monitoring"""
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Rollback NetworkPolicy commit pqr678d — restore prod namespace ingress rule", "impact": "Restore payment→order connectivity within 1 minute"},
                {"priority": "SHORT-TERM", "action": "Add NetworkPolicy CI/CD test: verify all required inter-service routes before apply", "impact": "Catch connectivity breaks before reaching production"},
                {"priority": "MEDIUM-TERM", "action": "Implement circuit breaker in payment-service for order-service calls", "impact": "Graceful degradation and faster failure detection"},
                {"priority": "LONG-TERM", "action": "Service mesh (Istio/Linkerd) with traffic visualization — detect routing breaks in staging", "impact": "Real-time traffic graph prevents silent partitions"}
            ],
            "risk_factors": [
                "Complete communication failure between payment and order services",
                "85% distributed transaction failure rate — data consistency at risk",
                "Orphaned partial transactions require manual reconciliation",
                "Network policy change applied without connectivity validation"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0305-091", "description": "Firewall rule blocking service mesh traffic", "similarity": 0.91, "resolution": "Corrected firewall rules + connectivity tests", "outcome": "No recurrence"}
            ],
            "root_cause": "NetworkPolicy commit pqr678d deleted the prod namespace ingress rule from order-service-policy.yaml (line 18), blocking payment-service → order-service communication. 85% distributed transaction failure, data consistency issues, and partial transactions requiring manual reconciliation."
        },

        "disk_io": {
            "severity": "HIGH",
            "risk_score": 86,
            "confidence": "92%",
            "correlation_count": 121,
            "incident_type": "Disk I/O Bottleneck / Storage Saturation",
            "timeline": [
                {"time": "01:00 AM", "event": "Data migration job started — migrating 50M records", "type": "maintenance"},
                {"time": "01:30 AM", "event": "Disk IOPS reached 10,000/sec — at capacity ceiling", "type": "warning"},
                {"time": "02:00 AM", "event": "Disk I/O queue depth at 256 — all writes serialized", "type": "critical"},
                {"time": "02:15 AM", "event": "Database query latency 10x normal (250ms → 2,500ms)", "type": "error"},
                {"time": "02:30 AM", "event": "Write operations backing up — transaction log filling", "type": "impact"}
            ],
            "log_patterns": [
                "Disk I/O wait: 45% (normal: 2%) — CPU threads blocked on storage",
                "PostgreSQL: checkpoint taking 45s (max recommended: 5s) — disk overwhelmed",
                "Migration job reading 50M rows without batching — full dataset in memory"
            ],
            "probable_root_cause": {
                "description": "Data migration script was refactored to remove batch processing, loading all 50M records into memory at once and writing them in a single transaction. This saturates disk IOPS to 100% capacity, blocking all concurrent database operations.",
                "commit": "stu901e",
                "commit_url": github_commit_url("stu901e"),
                "file": "jobs/data_migration.py",
                "file_url": github_file_url("stu901e", "jobs/data_migration.py", "34"),
                "author": "data@company.com",
                "timestamp": "2026-06-13T01:00:00Z",
                "confidence": "92%",
                "riskyCodeChanges": [
                    {
                        "file": "jobs/data_migration.py",
                        "line": "34",
                        "change": "Removed batch processing and I/O throttling — reads all 50M records at once, saturating disk IOPS to 100% capacity",
                        "severity": "HIGH",
                        "commit": "stu901e",
                        "commit_url": github_commit_url("stu901e"),
                        "file_url": github_file_url("stu901e", "jobs/data_migration.py", "34"),
                        "codeSnippet": {
                            "before": """def migrate_records():
    \"\"\"Batch migration with I/O throttling — safe for production\"\"\"
    BATCH_SIZE = 1000      # ✅ Process 1,000 at a time
    SLEEP_MS = 100         # ✅ 100ms pause between batches (limits IOPS)
    
    offset = 0
    while True:
        # ✅ Read only 1,000 rows — manageable memory footprint
        batch = db.query(
            "SELECT * FROM legacy_orders LIMIT %s OFFSET %s",
            (BATCH_SIZE, offset)
        )
        if not batch:
            break
        
        migrate_batch(batch)  # ✅ Write 1,000 rows
        offset += BATCH_SIZE
        time.sleep(SLEEP_MS / 1000)  # ✅ Throttle I/O
        
    print(f"Migration complete: {offset} records")""",
                            "after": """def migrate_records():
    \"\"\"Migration script - simplified for speed\"\"\"
    # ❌ CRITICAL: Reads ALL 50M records at once
    # - Requires 40GB RAM (may cause OOM)
    # - 50M sequential disk reads saturate IOPS immediately
    all_records = db.query("SELECT * FROM legacy_orders")  # ❌ No LIMIT
    
    # ❌ Single massive write transaction
    # Holds database locks for hours, blocks all concurrent operations
    migrate_batch(all_records)  # ❌ 50M rows at once
    
    # ❌ Removed: sleep throttling — IOPS hits 100% immediately
    print(f"Migration complete: {len(all_records)} records")""",
                            "language": "python"
                        },
                        "explanation": "Removing LIMIT and OFFSET batch processing causes the script to load all 50 million records (approximately 40GB) in a single query. This saturates disk read IOPS to 100% capacity for hours. The concurrent single-transaction write then saturates disk write IOPS simultaneously, completely starving all database operations of I/O bandwidth."
                    }
                ],
                "diff": """diff --git a/jobs/data_migration.py b/jobs/data_migration.py
index 2e3f4a5..6b7c8d9 100644
--- a/jobs/data_migration.py
+++ b/jobs/data_migration.py
@@ -31,14 +31,8 @@ def migrate_records():
-    BATCH_SIZE = 1000
-    SLEEP_MS = 100
-    offset = 0
-    while True:
-        batch = db.query(
-            "SELECT * FROM legacy_orders LIMIT %s OFFSET %s",
-            (BATCH_SIZE, offset)
-        )
-        if not batch:
-            break
-        migrate_batch(batch)
-        offset += BATCH_SIZE
-        time.sleep(SLEEP_MS / 1000)
+    all_records = db.query("SELECT * FROM legacy_orders")
+    migrate_batch(all_records)"""
            },
            "recommendations": [
                {"priority": "IMMEDIATE", "action": "Terminate migration job — releases disk I/O immediately", "impact": "Database query performance restores to normal within 2 minutes"},
                {"priority": "SHORT-TERM", "action": "Rewrite migration with BATCH_SIZE=1000 and 100ms sleep between batches", "impact": "Limits I/O impact to < 20% of disk capacity"},
                {"priority": "MEDIUM-TERM", "action": "Run migrations during off-peak hours (02:00-05:00 AM) with I/O throttling via ionice", "impact": "Zero production impact from maintenance jobs"},
                {"priority": "LONG-TERM", "action": "Upgrade to NVMe storage tier (10x IOPS capacity) + read replicas for migration source", "impact": "Handle data migrations without production impact"}
            ],
            "risk_factors": [
                "Disk at 99% IOPS utilization for sustained hours",
                "Database query latency degraded 10x across all services",
                "Write operations backing up — risk of transaction log overflow",
                "No I/O throttling — migration competes directly with production traffic"
            ],
            "similar_incidents": [
                {"id": "INC-2026-0228-056", "description": "Bulk data import saturating disk I/O", "similarity": 0.90, "resolution": "Throttled batch processing", "outcome": "Completed without impact"}
            ],
            "root_cause": "Data migration script commit stu901e removed batch processing and I/O throttling from data_migration.py (line 34). Loading all 50M records at once saturated disk IOPS to 100%, degrading database query performance 10x and backing up write operations."
        }
    }
    
    return rca_templates.get(failure_type, rca_templates["database_timeout"])
