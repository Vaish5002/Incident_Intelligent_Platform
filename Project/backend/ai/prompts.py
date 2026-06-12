"""
Prompt Templates for Groq AI
"""

RCA_GENERATION_PROMPT = """You are an expert Site Reliability Engineer (SRE) and incident analyst. Analyze the following production incident and generate a comprehensive Root Cause Analysis (RCA).

## Incident Information

**Incident Description:**
{incident_description}

**Severity:** {severity}
**Affected Service:** {affected_service}
**Risk Score:** {risk_score}/100

## Technical Data

### GitHub Analysis
{github_analysis}

### Log Analysis
{log_analysis}

### Timeline of Events
{timeline}

### Root Cause Candidates (Pre-analyzed)
{root_cause_candidates}

## Similar Past Incidents (if available)
{similar_incidents}

## Your Task

Generate a detailed Root Cause Analysis with the following sections:

1. **Executive Summary** (2-3 sentences)
   - What happened, when, and impact

2. **Root Cause** (Detailed explanation)
   - Primary cause of the incident
   - Why it happened
   - Technical details

3. **Contributing Factors** (if any)
   - Secondary issues that amplified the problem

4. **Impact Assessment**
   - User impact
   - Business impact
   - System impact

5. **Timeline Narrative**
   - Clear chronological story of what happened

6. **Immediate Actions Taken** (if mentioned in data)
   - What was done to resolve

7. **Recommendations**
   - **Immediate:** Quick fixes to prevent recurrence (next 24 hours)
   - **Short-term:** Tactical improvements (next 1-2 weeks)
   - **Long-term:** Strategic changes (next 1-3 months)

8. **Prevention Measures**
   - Monitoring improvements
   - Code/config changes
   - Process improvements

9. **Lessons Learned**
   - Key takeaways for the team

## Output Format

Please provide your analysis in a clear, structured markdown format. Be specific, technical, and actionable.

Focus on being:
- **Accurate:** Based on the data provided
- **Actionable:** Provide concrete next steps
- **Clear:** Easy for both technical and non-technical stakeholders
- **Comprehensive:** Cover all important aspects
"""


QUICK_RCA_PROMPT = """Analyze this incident and provide a quick RCA summary:

**Incident:** {incident_description}
**Logs:** {log_summary}
**Timeline:** {timeline_summary}

Provide:
1. Root Cause (1-2 sentences)
2. Top 3 Immediate Actions
3. Risk Level (Low/Medium/High/Critical)

Keep it concise and actionable.
"""


RECOMMENDATION_PROMPT = """Based on this incident analysis, generate specific recommendations:

**Root Cause:** {root_cause}
**Severity:** {severity}
**Affected Service:** {affected_service}

Provide:
1. **Immediate Actions** (0-24 hours) - Quick wins
2. **Short-term Fixes** (1-2 weeks) - Tactical improvements
3. **Long-term Strategy** (1-3 months) - Strategic changes

Each recommendation should include:
- Action description
- Priority (P0/P1/P2)
- Estimated effort
- Expected impact

Format as JSON array.
"""


SIMILAR_INCIDENT_ANALYSIS_PROMPT = """Compare this current incident with similar past incidents:

**Current Incident:**
{current_incident}

**Similar Past Incidents:**
{past_incidents}

Analysis required:
1. What patterns do you see?
2. Were past solutions effective?
3. Are there recurring systemic issues?
4. What can we learn from past incidents?

Provide insights that help prevent future occurrences.
"""


PREVENTION_STRATEGY_PROMPT = """Based on this incident, create a prevention strategy:

**Root Cause:** {root_cause}
**Service:** {affected_service}
**Recurrence Risk:** {risk_score}/100

Generate:
1. **Monitoring Improvements**
   - What metrics to track
   - Alert thresholds
   - Dashboard widgets

2. **Code/Infrastructure Changes**
   - Configuration improvements
   - Code patterns to adopt
   - Infrastructure hardening

3. **Process Improvements**
   - Code review focus areas
   - Deployment checklist updates
   - Incident response improvements

4. **Testing Enhancements**
   - Test scenarios to add
   - Load testing considerations
   - Chaos engineering experiments

Be specific and actionable.
"""


def build_rca_prompt(
    incident_description: str,
    severity: str,
    affected_service: str,
    risk_score: float,
    github_analysis: str,
    log_analysis: str,
    timeline: str,
    root_cause_candidates: str,
    similar_incidents: str = "No similar incidents found."
) -> str:
    """Build the complete RCA generation prompt"""
    
    return RCA_GENERATION_PROMPT.format(
        incident_description=incident_description,
        severity=severity,
        affected_service=affected_service,
        risk_score=risk_score,
        github_analysis=github_analysis,
        log_analysis=log_analysis,
        timeline=timeline,
        root_cause_candidates=root_cause_candidates,
        similar_incidents=similar_incidents
    )


def build_quick_rca_prompt(
    incident_description: str,
    log_summary: str,
    timeline_summary: str
) -> str:
    """Build quick RCA prompt for fast analysis"""
    
    return QUICK_RCA_PROMPT.format(
        incident_description=incident_description,
        log_summary=log_summary,
        timeline_summary=timeline_summary
    )
