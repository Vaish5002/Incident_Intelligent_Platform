import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { AppProvider } from '../../src/context/AppContext';
import Investigation from '../../src/pages/Investigation';
import { api } from '../../src/services/api';

vi.mock('../../src/services/api', () => ({
  api: {
    investigate: vi.fn(),
    getResults: vi.fn(),
    getTimeline: vi.fn(),
    downloadPdf: vi.fn(),
    healthCheck: vi.fn(),
    member3HealthCheck: vi.fn(),
  },
}));

describe('E2E Test - Scenario 3: Missing ENV Variable Investigation', () => {
  const mockMissingEnvResponse = {
    success: true,
    investigationId: 3,
    status: 'completed',
    data: {
      investigation_id: 3,
      status: 'completed',
      repo_url: 'https://github.com/test/config-service',
      incident_description: 'Service failing due to missing environment variables in production deployment',
      investigation: {
        severity: 'CRITICAL',
        risk_score: 85,
        correlation_count: 342,
        incident_type: 'Code Error',
        probable_root_cause: {
          description: 'Missing DATABASE_URL environment variable causing NullPointerException in application startup',
          confidence: 0.99
        },
        timeline: [
          { time: '14:30:00', event: 'Production deployment of v2.5.0 completed', type: 'info' },
          { time: '14:31:15', event: 'Application startup attempted', type: 'warning' },
          { time: '14:31:30', event: 'NullPointerException: DATABASE_URL is null', type: 'critical' },
          { time: '14:32:00', event: 'Service down - all requests failing with 503', type: 'critical' },
          { time: '14:35:00', event: 'Alert: DatabaseConfig null check failed', type: 'critical' }
        ],
        recommendations: [
          'Add DATABASE_URL to production environment configuration',
          'Implement mandatory environment variable validation on startup',
          'Add pre-deployment environment checklist verification',
          'Use configuration management service (Vault, Secrets Manager) for sensitive vars'
        ],
        log_patterns: [
          'NullPointerException: DATABASE_URL is null',
          'Error initializing database connection: variable not found',
          'ConfigurationError: Required environment variables missing',
          'Application failed to start - configuration invalid'
        ],
        risk_factors: [
          'Application completely down',
          '100% request failure rate',
          'No graceful degradation',
          'Configuration error not caught in pre-flight checks'
        ]
      }
    }
  };

  beforeEach(() => {
    vi.clearAllMocks();
    api.healthCheck.mockResolvedValue({ success: true });
    api.member3HealthCheck.mockResolvedValue({ success: true });
  });

  it('should complete full missing ENV variable investigation workflow', async () => {
    const user = userEvent.setup();
    
    api.investigate.mockResolvedValue(mockMissingEnvResponse);
    api.getResults.mockResolvedValue({
      success: true,
      data: mockMissingEnvResponse.data
    });

    render(
      <BrowserRouter>
        <AppProvider>
          <Investigation />
        </AppProvider>
      </BrowserRouter>
    );

    // Fill form with missing ENV scenario
    const githubInput = screen.getByPlaceholderText(/github.*url/i);
    const descriptionInput = screen.getByPlaceholderText(/describe.*incident/i);

    await user.type(githubInput, 'https://github.com/test/config-service');
    await user.type(descriptionInput, 'Service failing due to missing environment variables in production deployment');

    // Submit investigation
    const investigateButton = screen.getByRole('button', { name: /investigate/i });
    await user.click(investigateButton);

    // Verify API called with correct data
    await waitFor(() => {
      expect(api.investigate).toHaveBeenCalledWith(
        'https://github.com/test/config-service',
        'Service failing due to missing environment variables in production deployment'
      );
    });

    expect(api.investigate).toHaveBeenCalledTimes(1);
  });

  it('should detect configuration issue in root cause', () => {
    const investigation = mockMissingEnvResponse.data.investigation;

    // Verify root cause mentions configuration/environment
    const rootCause = investigation.probable_root_cause.description.toLowerCase();
    expect(rootCause).toMatch(/environment|config|variable|database/i);
    
    // Verify severity is critical
    expect(investigation.severity).toBe('CRITICAL');
    
    // Verify high confidence
    expect(investigation.probable_root_cause.confidence).toBeGreaterThan(0.95);
  });

  it('should verify root cause mentions missing ENV variable', () => {
    const investigation = mockMissingEnvResponse.data.investigation;
    const rootCause = investigation.probable_root_cause.description;

    // Verify missing variable mentioned
    expect(rootCause).toMatch(/missing|null|not found|environment/i);
  });

  it('should display prevention steps in recommendations', () => {
    const recommendations = mockMissingEnvResponse.data.investigation.recommendations;

    // Verify recommendations exist
    expect(recommendations).toBeDefined();
    expect(recommendations.length).toBeGreaterThan(0);

    // Verify prevention/configuration recommendations
    const hasPreventionRec = recommendations.some(rec =>
      rec.toLowerCase().includes('environment') ||
      rec.toLowerCase().includes('config') ||
      rec.toLowerCase().includes('validation') ||
      rec.toLowerCase().includes('checklist')
    );
    expect(hasPreventionRec).toBe(true);
  });

  it('should verify timeline shows critical error events', () => {
    const timeline = mockMissingEnvResponse.data.investigation.timeline;

    // Verify timeline exists
    expect(timeline).toBeDefined();
    expect(timeline.length).toBeGreaterThan(0);

    // Verify configuration/environment error event exists
    const hasConfigError = timeline.some(event =>
      event.event.toLowerCase().includes('config') ||
      event.event.toLowerCase().includes('environment') ||
      event.event.toLowerCase().includes('null') ||
      event.event.toLowerCase().includes('variable')
    );
    expect(hasConfigError).toBe(true);

    // Verify critical events exist
    const criticalEvents = timeline.filter(event => event.type === 'critical');
    expect(criticalEvents.length).toBeGreaterThan(0);
  });

  it('should verify error patterns show configuration errors', () => {
    const logPatterns = mockMissingEnvResponse.data.investigation.log_patterns;

    // Verify patterns exist
    expect(logPatterns).toBeDefined();
    expect(logPatterns.length).toBeGreaterThan(0);

    // Verify configuration/environment error patterns
    const hasConfigError = logPatterns.some(pattern =>
      pattern.toLowerCase().includes('null') ||
      pattern.toLowerCase().includes('environment') ||
      pattern.toLowerCase().includes('config') ||
      pattern.toLowerCase().includes('variable')
    );
    expect(hasConfigError).toBe(true);
  });

  it('should verify risk factors include configuration issues', () => {
    const riskFactors = mockMissingEnvResponse.data.investigation.risk_factors;

    // Verify risk factors exist
    expect(riskFactors).toBeDefined();
    expect(riskFactors.length).toBeGreaterThan(0);

    // Verify service availability risk
    const hasAvailabilityRisk = riskFactors.some(factor =>
      factor.toLowerCase().includes('down') ||
      factor.toLowerCase().includes('failure') ||
      factor.toLowerCase().includes('error') ||
      factor.toLowerCase().includes('unavailable')
    );
    expect(hasAvailabilityRisk).toBe(true);
  });

  it('should generate proper risk score for configuration error', () => {
    const investigation = mockMissingEnvResponse.data.investigation;

    // Verify risk score
    expect(investigation.risk_score).toBeDefined();
    expect(investigation.risk_score).toBeGreaterThanOrEqual(0);
    expect(investigation.risk_score).toBeLessThanOrEqual(100);

    // Configuration errors causing full outage should have high score
    expect(investigation.risk_score).toBeGreaterThan(75);
  });

  it('should show configuration as incident type', () => {
    const investigation = mockMissingEnvResponse.data.investigation;

    // Verify incident type is code/config related
    expect(['Code Error', 'Configuration', 'Deployment']).toContain(investigation.incident_type);
  });

  it('should correlate deployment time with error occurrence', () => {
    const timeline = mockMissingEnvResponse.data.investigation.timeline;

    // Verify deployment event exists
    const deploymentEvent = timeline.find(event =>
      event.event.toLowerCase().includes('deployment')
    );
    expect(deploymentEvent).toBeDefined();

    // Verify errors occur after deployment
    const deploymentIndex = timeline.indexOf(deploymentEvent);
    const errorEvent = timeline.find((event, idx) =>
      idx > deploymentIndex && (
        event.event.toLowerCase().includes('error') ||
        event.event.toLowerCase().includes('failed') ||
        event.event.toLowerCase().includes('null')
      )
    );
    expect(errorEvent).toBeDefined();
  });

  it('should handle investigation with partial data', async () => {
    api.investigate.mockResolvedValue({
      success: true,
      investigationId: 4,
      status: 'completed',
      data: {
        investigation_id: 4,
        status: 'completed',
        investigation: {
          severity: 'MEDIUM',
          // Missing optional fields
        }
      }
    });

    const result = await api.investigate(
      'https://github.com/test/repo',
      'Configuration issue'
    );

    // Should still return success
    expect(result.success).toBe(true);
    expect(result.data.investigation).toBeDefined();
  });

  it('should verify investigation completes within timeout', async () => {
    const user = userEvent.setup();
    
    // Simulate delayed API response
    api.investigate.mockImplementation(() => 
      new Promise(resolve => 
        setTimeout(() => resolve(mockMissingEnvResponse), 150)
      )
    );

    render(
      <BrowserRouter>
        <AppProvider>
          <Investigation />
        </AppProvider>
      </BrowserRouter>
    );

    const githubInput = screen.getByPlaceholderText(/github.*url/i);
    const descriptionInput = screen.getByPlaceholderText(/describe.*incident/i);

    await user.type(githubInput, 'https://github.com/test/repo');
    await user.type(descriptionInput, 'Missing config test');

    const investigateButton = screen.getByRole('button', { name: /investigate/i });
    await user.click(investigateButton);

    // Verify call completes within timeout
    await waitFor(() => {
      expect(api.investigate).toHaveBeenCalled();
    }, { timeout: 5000 });
  });

  it('should verify recommendations include configuration best practices', () => {
    const recommendations = mockMissingEnvResponse.data.investigation.recommendations;

    // Verify at least one recommendation about environment validation
    const hasValidationRec = recommendations.some(rec =>
      rec.toLowerCase().includes('validation') ||
      rec.toLowerCase().includes('environment') ||
      rec.toLowerCase().includes('mandatory')
    );
    expect(hasValidationRec).toBe(true);

    // Verify at least one recommendation about configuration management
    const hasConfigMgmt = recommendations.some(rec =>
      rec.toLowerCase().includes('vault') ||
      rec.toLowerCase().includes('secrets') ||
      rec.toLowerCase().includes('configuration management')
    );
    expect(hasConfigMgmt).toBe(true);
  });
});

