import React from 'react';
import { ShieldAlert, AlertCircle, FileCheck2 } from 'lucide-react';

const Recommendations = ({ incident }) => {
  if (!incident) return null;

  // Map recommendations dynamically based on incident type
  const getRemediationTimeline = (incId) => {
    // If the incident has real backend-generated AI recommendations, use them dynamically
    if (incident.aiRecommendations && incident.aiRecommendations.length > 0) {
      const immediate = [];
      const shortTerm = [];
      const longTerm = [];
      
      incident.aiRecommendations.forEach(rec => {
        const actionStr = typeof rec === 'object' 
          ? `${rec.action || rec.description || ''}${rec.impact ? ` (Impact: ${rec.impact})` : ''}`
          : rec;
        
        const priority = typeof rec === 'object' ? (rec.priority || '').toUpperCase() : '';
        
        if (priority.includes('IMMEDIATE') || priority.includes('CRITICAL')) {
          immediate.push(actionStr);
        } else if (priority.includes('SHORT') || priority.includes('MEDIUM') || priority.includes('SEV')) {
          shortTerm.push(actionStr);
        } else {
          longTerm.push(actionStr);
        }
      });
      
      // Handle cases where categorization might be uneven
      if (immediate.length > 0 || shortTerm.length > 0 || longTerm.length > 0) {
        return {
          immediate: immediate.length > 0 ? immediate : ["Investigate immediate trace logs and metrics."],
          shortTerm: shortTerm.length > 0 ? shortTerm : ["Configure automated alerts and unit tests."],
          longTerm: longTerm.length > 0 ? longTerm : ["Conduct post-mortem and optimize resources."]
        };
      }
    }

    switch (incId) {
      case 'INC-3091': // DB Connection pool
        return {
          immediate: ["Terminate blocked PostgreSQL process connection threads manually.", "Roll back OrderService checkout deployment tag to version v2.4.0."],
          shortTerm: ["Add composite index idx_orders_user_status: `CREATE INDEX CONCURRENTLY idx_orders_user_status ON orders(user_id, status);`", "Set query timeout threshold limit in Hikari pool configuration to 5000ms."],
          longTerm: ["Refactor OrderService.js query-in-loop code to batch query load orders via SQL 'IN' operator.", "Set static analysis rules (ESLint or SonarQube) to block N+1 query loop commits in CI/CD pipeline."]
        };
      case 'INC-3092': // Kong Gateway 504
        return {
          immediate: ["Reboot Kong API Gateway worker nodes.", "Manually scale auth-service container pods to 5 minimum replicas."],
          shortTerm: ["Revert gateway.conf keepalive_timeout configuration back to 5s.", "Configure authentication login route rate limiter (limit to 100 req/min per IP)."],
          longTerm: ["Implement active gateway health monitoring with automated replica scaling.", "Add an upstream circuit breaker to Kong config returning direct 503 fallback state when downstream is dead."]
        };
      case 'INC-3093': // Auth NullPointer
        return {
          immediate: ["Roll back production User Authentication service to v1.92.2."],
          shortTerm: ["Apply nullability checks in UserProfileResolver.java:54 (`if (prefs == null) return Theme.DARK;`).", "Deploy database migration to backfill default preference records for legacy users."],
          longTerm: ["Configure strict @NonNull annotation compliance checks in Gradle/Maven compilation.", "Write unit tests simulating historical user schemas to detect null references early."]
        };
      case 'INC-3094': // WebSocket OOM
        return {
          immediate: ["Run shell script to recycle leaked WebSocket container nodes.", "Increase Kubernetes pod RAM allocation from 2GB to 3GB temporarily."],
          shortTerm: ["Patch socketManager.js connection handlers to properly call `process.off('message')` when connection ends.", "Setup Node.js heapdump inspector in development clusters."],
          longTerm: ["Avoid global process message emitters for single socket sessions; migrate to a scoped EventBus.", "Add automated memory limit slope alarms to trigger when container RAM rises linearly for >2 hours."]
        };
      case 'INC-3095': // Stripe API Outage
        return {
          immediate: ["Trigger billing router configuration toggle to bypass Stripe and route checkouts to Adyen backup."],
          shortTerm: ["Set client checkout frontend alerts notifying users of Stripe regional outage.", "Verify local pending invoices matching Webhook sync dates."],
          longTerm: ["Implement automated billing router circuit breakers that auto-switch to Adyen when Stripe error rate exceeds 5%.", "Configure a fallback payment token queue to safely retry delayed stripe charges upon provider recovery."]
        };
      default: // Uploaded custom incidents
        return {
          immediate: ["Review socket timeout variables and connection settings in logs.", "Restart gateway routing adapters."],
          shortTerm: ["Reduce timeout parameters in adapter configurations back to default 5000ms.", "Compare API records from uploaded CSV logs with live load balancer latencies."],
          longTerm: ["Integrate automated unit tests for configuration timeouts.", "Establish telemetry monitors tracking socket counts in staging."]
        };
    }
  };

  const timeline = getRemediationTimeline(incident.id);

  return (
    <div className="space-y-6 text-left">
      <h4 className="text-sm font-bold text-gray-200 uppercase tracking-wider font-mono">
        Remediation Action Plan
      </h4>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Immediate Action */}
        <div className="p-5 rounded-xl bg-rose-500/5 border border-rose-500/15 space-y-4">
          <div className="flex items-center gap-2 text-rose-400 font-mono font-bold text-xs uppercase border-b border-rose-500/10 pb-2.5">
            <ShieldAlert className="w-4.5 h-4.5 animate-pulse-slow" />
            <span>Immediate Actions</span>
          </div>
          <ul className="space-y-2.5 text-xs text-gray-300">
            {timeline.immediate.map((item, idx) => (
              <li key={idx} className="flex gap-2 items-start leading-relaxed">
                <span className="text-rose-400 font-bold shrink-0 mt-0.5">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Short-Term Action */}
        <div className="p-5 rounded-xl bg-amber-500/5 border border-amber-500/15 space-y-4">
          <div className="flex items-center gap-2 text-amber-400 font-mono font-bold text-xs uppercase border-b border-amber-500/10 pb-2.5">
            <AlertCircle className="w-4.5 h-4.5" />
            <span>Short-Term Actions</span>
          </div>
          <ul className="space-y-2.5 text-xs text-gray-300">
            {timeline.shortTerm.map((item, idx) => (
              <li key={idx} className="flex gap-2 items-start leading-relaxed">
                <span className="text-amber-400 font-bold shrink-0 mt-0.5">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Long-Term Action */}
        <div className="p-5 rounded-xl bg-emerald-500/5 border border-emerald-500/15 space-y-4">
          <div className="flex items-center gap-2 text-emerald-400 font-mono font-bold text-xs uppercase border-b border-emerald-500/10 pb-2.5">
            <FileCheck2 className="w-4.5 h-4.5" />
            <span>Long-Term Actions</span>
          </div>
          <ul className="space-y-2.5 text-xs text-gray-300">
            {timeline.longTerm.map((item, idx) => (
              <li key={idx} className="flex gap-2 items-start leading-relaxed">
                <span className="text-emerald-400 font-bold shrink-0 mt-0.5">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>
    </div>
  );
};

export default Recommendations;
