// Mock database representing the 5 incidents and associated metadata for SmartOps AI

export const mockIncidents = [
  {
    id: "INC-3091",
    name: "INC-3091: Core DB Connection Pool Exhaustion",
    shortName: "Core DB Connection Pool Exhaustion",
    severity: "CRITICAL",
    status: "INVESTIGATING",
    time: "2026-06-08 11:20:00",
    riskScore: 92,
    errorCount: 2405,
    category: "Database",
    activeUsersAffected: 1420,
    impactScore: 9.5,
    logAnalysis: {
      rootCause: "Database connection pool exhausted due to unindexed query on table 'orders' during high concurrency bulk execution.",
      errorPatterns: [
        "HikariPool-1 - Connection is not available, request timed out after 30000ms.",
        "java.sql.SQLTransientConnectionException: Connection is not available.",
        "PostgreSQL Exception: fatal: remaining connection slots are reserved for non-replication superuser connections"
      ],
      errorCount: 2405,
      rawLogs: `2026-06-08 11:15:01.402 INFO  [org.hibernate.engine.jdbc.connections.internal.DriverManagerConnectionProviderImpl] - HHH000115: Hibernate connection pool size: 20
2026-06-08 11:15:15.984 WARN  [com.zaxxer.hikari.pool.HikariPool] - HikariPool-1 - Connection is not available, request timed out after 30000ms.
2026-06-08 11:15:45.989 ERROR [com.smartops.orders.OrderController] - Error processing checkout request for user_id: 884912
java.sql.SQLTransientConnectionException: HikariPool-1 - Connection is not available, request timed out after 30000ms.
  at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:218) ~[HikariCP-5.0.1.jar:na]
  at com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:162) ~[HikariCP-5.0.1.jar:na]
  at org.hibernate.engine.jdbc.connections.internal.DatasourceConnectionProviderImpl.getConnection(DatasourceConnectionProviderImpl.java:122) ~[hibernate-core-6.2.5.Final.jar:6.2.5.Final]
  at com.smartops.orders.OrderService.processBatch(OrderService.js:142) ~[classes/:na]
2026-06-08 11:16:02.115 ERROR [org.postgresql.Driver] - FATAL: remaining connection slots are reserved for non-replication superuser connections`
    },
    timelineAnalysis: {
      sequence: [
        { time: "11:15:00", event: "Webapp: Database query response latency spikes from 120ms to 12.4s.", type: "warning" },
        { time: "11:17:30", event: "DB Server: Active connection count hits maximum threshold (500 connections).", type: "critical" },
        { time: "11:18:12", event: "Webapp: Connection acquisition timeouts begin throwing SQL Transient Exceptions in OrderService.", type: "critical" },
        { time: "11:20:00", event: "SmartOps Agent: Anomalous exception spike detected. Automated alert sent to DBA on-call.", type: "info" }
      ],
      duration: "45 minutes",
      triggerType: "Deployment"
    },
    gitAnalysis: {
      riskyCodeChanges: [
        {
          file: "src/services/OrderService.js",
          line: 142,
          change: "Added a raw query `SELECT * FROM orders WHERE status = ? AND user_id = ?` inside a loop without composite indexing.",
          severity: "HIGH"
        }
      ],
      commitHash: "db97a2f1",
      author: "j.doe@smartops.ai",
      diff: `diff --git a/src/services/OrderService.js b/src/services/OrderService.js
index f30f142..8b5cf6d 100644
--- a/src/services/OrderService.js
+++ b/src/services/OrderService.js
@@ -139,5 +139,10 @@ class OrderService {
   async processBatch(orders) {
     for (const order of orders) {
-      const status = await this.db.query('SELECT status FROM order_status WHERE id = ?', [order.id]);
+      // Risky Change: Added unindexed query inside bulk order processing loop
+      const activeOrders = await this.db.query(
+        'SELECT * FROM orders WHERE status = ? AND user_id = ?',
+        [order.status, order.userId]
+      );
       await this.updateStatus(order.id, activeOrders);
     }
   }`
    },
    riskAssessment: {
      score: 92,
      severity: "CRITICAL",
      confidence: "96%",
      riskFactors: [
        "Database pool utilization at 100%",
        "Frontend checkout failures reaching 84%",
        "Database CPU utilization at 98%"
      ]
    },
    aiRecommendations: [
      "Roll back OrderService deployment (Commit db97a2f1) to restore query efficiency immediately.",
      "Execute database migration to add a composite index: `CREATE INDEX CONCURRENTLY idx_orders_user_status ON orders(user_id, status);`",
      "Refactor OrderService.js line 142 to batch query orders using SQL `IN` operator instead of query-in-loop (N+1 pattern)."
    ],
    rcaReport: {
      executiveSummary: "On June 8, 2026, our production PostgreSQL database experienced connection pool exhaustion, causing checkout transactions to fail for approximately 45 minutes. The incident began 15 minutes after deployment of release v2.4.1.",
      rootCause: "A query added to OrderService.js loaded user orders inside a batch processing loop, creating an N+1 query problem. Because the 'orders' table (8.4M records) lacked a composite index on (user_id, status), each loop iteration triggered a full table scan, locking up database connections.",
      businessImpact: "Transaction success rate dropped to 16% for 45 minutes. A total of 1,420 users were directly affected. Estimated revenue impact: $42,000 in lost orders.",
      correctiveActions: [
        "Terminated active blocked PostgreSQL connection sessions manually.",
        "Rolled back checkout service deployment to version v2.4.0."
      ],
      preventiveActions: [
        "Create a composite index on orders (user_id, status) in the production database.",
        "Implement static analysis (ESLint/SonarQube rules) to block N+1 query loops.",
        "Configure query timeout limits in the Hikari connection pool (max 5000ms)."
      ]
    },
    copilotQas: {
      "Why did this incident happen?": "The incident was caused by database connection pool exhaustion. A new code change introduced an N+1 query inside a loop, querying the database repeatedly. Since the orders table lacked an index for that query, PostgreSQL was forced to run full table scans, taking seconds per query and locking up all 500 connection pool slots.",
      "What failed first?": "The PostgreSQL connection slots hit their maximum limit. After that, HikariCP (our Java-based application connection pool manager) began failing to acquire connections, raising SQLTransientConnectionException timeout errors.",
      "How can this be prevented?": "1. Avoid query-in-loop design; batch queries using 'WHERE user_id IN (...)'.\n2. Create a composite index on orders(user_id, status) to make lookup O(log N) instead of a full table scan.\n3. Decrease query timeouts in the pool settings to fail early rather than blocking threads.",
      "Which code change caused the issue?": "The issue was caused by Commit db97a2f1 in `src/services/OrderService.js` at line 142, which introduced: `SELECT * FROM orders WHERE status = ? AND user_id = ?` inside the loop."
    }
  },
  {
    id: "INC-3092",
    name: "INC-3092: Edge Gateway 504 Gateway Timeout",
    shortName: "Edge Gateway 504 Timeout",
    severity: "HIGH",
    status: "INVESTIGATING",
    time: "2026-06-08 09:12:00",
    riskScore: 81,
    errorCount: 820,
    category: "Network",
    activeUsersAffected: 3100,
    impactScore: 8.0,
    logAnalysis: {
      rootCause: "Downstream authentication service (/api/v1/auth) became unresponsive due to memory allocation failure, crashing worker nodes and saturating Kong Gateway slots.",
      errorPatterns: [
        "[error] 1421#0: *2843 upstream timed out (110: Connection timed out) while connecting to upstream",
        "Kong Gateway upstream response timed out, endpoint: /api/v1/auth"
      ],
      errorCount: 820,
      rawLogs: `2026-06-08 09:05:12.889 [warn] gateway-1: upstream check for auth-service-replica-1 failed
2026-06-08 09:07:00.112 [error] 40#40: *88201 upstream timed out (110: Connection timed out) while connecting to upstream, client: 172.54.12.8, server: kong, request: "POST /api/v1/auth/login HTTP/2.0", upstream: "http://10.244.2.14:8080/login"
2026-06-08 09:07:05.412 [error] 40#40: *88204 upstream timed out (110: Connection timed out) while connecting to upstream, client: 172.54.12.19, request: "POST /api/v1/auth/refresh HTTP/2.0"
2026-06-08 09:10:11.902 [alert] Gateway latency average exceeded threshold (5000ms) - current: 30005ms`
    },
    timelineAnalysis: {
      sequence: [
        { time: "09:05:00", event: "Auth Service pod CPU and RAM climb to 100% and crashes under peak load.", type: "warning" },
        { time: "09:07:12", event: "Kong API Gateway reports upstream connection timeouts for `/api/v1/auth`.", type: "critical" },
        { time: "09:10:00", event: "Gateway 504 Timeout rate spikes to 18%, affecting all inbound authentication requests.", type: "critical" },
        { time: "09:12:00", event: "PagerDuty alert triggers for Edge Gateway Health.", type: "info" }
      ],
      duration: "25 minutes",
      triggerType: "Config Change"
    },
    gitAnalysis: {
      riskyCodeChanges: [
        {
          file: "kong/gateway.conf",
          line: 88,
          change: "Increased HTTP keepalive timeout from 5s to 300s, preventing worker connection reuse.",
          severity: "MEDIUM"
        }
      ],
      commitHash: "cc84120a",
      author: "s.admin@smartops.ai",
      diff: `diff --git a/kong/gateway.conf b/kong/gateway.conf
index b918c2e..dd8172c 100644
--- a/kong/gateway.conf
+++ b/kong/gateway.conf
@@ -87,3 +87,3 @@
 proxy_connect_timeout 5s;
-proxy_read_timeout 5s;
-keepalive_timeout 5s;
+proxy_read_timeout 30s;
+keepalive_timeout 300s; # Risky Change: extremely high keepalive time under load`
    },
    riskAssessment: {
      score: 81,
      severity: "HIGH",
      confidence: "89%",
      riskFactors: [
        "Auth API service reporting 0 healthy replicas",
        "Edge gateway connection limits saturated",
        "Average response latency spiked to 30s"
      ]
    },
    aiRecommendations: [
      "Revert gateway.conf keepalive_timeout back to 5s to release stalled connections.",
      "Restart the auth-service Kubernetes deployment to replace dead pods.",
      "Configure a rate limiter on /api/v1/auth/login to protect downstream auth from brute force spikes."
    ],
    rcaReport: {
      executiveSummary: "Our API Gateway began serving HTTP 504 Gateway Timeouts to clients trying to reach authentication endpoints. Users were unable to log in, affecting approximately 3,100 active sessions.",
      rootCause: "The authentication service backend failed under peak traffic load. Meanwhile, a recent gateway configuration change that set the keepalive timeout to 300 seconds caused the gateway to hold onto stale connection slots, exhausting file descriptors on Kong nodes.",
      businessImpact: "Authentication services were offline for 25 minutes. 3,100 active users logged out; partner API integrations failed.",
      correctiveActions: [
        "Rebooted Kong gateway worker instances.",
        "Scaled auth-service pods to 5 replicas manually."
      ],
      preventiveActions: [
        "Revert proxy keepalive and read timeouts to conservative levels.",
        "Implement circuit breaking in Kong that redirects to a custom 'Auth Service Temporarily Unavailable' message when downstream health fails."
      ]
    },
    copilotQas: {
      "Why did this incident happen?": "The auth-service crashed, and Kong API Gateway was configured with a long 300-second keepalive timeout. As client requests poured in, the gateway kept connections open waiting for the crashed downstream server, exhausting Nginx connection workers and returning 504 timeouts to everyone.",
      "What failed first?": "The downstream auth-service pod replica crashed first due to CPU starvation and memory allocation failure.",
      "How can this be prevented?": "By adding an active health check with a circuit breaker in the gateway config. When auth-service goes down, Kong should fail immediately rather than waiting for timeouts, preserving connection slots.",
      "Which code change caused the issue?": "Commit cc84120a in `kong/gateway.conf`, which increased the `keepalive_timeout` to 300s and `proxy_read_timeout` to 30s."
    }
  },
  {
    id: "INC-3093",
    name: "INC-3093: NullPointer on User Authentication",
    shortName: "Auth NullPointer Exception",
    severity: "CRITICAL",
    status: "RESOLVED",
    time: "2026-06-07 18:45:00",
    riskScore: 95,
    errorCount: 4501,
    category: "Code Error",
    activeUsersAffected: 2200,
    impactScore: 9.8,
    logAnalysis: {
      rootCause: "NullPointerException in user profile resolver service due to missing null validation on legacy user preference rows in database.",
      errorPatterns: [
        "java.lang.NullPointerException: Cannot invoke 'UserPreferences.getTheme()' because 'prefs' is null",
        "at com.smartops.auth.UserProfileResolver.resolvePreferences(UserProfileResolver.java:54)"
      ],
      errorCount: 4501,
      rawLogs: `2026-06-07 18:40:02.124 INFO  [com.smartops.deploy] - Deploying version v1.92.3 to production canary (5%)
2026-06-07 18:41:15.912 ERROR [com.smartops.auth.AuthController] - Exception in authentication handler for user ID 10928
java.lang.NullPointerException: Cannot invoke "com.smartops.auth.UserPreferences.getTheme()" because the return value of "com.smartops.auth.UserProfile.getPreferences()" is null
  at com.smartops.auth.UserProfileResolver.resolvePreferences(UserProfileResolver.java:54) ~[classes/:na]
  at com.smartops.auth.UserProfileResolver.resolveProfile(UserProfileResolver.java:32) ~[classes/:na]
  at com.smartops.auth.AuthController.authenticate(AuthController.java:82) ~[classes/:na]
2026-06-07 18:42:01.002 ERROR [com.smartops.auth.AuthController] - Exception in authentication handler for user ID 10492`
    },
    timelineAnalysis: {
      sequence: [
        { time: "18:40:00", event: "CI/CD Pipeline: Production release v1.92.3 deployed to the canary cluster (5% traffic).", type: "info" },
        { time: "18:41:15", event: "Webapp: Sudden explosion of NullPointerExceptions on the authentication and login routes.", type: "critical" },
        { time: "18:43:00", event: "SmartOps Agent: Automated rollback rule triggered as Canary error rate crosses 5% threshold.", type: "info" },
        { time: "18:45:00", event: "CI/CD Pipeline: Rollback to v1.92.2 complete. Error rate returns to baseline (0%).", type: "info" }
      ],
      duration: "5 minutes",
      triggerType: "Deployment"
    },
    gitAnalysis: {
      riskyCodeChanges: [
        {
          file: "src/main/java/com/smartops/auth/UserProfileResolver.java",
          line: 54,
          change: "Refactored user preferences loader to load lazily without validating null checks on historical database rows.",
          severity: "HIGH"
        }
      ],
      commitHash: "a991f8b2",
      author: "d.developer@smartops.ai",
      diff: `diff --git a/src/main/java/com/smartops/auth/UserProfileResolver.java b/src/main/java/com/smartops/auth/UserProfileResolver.java
index a1289cf..b8291a2 100644
--- a/src/main/java/com/smartops/auth/UserProfileResolver.java
+++ b/src/main/java/com/smartops/auth/UserProfileResolver.java
@@ -52,3 +52,7 @@ public class UserProfileResolver {
     UserProfile profile = db.loadProfile(userId);
-    UserPreferences prefs = profile.getPreferences();
-    return prefs.getTheme(); // Risky: Throws NPE if user has never saved preferences
+    UserPreferences prefs = profile.getPreferences();
+    if (prefs == null) {
+        return "dark"; // Fixed locally, but deployed file had no null check
+    }
+    return prefs.getTheme();`
    },
    riskAssessment: {
      score: 95,
      severity: "CRITICAL",
      confidence: "99%",
      riskFactors: [
        "Canary user authentication success rate dropped to 0%",
        "Regression introduced in core authentication package",
        "NullPointer exceptions thrown on main login path"
      ]
    },
    aiRecommendations: [
      "Keep application at rolled-back version v1.92.2 until bug is patched.",
      "Add a defensive null-check on UserPreferences in `UserProfileResolver.java:54`.",
      "Add a database migration script to backfill empty preference records for legacy users."
    ],
    rcaReport: {
      executiveSummary: "A minor release (v1.92.3) caused 100% login failure rates for legacy users within the canary release slot (5% of users). The system automatically rolled back within 5 minutes.",
      rootCause: "The new code refactored how user preference profiles were initialized. Legacy database records did not have preference records created, causing `profile.getPreferences()` to return `null`. The code attempted to call `.getTheme()` on this null reference.",
      businessImpact: "Affected 2,200 users during active canary test. Zero login capabilities for those users for 5 minutes. No database data loss.",
      correctiveActions: [
        "Automated deployment rollback by Kubernetes cluster alert controller.",
        "Created hotfix pull request with defensive null checks."
      ],
      preventiveActions: [
        "Enforce strict nullability assertions in the Java compiler (like @NonNull annotations).",
        "Write integration tests that load mock accounts simulating accounts created in older version iterations."
      ]
    },
    copilotQas: {
      "Why did this incident happen?": "The service attempted to fetch the theme preference from the user's settings. However, older user accounts did not have user preferences initialized in the database, meaning the resolver loaded a null object and tried to call a method on it.",
      "What failed first?": "The Java method `UserProfileResolver.resolvePreferences` threw a Java NullPointerException during login authentication.",
      "How can this be prevented?": "Enforce static analysis null-checking (e.g. FindBugs/Lombok/@Nullable annotations) and ensure you default to fallback objects when optional DB rows are missing.",
      "Which code change caused the issue?": "Commit a991f8b2 in `UserProfileResolver.java`, where line 54 was modified to read `return prefs.getTheme();` without a preceding `prefs != null` assertion."
    }
  },
  {
    id: "INC-3094",
    name: "INC-3094: WebSocket Service OOM Out of Memory",
    shortName: "WebSocket Service OOM",
    severity: "HIGH",
    status: "INVESTIGATING",
    time: "2026-06-07 04:00:00",
    riskScore: 78,
    errorCount: 125,
    category: "Infrastructure",
    activeUsersAffected: 950,
    impactScore: 7.2,
    logAnalysis: {
      rootCause: "Memory leak in WebSocket server connection handlers. Global event listeners were not removed when client connections closed, causing GC to retain sockets.",
      errorPatterns: [
        "FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory",
        "Process exited with code 137 (OOM Killed)"
      ],
      errorCount: 125,
      rawLogs: `2026-06-07 03:00:00.102 INFO  [com.smartops.ws] - Memory usage: heapUsed=1.21 GB, activeConnections=4100
2026-06-07 03:30:00.115 INFO  [com.smartops.ws] - Memory usage: heapUsed=1.65 GB, activeConnections=3900
2026-06-07 03:55:00.902 ERROR [com.smartops.ws] - FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory
2026-06-07 04:00:01.002 SYSTEM - Container ws-service-pod-2 crashed. Exit code: 137 (OOMKilled)
2026-06-07 04:00:15.112 SYSTEM - Kubelet restarted ws-service-pod-2. Memory usage cleared to 120MB.`
    },
    timelineAnalysis: {
      sequence: [
        { time: "22:00:00", event: "Websocket Server: Memory usage begins climbing linearly at a rate of 150MB per hour, regardless of steady connections.", type: "warning" },
        { time: "03:45:00", event: "Node.js VM: Enters garbage collection thrashing state. Latency increases for real-time alerts.", type: "warning" },
        { time: "04:00:00", event: "Kubernetes Daemon: Detects pod memory limit breaches. Pod is forcefully terminated (OOM Killed).", type: "critical" }
      ],
      duration: "6 hours",
      triggerType: "Memory Leak"
    },
    gitAnalysis: {
      riskyCodeChanges: [
        {
          file: "src/services/socketManager.js",
          line: 42,
          change: "Added a global process level IPC listener inside the ws socket handler without cleaning it up on close.",
          severity: "HIGH"
        }
      ],
      commitHash: "ws9823c1",
      author: "a.smart@smartops.ai",
      diff: `diff --git a/src/services/socketManager.js b/src/services/socketManager.js
index c892182..a99281a 100644
--- a/src/services/socketManager.js
+++ b/src/services/socketManager.js
@@ -40,3 +40,7 @@
   ws.on('message', (msg) => {
-    process.on('message', (ipcMsg) => ws.send(JSON.stringify(ipcMsg))); // Risky: adds a new global process listener per socket connection
+    const ipcHandler = (ipcMsg) => ws.send(JSON.stringify(ipcMsg));
+    process.on('message', ipcHandler);
+    
+    ws.on('close', () => {
+      // Missing: process.off('message', ipcHandler) to prevent socket reference from being held in memory
+    });
   });`
    },
    riskAssessment: {
      score: 78,
      severity: "HIGH",
      confidence: "91%",
      riskFactors: [
        "Memory leak slope is strictly positive (+150MB/h)",
        "Kubernetes container crash loop warning",
        "Intermittent disconnection of active web socket terminals"
      ]
    },
    aiRecommendations: [
      "Modify socketManager.js to unregister the IPC listener on socket close.",
      "Configure WebSocket memory thresholds and setup automated container restarts during off-peak hours.",
      "Add Jest/Mocha heapdump testing to check for memory leaks in PR pipeline."
    ],
    rcaReport: {
      executiveSummary: "Our notification system's WebSocket pods suffered recurring Out-Of-Memory (OOM) crashes every 6 hours, disconnecting active dashboard users and delaying message delivery.",
      rootCause: "A global process listener (`process.on('message')`) was being registered for every client socket connection to push internal events. However, when a client disconnected, the application did not unregister this listener. The global `process` object held references to each closed socket context, causing a severe memory leak.",
      businessImpact: "Real-time alerts were delayed by up to 10 minutes. Dashboard widgets failed to update dynamically for 950 users.",
      correctiveActions: [
        "Patched the socket manager code to properly run `process.off` when sockets close.",
        "Set Kubernetes pod memory limits dynamically from 2GB to 3GB as a temporary buffer."
      ],
      preventiveActions: [
        "Enforce memory leak verification checks in staging environment.",
        "Avoid using global process event listeners per-socket connection; use dedicated EventEmitter classes with clean life cycles."
      ]
    },
    copilotQas: {
      "Why did this incident happen?": "The WebSocket server registered a global `process.on('message')` listener for every active socket connection. When sockets disconnected, the listener was not cleaned up. Because the global `process` object exists for the lifetime of the application, it retained references to the closed socket objects, preventing the Node.js garbage collector from reclaiming that memory.",
      "What failed first?": "The Node.js V8 engine ran out of heap space, which triggered an absolute crash, resulting in a Kubernetes Pod exit with status code 137 (OOMKilled).",
      "How can this be prevented?": "By adding clean-up logic on the socket `close` event: `process.off('message', ipcHandler)`. This detaches the reference, allowing the socket connection to be safely garbage-collected.",
      "Which code change caused the issue?": "Commit ws9823c1 in `src/services/socketManager.js` where the process messenger listener was added inside the WebSocket connection handler."
    }
  },
  {
    id: "INC-3095",
    name: "INC-3095: Payment Gateway API Service Outage",
    shortName: "Stripe API Outage",
    severity: "MEDIUM",
    status: "RESOLVED",
    time: "2026-06-06 14:10:00",
    riskScore: 65,
    errorCount: 512,
    category: "External Service",
    activeUsersAffected: 312,
    impactScore: 6.0,
    logAnalysis: {
      rootCause: "Third-party credit card processor (Stripe) suffered an API outage in US-East-1 region, resulting in network connection drops on outbound payment requests.",
      errorPatterns: [
        "StripeConnectionError: Connection to Stripe API failed.",
        "API Gateway checkout call received 502 Bad Gateway from payment upstream"
      ],
      errorCount: 512,
      rawLogs: `2026-06-06 14:00:12.441 INFO  [com.smartops.billing] - Initiating Stripe payment intent for $89.00
2026-06-06 14:00:32.449 ERROR [com.smartops.billing] - Stripe API connection timed out after 20000ms.
com.stripe.exception.PermissionException: Connection to Stripe API failed.
  at com.stripe.net.HttpClient.sendRequest(HttpClient.java:84) ~[stripe-java-24.1.0.jar:na]
  at com.stripe.net.StripeResponseGetter.request(StripeResponseGetter.java:102) ~[stripe-java-24.1.0.jar:na]
2026-06-06 14:01:05.112 ERROR [com.smartops.billing] - Stripe API connection timed out. Status: 502 Bad Gateway`
    },
    timelineAnalysis: {
      sequence: [
        { time: "14:00:00", event: "Checkout: Server requests to Stripe API endpoints begin returning 502 Bad Gateway timeouts.", type: "warning" },
        { time: "14:02:15", event: "Alert Manager: Alarm triggers for billing error threshold (>3% checkout failure rate).", type: "warning" },
        { time: "14:05:00", event: "Customer Support: Large influx of tickets reporting credit card payment failures.", type: "warning" },
        { time: "14:10:00", event: "Billing Service: Operator flips feature flag to reroute transactions to backup provider Adyen.", type: "info" }
      ],
      duration: "10 minutes",
      triggerType: "Third-Party Outage"
    },
    gitAnalysis: {
      riskyCodeChanges: [],
      commitHash: "N/A",
      author: "N/A",
      diff: `No local repository changes detected.
This incident is attributed to external Stripe API availability degradation.`
    },
    riskAssessment: {
      score: 65,
      severity: "MEDIUM",
      confidence: "98%",
      riskFactors: [
        "External payment service returned 502 error",
        "Zero modifications in recent codebase releases",
        "Stripe Status page reports major outage in billing api"
      ]
    },
    aiRecommendations: [
      "Verify Stripe API health returns to normal status before reverting payment router settings.",
      "Implement automatic circuit breaking in checkout endpoints to auto-toggle payment providers on API timeouts.",
      "Provide clean diagnostic warnings on UI checkout page when Stripe is down, prompting user with alternative payment methods."
    ],
    rcaReport: {
      executiveSummary: "Stripe API server errors blocked credit card payments on our site for 10 minutes. Billing was restored by manually routing traffic to Adyen.",
      rootCause: "Stripe's payment endpoint experienced an outage in their US-East-1 AWS hosting facilities. Connection requests timed out.",
      businessImpact: "Blocked billing paths for 312 checkout attempts. Zero permanent data discrepancies. 100% of transactions restored once the fallback was activated.",
      correctiveActions: [
        "Manually updated payment router settings to use Adyen gateway.",
        "Notified billing teams of reconciliation steps for pending tokens."
      ],
      preventiveActions: [
        "Implement automated circuit breakers to switch gateways without manual operator action.",
        "Add billing queue alerts for payment retry handlers."
      ]
    },
    copilotQas: {
      "Why did this incident happen?": "The incident occurred due to an external service outage at Stripe, our primary payment processor, which resulted in 502 Bad Gateway errors for all API callouts.",
      "What failed first?": "Our HTTP client connection calls to Stripe APIs failed.",
      "How can this be prevented?": "We can prevent this from causing downtime by programming an automatic fallback billing switch that transfers traffic to Adyen if Stripe failures exceed a 5% limit in 1 minute.",
      "Which code change caused the issue?": "None. The incident was external, and there were no local git changes or configurations deployed during this timeframe."
    }
  }
];

