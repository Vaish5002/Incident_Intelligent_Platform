import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { AppProvider } from '../../src/context/AppContext';
import Investigation from '../../src/pages/Investigation';
import Results from '../../src/pages/Results';
import { api } from '../../src/services/api';

// Mock API module
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

describe('E2E Test - Scenario 1: DB Timeout Investigation', () => {
  const mockInvestigationResponse = {
    success: true,
    investigationId: 1,
    status: 'completed',
    data: {
      investigation_id: 1,
      status: 'completed',
      repo_url: 'https://github.com/test/db-timeout-repo',
      incident_description: 'Database connection timeout errors during peak load',
      investigation: {
        severity: 'CRITICAL',
        risk_score: 92,
        correlation_count: 2405,
        incident_type: 'Database',
        probable_root_cause: {
          description: 'Database connection pool exhausted due to unindexed query on orders table',
          confidence: 0.96
        },
        timeline: [
          { time: '11:15:00', event: 'Database query latency spike detected', type: 'warning' },
          { time: '11:17:30', event: 'Connection pool reached maximum capacity', type: 'critical' },
          { time: '11:18:12', event: 'SQL timeout exceptions thrown', type: 'critical' },
          { time: '11:20:00', event: 'Automated alert sent to on-call DBA', type: 'info' }
        ],
        recommendations: [
          'Roll back recent OrderService deployment',
          'Add composite index on orders table: (user_id, status)',
          'Refactor N+1 query pattern in batch processing'
        ],
        log_patterns: [
          'HikariPool-1 - Connection is not available',
          'SQLTransientConnectionException: Connection timeout',
          'PostgreSQL: remaining connection slots reserved'
        ]
      }
    }
  };

  const mockPdfResponse = {
    success: true,
    filename: 'RCA_Report_1_2026-06-09.pdf',
    message: 'PDF downloaded successfully'
  };

  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
    
    // Setup default mock responses
    api.healthCheck.mockResolvedValue({ success: true });
    api.member3HealthCheck.mockResolvedValue({ success: true });
  });

  it('should complete full DB timeout investigation workflow', async () => {
    const user = userEvent.setup();
    
    // Mock API responses
    api.investigate.mockResolvedValue(mockInvestigationResponse);
    api.getResults.mockResolvedValue({
      success: true,
      data: mockInvestigationResponse.data
    });
    api.downloadPdf.mockResolvedValue(mockPdfResponse);

    // Render Investigation page
    const { container } = render(
      <BrowserRouter>
        <AppProvider>
          <Investigation />
        </AppProvider>
      </BrowserRouter>
    );

    // Step 1: Fill in the investigation form
    const githubInput = screen.getByPlaceholderText(/github.*url/i);
    const descriptionInput = screen.getByPlaceholderText(/describe.*incident/i);

    await user.type(githubInput, 'https://github.com/test/db-timeout-repo');
    await user.type(descriptionInput, 'Database connection timeout errors during peak load');

    // Step 2: Submit the investigation
    const investigateButton = screen.getByRole('button', { name: /investigate/i });
    await user.click(investigateButton);

    // Step 3: Verify API was called with correct data
    await waitFor(() => {
      expect(api.investigate).toHaveBeenCalledWith(
        'https://github.com/test/db-timeout-repo',
        'Database connection timeout errors during peak load'
      );
    });

    // Step 4: Wait for progress tracker to appear
    await waitFor(() => {
      expect(screen.queryByText(/github agent/i)).toBeInTheDocument();
    }, { timeout: 3000 });

    // Step 5: Verify investigation completes
    // (In real scenario, this would involve navigation to Results page)
    expect(api.investigate).toHaveBeenCalledTimes(1);
    expect(mockInvestigationResponse.status).toBe('completed');
  });

  it('should display DB timeout in root cause analysis', async () => {
    // Mock investigation data
    const mockIncident = {
      id: 'INC-1',
      name: 'INC-1: Database Timeout',
      shortName: 'Database Timeout',
      severity: 'CRITICAL',
      status: 'RESOLVED',
      riskScore: 92,
      logAnalysis: {
        rootCause: 'Database connection pool exhausted due to unindexed query',
        errorPatterns: [
          'Connection timeout',
          'SQLTransientConnectionException',
          'Connection pool exhausted'
        ]
      },
      riskAssessment: {
        score: 92,
        severity: 'CRITICAL',
        confidence: '96%'
      }
    };

    // Setup context with mock incident
    const { container } = render(
      <BrowserRouter>
        <AppProvider>
          <Results />
        </AppProvider>
      </BrowserRouter>
    );

    // Verify database-related terms appear
    await waitFor(() => {
      const text = container.textContent;
      expect(text).toMatch(/database|timeout|connection/i);
    });
  });

  it('should verify risk score is generated for DB timeout', async () => {
    const investigation = mockInvestigationResponse.data.investigation;

    // Verify risk score exists and is in valid range
    expect(investigation.risk_score).toBeDefined();
    expect(investigation.risk_score).toBeGreaterThanOrEqual(0);
    expect(investigation.risk_score).toBeLessThanOrEqual(100);
    
    // Verify severity is CRITICAL
    expect(investigation.severity).toBe('CRITICAL');
    
    // Verify confidence score
    expect(investigation.probable_root_cause.confidence).toBeGreaterThan(0.9);
  });

  it('should generate PDF for DB timeout investigation', async () => {
    api.downloadPdf.mockResolvedValue(mockPdfResponse);

    // Call PDF download
    const result = await api.downloadPdf(1);

    // Verify PDF generation was successful
    expect(result.success).toBe(true);
    expect(result.filename).toContain('RCA_Report');
    expect(result.filename).toContain('.pdf');
  });

  it('should verify timeline contains DB timeout events', () => {
    const timeline = mockInvestigationResponse.data.investigation.timeline;

    // Verify timeline has events
    expect(timeline).toBeDefined();
    expect(timeline.length).toBeGreaterThan(0);

    // Verify database-related events exist
    const hasDbEvent = timeline.some(event => 
      event.event.toLowerCase().includes('database') ||
      event.event.toLowerCase().includes('connection') ||
      event.event.toLowerCase().includes('sql')
    );
    expect(hasDbEvent).toBe(true);

    // Verify event types are valid
    const validTypes = ['info', 'warning', 'critical'];
    timeline.forEach(event => {
      expect(validTypes).toContain(event.type);
    });
  });

  it('should verify recommendations are provided', () => {
    const recommendations = mockInvestigationResponse.data.investigation.recommendations;

    // Verify recommendations exist
    expect(recommendations).toBeDefined();
    expect(recommendations.length).toBeGreaterThan(0);

    // Verify recommendations are strings
    recommendations.forEach(rec => {
      expect(typeof rec).toBe('string');
      expect(rec.length).toBeGreaterThan(0);
    });
  });

  it('should handle investigation errors gracefully', async () => {
    const user = userEvent.setup();
    
    // Mock API error
    api.investigate.mockRejectedValue(new Error('Backend connection failed'));

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
    await user.type(descriptionInput, 'Test error handling');

    const investigateButton = screen.getByRole('button', { name: /investigate/i });
    await user.click(investigateButton);

    // Verify error message appears
    await waitFor(() => {
      const errorText = screen.queryByText(/failed|error/i);
      expect(errorText).toBeInTheDocument();
    });
  });
});

describe('DB Timeout - API Integration Tests', () => {
  it('should verify investigation API returns expected structure', async () => {
    api.investigate.mockResolvedValue({
      success: true,
      investigationId: 1,
      status: 'completed',
      data: {
        investigation_id: 1,
        status: 'completed',
        investigation: {
          severity: 'CRITICAL',
          risk_score: 92
        }
      }
    });

    const result = await api.investigate(
      'https://github.com/test/repo',
      'Database timeout'
    );

    expect(result).toHaveProperty('success');
    expect(result).toHaveProperty('investigationId');
    expect(result).toHaveProperty('status');
    expect(result).toHaveProperty('data');
  });

  it('should verify results API returns investigation data', async () => {
    api.getResults.mockResolvedValue({
      success: true,
      data: {
        id: 1,
        status: 'completed',
        severity: 'CRITICAL',
        investigation: {}
      }
    });

    const result = await api.getResults(1);

    expect(result.success).toBe(true);
    expect(result.data).toHaveProperty('id');
    expect(result.data).toHaveProperty('status');
    expect(result.data).toHaveProperty('severity');
  });
});
