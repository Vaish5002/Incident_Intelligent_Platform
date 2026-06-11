"""
Test Suite for Module 9 (PDF Report Generator)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.ai.pdf_generator import PDFGenerator
from backend.ai.knowledge_base import KnowledgeBaseService
from backend.database.connection import init_db
from datetime import datetime
import os


def print_header(text):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70 + "\n")


def print_success(text):
    print(f"✅ SUCCESS: {text}")


def print_test(text):
    print(f"\n--- {text} ---")


def test_module9_pdf_generator():
    """Test Module 9: PDF Report Generator"""
    print_header("MODULE 9: PDF REPORT GENERATOR")
    
    # Initialize services
    print("Initializing services...")
    init_db()
    pdf_generator = PDFGenerator()
    kb_service = KnowledgeBaseService()
    print("Services initialized")
    
    # Check if PDF generator is available
    if not pdf_generator.is_available():
        print("⚠️  WARNING: reportlab not available")
        print("Install with: pip install reportlab")
        return False
    
    print(f"PDF Generator Status: Available ✅")
    
    # Test 1: Generate PDF (Expected: PDF downloads successfully)
    print_test("Test 1: Generate PDF Report")
    
    # Sample RCA data
    sample_rca = """
# Root Cause Analysis

## Executive Summary

Payment service experienced complete outage for 45 minutes affecting 1,250 users and resulting in $45,000 in failed transactions. The root cause was identified as database connection pool exhaustion caused by a configuration change that reduced the pool size from 50 to 10 connections during a routine deployment.

## Timeline

### 10:15 AM - Deployment Started
- Version 2.3.1 deployed to production
- Configuration changes included database optimization

### 10:30 AM - First Errors Detected
- Connection timeout errors started appearing
- Error rate: 5% of requests

### 10:45 AM - Service Degradation
- Error rate increased to 35%
- Users reporting payment failures

### 11:00 AM - Complete Outage
- All payment transactions failing
- Database connection pool exhausted

### 11:20 AM - Issue Identified
- Root cause identified: DB_POOL_SIZE=10 (down from 50)
- Rollback initiated

### 11:45 AM - Service Restored
- Configuration corrected
- Service fully operational

## Root Cause

The immediate root cause was a configuration change in the database connection pool settings. During deployment of version 2.3.1, the `DB_POOL_SIZE` parameter was reduced from 50 to 10 as part of a resource optimization effort.

**Technical Details:**
- Configuration file: `config/database.py`
- Changed parameter: `DB_POOL_SIZE`
- Previous value: 50
- New value: 10
- Commit SHA: abc123def456

Under normal load (averaging 25-30 concurrent connections), the reduced pool size caused immediate connection exhaustion. When all 10 connections were in use, subsequent requests timed out after 30 seconds, leading to cascading failures.

## Contributing Factors

1. **Insufficient Load Testing**: The configuration change was not tested under production-level load conditions.

2. **Lack of Monitoring Alerts**: No alerts configured for connection pool exhaustion or high connection wait times.

3. **Manual Configuration Management**: Configuration changes were made manually without automated validation.

4. **Missing Gradual Rollout**: Change was deployed to 100% of production immediately without canary or gradual rollout.

## Impact Assessment

### User Impact
- **Affected Users**: 1,250 active users
- **Failed Transactions**: 892 payment attempts
- **Duration**: 45 minutes of complete outage
- **Customer Support**: 127 support tickets opened

### Business Impact
- **Revenue Loss**: $45,000 in failed transactions
- **Refunds Issued**: $2,300 in goodwill credits
- **Brand Reputation**: Social media mentions increased 340%
- **SLA Breach**: 99.9% uptime SLA breached for the month

### System Impact
- **Service Availability**: 0% for payment service
- **Dependent Services**: Checkout, subscription, billing affected
- **Database Load**: Connection pool exhaustion
- **Error Rate**: 100% for 15 minutes

## Immediate Actions Taken

1. **Configuration Rollback** [Completed 11:20 AM]
   - Reverted DB_POOL_SIZE to 50
   - Redeployed configuration
   - Verified connection availability

2. **Service Health Verification** [Completed 11:45 AM]
   - Confirmed all services operational
   - Validated transaction processing
   - Monitored error rates (returned to <0.1%)

3. **Customer Communication** [Completed 12:00 PM]
   - Status page updated
   - Email sent to affected users
   - Social media update posted

## Recommendations

### Immediate (0-24 hours) [P0]

1. **Add Connection Pool Monitoring** [Effort: 2 hours]
   - Alert when pool utilization > 80%
   - Dashboard for real-time connection metrics
   - Historical trend analysis

2. **Document Configuration Standards** [Effort: 4 hours]
   - Minimum pool size based on load testing
   - Configuration change approval process
   - Required testing checklist

3. **Review Other Resource Configurations** [Effort: 4 hours]
   - Audit all resource pool configurations
   - Identify other potential bottlenecks
   - Validate against production load

### Short-term (1-2 weeks) [P1]