// Helper variables for Recharts dashboard analytics
export const severityData = [
  { name: 'Critical', value: 2, color: '#f43f5e' },
  { name: 'High', value: 2, color: '#f59e0b' },
  { name: 'Medium', value: 1, color: '#10b981' }
];

export const errorFrequencyData = [
  { time: '08:00', 'DB Timeout': 5, 'API Gateway': 12, 'Deployment': 0, 'OOM Leak': 10 },
  { time: '09:00', 'DB Timeout': 15, 'API Gateway': 120, 'Deployment': 0, 'OOM Leak': 12 },
  { time: '10:00', 'DB Timeout': 25, 'API Gateway': 820, 'Deployment': 0, 'OOM Leak': 14 },
  { time: '11:00', 'DB Timeout': 110, 'API Gateway': 30, 'Deployment': 4, 'OOM Leak': 15 },
  { time: '12:00', 'DB Timeout': 2405, 'API Gateway': 5, 'Deployment': 15, 'OOM Leak': 16 },
  { time: '13:00', 'DB Timeout': 180, 'API Gateway': 4, 'Deployment': 4501, 'OOM Leak': 18 }
];

export const timelineData = [
  { day: 'Mon', incidents: 1 },
  { day: 'Tue', incidents: 3 },
  { day: 'Wed', incidents: 2 },
  { day: 'Thu', incidents: 4 },
  { day: 'Fri', incidents: 5 },
  { day: 'Sat', incidents: 2 },
  { day: 'Sun', incidents: 6 }
];

export const riskScoreDistribution = [
  { range: '0-20', count: 12 },
  { range: '21-40', count: 35 },
  { range: '41-60', count: 78 },
  { range: '61-80', count: 42 },
  { range: '81-100', count: 5 } // 5 active incidents fall in this top risk bracket
];