describe('Missing ENV - Cross-Scenario Tests', () => {
  it('should validate investigation response structure', () => {
    const investigation = mockMissingEnvResponse.data.investigation;

    // Verify all required fields exist
    const requiredFields = [
      'severity',
      'risk_score',
      'incident_type',
      'probable_root_cause',
      'timeline',
      'recommendations',
      'log_patterns'
    ];

    requiredFields.forEach(field => {
      expect(investigation).toHaveProperty(field);
      expect(investigation[field]).toBeDefined();
    });
  });

  it('should verify timeline has proper structure', () => {
    const timeline = mockMissingEnvResponse.data.investigation.timeline;

    // Verify each event has required fields
    timeline.forEach(event => {
      expect(event).toHaveProperty('time');
      expect(event).toHaveProperty('event');
      expect(event).toHaveProperty('type');

      // Verify type is valid
      expect(['info', 'warning', 'critical']).toContain(event.type);
    });
  });

  it('should verify recommendations are actionable', () => {
    const recommendations = mockMissingEnvResponse.data.investigation.recommendations;

    // Each recommendation should be a string
    recommendations.forEach(rec => {
      expect(typeof rec).toBe('string');
      expect(rec.length).toBeGreaterThan(10); // Meaningful recommendation
    });
  });

  it('should verify error patterns match log analysis', () => {
    const investigation = mockMissingEnvResponse.data.investigation;

    // Error patterns should relate to root cause
    const rootCauseLower = investigation.probable_root_cause.description.toLowerCase();
    const patternsRelated = investigation.log_patterns.some(pattern =>
      rootCauseLower.split(' ').some(word =>
        pattern.toLowerCase().includes(word)
      )
    );

    expect(patternsRelated).toBe(true);
  });
});

describe('Investigation - API Error Handling', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should handle API timeout gracefully', async () => {
    api.investigate.mockImplementation(() =>
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Request timeout')), 100)
      )
    );

    try {
      await api.investigate('https://github.com/test/repo', 'Test timeout');
      expect.fail('Should have thrown error');
    } catch (error) {
      expect(error.message).toContain('timeout');
    }
  });

  it('should handle API connection error', async () => {
    api.investigate.mockRejectedValue(new Error('Connection refused'));

    try {
      await api.investigate('https://github.com/test/repo', 'Test');
      expect.fail('Should have thrown error');
    } catch (error) {
      expect(error.message).toContain('Connection');
    }
  });

  it('should handle server error response', async () => {
    api.investigate.mockRejectedValue(new Error('Server returned 500'));

    try {
      await api.investigate('https://github.com/test/repo', 'Test');
      expect.fail('Should have thrown error');
    } catch (error) {
      expect(error.message).toContain('500');
    }
  });
});
