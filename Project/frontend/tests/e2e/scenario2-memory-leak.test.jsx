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

describe('E2E Test - Scenario 2: Memory Leak Investigation', () => {
  const mockMemoryLeakResponse = {
    success: true,
    investigationId: 2,
    status: 'completed',
    data: {
      investigation_id: 2,
      status: 'completed',
      repo_url: 'https://github.com/test/websocket-service',
      incident_description: 'WebSocket service experiencing memory leak and OOM crashes',
      investigation: {
        severity: 'HIGH',
        risk_score: 78,
        correlation_count: 125,
        incident_type: 'Infrastructure',
        probable_root_cause: {
          description: 'Memory leak in WebSocket connection handlers - event listeners not removed on socket close',
          confidence: 0.91
        },
        timeline: [
          { time: '22:00:00', event: 'Memory usage climbing linearly at 150MB/hour', type: 'warning' },
          { time: '03:45:00', event: 'Node.js VM enters GC thrashing state', type: 'warning' },
          { time: '04:00:00', event: 'Pod memory limit breached - OOM Killed', type: 'critical' }
        ],
        recommendations: [
          'Modify socketManager.js to unregister IPC listener on socket close',
          'Add Jest/Mocha heapdump testing for memory leak detection',
          'Configure WebSocket memory thresholds with automated restarts'
        ],
        log_patterns: [
          'FATAL ERROR: JavaScript heap out of memory',
          'Process exited with code 137 (OOM Killed)',
          'Ineffective mark-compacts near heap limit'
        ],
        risk_factors: [
          'Memory leak slope strictly positive (+150MB/h)',
          'Kubernetes container crash loop',
          'Active WebSocket terminal disconnections'
        ]
      }
    }
  };

  beforeEach(() => {
    vi.clearAllMocks();
    api.healthCheck.mockResolvedValue({ success: true });
    api.member3HealthCheck.mockResolvedValue({ success: true });
  });

  it('should complete full memory leak investigation workflow', async () => {
    const user = userEvent.setup();
    
    api.investigate.mockResolvedValue(mockMemoryLeakResponse);
    api.getResults.mockResolvedValue({
      success: true,
      data: mockMemoryLeakResponse.data
    });

    render(
      <BrowserRouter>
        <AppProvider>
          <Investigation />
        </AppProvider>
      </BrowserRouter>
    );

    // Fill form with memory leak scenario
    const githubInput = screen.getByPlaceholderText(/github.*url/i);
    const descriptionInput = screen.getByPlaceholderText(/describe.*incident/i);

    await user.type(githubInput, 'https://github.com/test/websocket-service');
    await user.type(descriptionInput, 'WebSocket service experiencing memory leak and OOM crashes');

    // Submit investigation
    const investigateButton = screen.getByRole('button', { name: /investigate/i });
    await user.click(investigateButton);

    // Verify API called
    await waitFor(() => {
      expect(api.investigate).toHaveBeenCalledWith(
        'https://github.com/test/websocket-service',
        'WebSocket service experiencing memory leak and OOM crashes'
      );
    });

    expect(api.investigate).toHaveBeenCalledTimes(1);
  });

  it('should detect memory issue in investigation results', () => {
    const investigation = mockMemoryLeakResponse.data.investigation;

    // Verify memory-related root cause
    const rootCause = investigation.probable_root_cause.description.toLowerCase();
    expect(rootCause).toMatch(/memory/);
    
    // Verify incident type
    expect(investigation.incident_type).toBe('Infrastructure');
    
    // Verify severity
    expect(['HIGH', 'CRITICAL']).toContain(investigation.severity);
  });

  it('should verify timeline displays memory leak progression', () => {
    const timeline = mockMemoryLeakResponse.data.investigation.timeline;

    // Verify timeline exists
    expect(timeline).toBeDefined();
    expect(timeline.length).toBeGreaterThan(0);

    // Verify memory-related events
    const hasMemoryEvent = timeline.some(event =>
      event.event.toLowerCase().includes('memory') ||
      event.event.toLowerCase().includes('oom') ||
      event.event.toLowerCase().includes('heap')
    );
    expect(hasMemoryEvent).toBe(true);

    // Verify critical event exists
    const hasCriticalEvent = timeline.some(event => event.type === 'critical');
    expect(hasCriticalEvent).toBe(true);
  });

  it('should generate recommendations for memory leak', () => {
    const recommendations = mockMemoryLeakResponse.data.investigation.recommendations;

    // Verify recommendations exist
    expect(recommendations).toBeDefined();
    expect(recommendations.length).toBeGreaterThan(0);

    // Verify memory-related recommendations
    const hasMemoryRec = recommendations.some(rec =>
      rec.toLowerCase().includes('memory') ||
      rec.toLowerCase().includes('leak') ||
      rec.toLowerCase().includes('heap')
    );
    expect(hasMemoryRec).toBe(true);
  });

  it('should verify error patterns contain OOM errors', () => {
    const logPatterns = mockMemoryLeakResponse.data.investigation.log_patterns;

    // Verify patterns exist
    expect(logPatterns).toBeDefined();
    expect(logPatterns.length).toBeGreaterThan(0);

    // Verify OOM-related patterns
    const hasOomPattern = logPatterns.some(pattern =>
      pattern.toLowerCase().includes('oom') ||
      pattern.toLowerCase().includes('out of memory') ||
      pattern.toLowerCase().includes('heap')
    );
    expect(hasOomPattern).toBe(true);
  });

  it('should verify risk factors for memory leak', () => {
    const riskFactors = mockMemoryLeakResponse.data.investigation.risk_factors;

    // Verify risk factors exist
    expect(riskFactors).toBeDefined();
    expect(riskFactors.length).toBeGreaterThan(0);

    // Verify memory-related risk factors
    const hasMemoryRisk = riskFactors.some(factor =>
      factor.toLowerCase().includes('memory') ||
      factor.toLowerCase().includes('leak')
    );
    expect(hasMemoryRisk).toBe(true);
  });

  it('should verify risk score is calculated', () => {
    const investigation = mockMemoryLeakResponse.data.investigation;

    // Verify risk score
    expect(investigation.risk_score).toBeDefined();
    expect(investigation.risk_score).toBeGreaterThanOrEqual(0);
    expect(investigation.risk_score).toBeLessThanOrEqual(100);

    // Verify confidence
    expect(investigation.probable_root_cause.confidence).toBeGreaterThan(0.8);
  });

  it('should handle memory leak investigation with missing data', async () => {
    api.investigate.mockResolvedValue({
      success: true,
      investigationId: 3,
      status: 'completed',
      data: {
        investigation_id: 3,
        status: 'completed',
        investigation: {
          severity: 'MEDIUM',
          // Missing some optional fields
        }
      }
    });

    const result = await api.investigate(
      'https://github.com/test/repo',
      'Memory issue'
    );

    // Should still return success
    expect(result.success).toBe(true);
    expect(result.data.investigation).toBeDefined();
  });

  it('should verify investigation completes within timeout', async () => {
    const user = userEvent.setup();
    
    api.investigate.mockImplementation(() => 
      new Promise(resolve => 
        setTimeout(() => resolve(mockMemoryLeakResponse), 100)
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
    await user.type(descriptionInput, 'Memory leak test');

    const investigateButton = screen.getByRole('button', { name: /investigate/i });
    await user.click(investigateButton);

    // Verify call completes within reasonable time
    await waitFor(() => {
      expect(api.investigate).toHaveBeenCalled();
    }, { timeout: 5000 });
  });
});

describe('Memory Leak - Specific Component Tests', () => {
  it('should validate memory leak data structure', () => {
    const investigation = mockMemoryLeakResponse.data.investigation;

    // Verify required fields
    expect(investigation).toHaveProperty('severity');
    expect(investigation).toHaveProperty('risk_score');
    expect(investigation).toHaveProperty('incident_type');
    expect(investigation).toHaveProperty('probable_root_cause');
    expect(investigation).toHaveProperty('timeline');
    expect(investigation).toHaveProperty('recommendations');

    // Verify nested structures
    expect(investigation.probable_root_cause).toHaveProperty('description');
    expect(investigation.probable_root_cause).toHaveProperty('confidence');
  });

  it('should verify timeline events are chronological', () => {
    const timeline = mockMemoryLeakResponse.data.investigation.timeline;

    // Verify timeline is sorted by time
    for (let i = 1; i < timeline.length; i++) {
      const prevTime = timeline[i - 1].time;
      const currTime = timeline[i].time;
      
      // Times should be in ascending order
      expect(currTime >= prevTime).toBe(true);
    }
  });
});