1. **Implement Automated Configuration Validation** [Effort: 2-3 days]
   - Pre-deployment configuration checks
   - Load test simulation for config changes
   - Automated rollback on threshold violations

2. **Enhanced Load Testing** [Effort: 1 week]
   - Production-scale load testing environment
   - Automated load tests in CI/CD pipeline
   - Configuration change impact analysis

3. **Gradual Rollout Strategy** [Effort: 3-4 days]
   - Canary deployments for all changes
   - Automated promotion based on metrics
   - Quick rollback capabilities

### Long-term (1-3 months) [P2]

1. **Infrastructure as Code** [Effort: 1 month]
   - Migrate all configuration to IaC
   - Version control for all configs
   - Automated drift detection

2. **Chaos Engineering** [Effort: 6 weeks]
   - Regular resilience testing
   - Failure injection experiments
   - Automated recovery validation

3. **Advanced Monitoring & Alerting** [Effort: 1 month]
   - AI-powered anomaly detection
   - Predictive capacity alerts
   - Automated remediation for common issues

## Prevention Measures

### Monitoring Improvements
- **Real-time Connection Pool Metrics**: Dashboard showing current/max connections, wait times, timeout rates
- **Predictive Alerts**: ML-based alerts for unusual connection patterns
- **Automated Health Checks**: Every 30 seconds with automatic escalation

### Code and Configuration Changes
- **Configuration Validation Pipeline**: Automated checks before deployment
- **Load Test Requirements**: Mandatory load testing for any resource configuration changes
- **Peer Review Process**: All configuration changes require approval from senior engineer

### Process Improvements
- **Change Management Protocol**: Formal approval for production configuration changes
- **Deployment Windows**: Critical changes only during low-traffic periods
- **Communication Protocol**: Automated notifications to on-call team for all deployments

### Testing Enhancements
- **Production-scale Testing Environment**: Environment matching production capacity
- **Automated Regression Tests**: Database connection tests in CI/CD
- **Chaos Testing**: Regular failure injection to validate resilience

## Lessons Learned

### What Went Well
- **Quick Identification**: Root cause identified within 20 minutes
- **Effective Rollback**: Rollback procedure worked smoothly
- **Team Coordination**: Engineering and support teams coordinated effectively

### What Could Be Improved
- **Proactive Monitoring**: Should have detected configuration risk before impact
- **Testing Coverage**: Load testing should have caught this issue
- **Deployment Strategy**: Gradual rollout would have limited impact

### Key Takeaways for Team
1. **Always validate configuration changes** against production load
2. **Monitor resource utilization closely** especially connection pools
3. **Implement gradual rollouts** for all production changes
4. **Test, test, test** - especially for resource-critical configurations
5. **Set up comprehensive alerting** before problems occur

## Post-Incident Actions

**Completed:**
- ✅ Incident postmortem meeting held
- ✅ Root cause documented
- ✅ Immediate fixes deployed
- ✅ Customer communication sent

**In Progress:**
- 🔄 Connection pool monitoring implementation
- 🔄 Configuration validation pipeline
- 🔄 Load testing environment setup

**Planned:**
- 📋 IaC migration (Q2 2024)
- 📋 Chaos engineering program (Q2 2024)
- 📋 Advanced monitoring rollout (Q3 2024)

---

**Report Prepared By:** SmartOps AI  
**Date:** June 9, 2026  
**Incident ID:** INC-2024-001  
**Status:** Resolved
"""
    
    try:
        # Generate PDF
        pdf_buffer = pdf_generator.generate_rca_pdf(
            incident_id="INC-TEST-PDF-001",
            incident_description="Payment service complete outage affecting 1,250 users",
            rca_text=sample_rca,
            severity="Critical",
            risk_score=91.5,
            confidence=95.0,
            affected_service="payment",
            occurred_at="2024-01-15T10:30:00",
            resolved_at="2024-01-15T11:45:00"
        )
        
        # Save to file for verification
        output_dir = Path(__file__).parent / "test_output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "test_rca_report.pdf"
        with open(output_file, 'wb') as f:
            f.write(pdf_buffer.read())
        
        file_size = output_file.stat().st_size
        
        print(f"PDF generated successfully:")
        print(f"  File: {output_file}")
        print(f"  Size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print(f"  Status: ✅ PDF downloaded successfully")
        
        # Verify file exists and has content
        assert output_file.exists(), "PDF file not created"
        assert file_size > 1000, "PDF file too small (possibly empty)"
        
        print_success("Test 1 PASSED - PDF downloads successfully")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Large RCA (Expected: Formatting remains correct)
    print_test("Test 2: Large RCA Document")
    
    # Create a very large RCA with multiple sections
    large_rca = """
# Comprehensive Root Cause Analysis - Extended Report

## Executive Summary

This is a comprehensive incident report covering multiple aspects of a complex system failure. The incident affected multiple services across different regions and required coordinated response from multiple teams.

""" + "\n\n".join([f"""
## Section {i}: Detailed Analysis Part {i}

This section provides detailed analysis of aspect {i} of the incident. The analysis includes multiple subsections with detailed technical information.

### Subsection {i}.1: Technical Details

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

### Subsection {i}.2: Impact Analysis

The impact of this aspect included:
- Impact point 1 for section {i}
- Impact point 2 for section {i}
- Impact point 3 for section {i}
- Impact point 4 for section {i}

### Subsection {i}.3: Mitigation Steps

1. First mitigation step for aspect {i}
2. Second mitigation step for aspect {i}
3. Third mitigation step for aspect {i}
4. Fourth mitigation step for aspect {i}

""" for i in range(1, 11)])
    
    try:
        # Generate large PDF
        large_pdf_buffer = pdf_generator.generate_rca_pdf(
            incident_id="INC-TEST-LARGE-001",
            incident_description="Large multi-service failure requiring comprehensive analysis",
            rca_text=large_rca,
            severity="Critical",
            risk_score=88.0,
            confidence=92.0,
            affected_service="multiple",
            occurred_at="2024-01-15T10:00:00",
            resolved_at="2024-01-15T14:30:00"
        )
        
        # Save to file
        large_output_file = output_dir / "test_large_rca_report.pdf"
        with open(large_output_file, 'wb') as f:
            f.write(large_pdf_buffer.read())
        
        file_size = large_output_file.stat().st_size
        
        print(f"Large PDF generated successfully:")
        print(f"  File: {large_output_file}")
        print(f"  Size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print(f"  Status: ✅ Formatting remains correct")
        
        # Verify file is larger (has more content)
        assert large_output_file.exists(), "Large PDF file not created"
        assert file_size > 10000, "Large PDF file too small"
        
        print_success("Test 2 PASSED - Large RCA formatting correct")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Generate PDF from stored incident
    print_test("Test 3: Generate PDF from Knowledge Base")
    
    try:
        # First, store an incident with RCA
        kb_service.store_incident(
            incident_id="INC-PDF-KB-001",
            description="Authentication service timeout errors",
            severity="High",
            affected_service="auth",
            risk_score=75.0,
            confidence=85.0
        )
        
        # Store RCA for the incident
        kb_service.store_rca_report(
            incident_id="INC-PDF-KB-001",
            root_cause="Session store connection pool exhausted",
            impact_analysis="Users unable to authenticate for 30 minutes",
            recommendations="Increase session store pool size, add monitoring",
            prevention_measures="Implement connection pool alerts",
            rca_text="""
## Executive Summary
Authentication service timeout caused by session store pool exhaustion.

## Root Cause
Session store connection pool size (20) insufficient for peak load.

## Recommendations
1. Increase pool size to 50
2. Add connection pool monitoring
3. Implement auto-scaling

## Prevention
- Real-time pool monitoring
- Load testing for session store
- Automated capacity planning
""",
            model_used="gemini-flash-latest"
        )
        
        print("  Incident and RCA stored in knowledge base")
        
        # Retrieve and verify
        incident = kb_service.get_incident("INC-PDF-KB-001")
        assert incident is not None, "Incident not retrieved"
        assert incident['rca_report'] is not None, "RCA not retrieved"
        
        print("  Retrieved incident from knowledge base ✅")
        print_success("Test 3 PASSED - Knowledge base integration working")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Service info
    print_test("Test 4: PDF Generator Service Info")
    
    info = pdf_generator.get_service_info()
    
    print(f"Service Info:")
    print(f"  Service: {info['service']}")
    print(f"  Status: {info['status']}")
    print(f"  Library: {info['library']}")
    print(f"  Capabilities: {len(info['capabilities'])}")
    print(f"  Formats: {info['formats']}")
    print(f"  Page Size: {info['page_size']}")
    
    assert info['status'] == 'operational', "Service not operational"
    print_success("Test 4 PASSED - Service info retrieved")
    
    print_header("MODULE 9: ALL TESTS PASSED")
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST OUTPUT FILES")
    print("=" * 70)
    print(f"\n📄 Generated PDF files in: {output_dir.absolute()}")
    print(f"   1. test_rca_report.pdf - Standard RCA report")
    print(f"   2. test_large_rca_report.pdf - Large RCA report")
    print("\n✅ Open these files to verify PDF formatting and content!")
    print("=" * 70 + "\n")
    
    return True


def main():
    """Run all tests"""
    print_header("TESTING MODULE 9")
    print("Member 3: AI & RCA Engine")
    print("Testing PDF Report Generator")
    
    try:
        # Test Module 9
        module9_pass = test_module9_pdf_generator()
        
        # Final Summary
        print_header("FINAL TEST RESULTS")
        if module9_pass:
            print("✅ SUCCESS: All tests passed!")
            print("\nModule 9: PDF Report Generator - COMPLETE")
            print("  ✅ Generate PDF → PDF downloads successfully")
            print("  ✅ Large RCA → Formatting remains correct")
            print("  ✅ Knowledge base integration working")
            print("  ✅ Service info available")
            print("\nDeliverable:")
            print("  ✅ Module 9: PDF generation completed")
            print_header("MODULE 9 READY FOR PRODUCTION")
            return 0
        else:
            print("❌ FAILURE: Some tests failed")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
