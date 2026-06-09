# SmartOps AI – Agentic Incident Intelligence Platform Frontend

Create a modern, dark-themed Enterprise SaaS React frontend for **SmartOps AI**, an Agentic Incident Intelligence Platform. Built using JavaScript, Vite, React Router, Recharts, and Tailwind CSS, featuring glassmorphism cards and a responsive layout.

## Final Specifications (User Approved)

- **Language**: JavaScript (React + Vite)
- **Styling**: Tailwind CSS (Dark Theme, Glassmorphism Cards, Modern AI Platform look)
- **Libraries**: `react-router-dom` for navigation, `recharts` for charts, and `lucide-react` for icons.

---

## Proposed Modules & Pages

1. **Login Page (`/login`)**
   - Sleek login page with email, password, and a glowing "Sign In" button.
   - Premium **SmartOps AI** branding with floating background abstract animations.

2. **Dashboard (`/dashboard` or `/`)**
   - Metric Cards: Total Incidents, Critical Incidents, Open Investigations, Resolved Cases.
   - Recharts Visualizations:
     - Error Frequency Chart (Bar/Line)
     - Incident Severity Pie Chart
     - Incident Timeline Chart (Line/Area)
     - Risk Score Distribution Gauge/Bar
   - Recent Incidents Table (showing mock incidents).

3. **Incident Upload Module (`/upload`)**
   - Form fields: Incident Name, Log file (.txt/.log), Timeline CSV (.csv), Git Diff (.txt).
   - Drag & Drop zone with file type validation and status indicators.
   - "Analyze Incident" action button that initiates mock analysis and routes to the Analysis page.

4. **Incident Analysis Module (`/analysis`)**
   - Displays AI-driven analysis results across different specialized agents:
     - **Log Analysis Agent**: Root Cause, Error Patterns, Error Count.
     - **Timeline Analysis Agent**: Chronological Key Events, Incident Sequence.
     - **Git Analysis Agent**: Risky Code Changes, Deployments.
     - **Risk Assessment Agent**: Risk Score, Severity Level.
     - **AI Recommendations**: Summary of suggested remediations.
   - Interactive dropdown to switch between the 5 mock incident scenarios.

5. **RCA Report Module (`/reports`)**
   - Detailed RCA template for selected incidents: Executive Summary, Root Cause, Business Impact, Corrective Actions, Preventive Actions.
   - Download PDF button (triggers browser print or mock PDF download).

6. **AI Copilot Module (`/copilot`)**
   - Interactive chat interface with smart prompt suggestions:
     - "Why did this incident happen?"
     - "What failed first?"
     - "How can this be prevented?"
     - "Which code change caused the issue?"
   - Instant response generator tailored to the currently active/selected incident.

7. **Navigation & Shared Shell**
   - Responsive sidebar with route options: `/dashboard`, `/upload`, `/analysis`, `/reports`, `/copilot`.
   - Global status header showing current active system health.

---

## Mock Incident Scenarios (Data Model)
We will define a central database of 5 mock incidents in `src/services/mockData.js`:
1. **Database Timeout Incident**: Connection pool exhausted due to unindexed query.
2. **API Gateway Failure**: 504 Gateway Timeout caused by a downstream service crash.
3. **Faulty Deployment**: Bad commit introducing a null-pointer exception on user authentication.
4. **Memory Leak**: Node process crashing every 6 hours due to unclosed event listeners.
5. **Service Outage**: Third-party payment provider API unavailability.

---

## Implementation Checklist

### Phase 1: Environment & Initialization
- [ ] Install Node.js LTS via `winget`
- [ ] Initialize React + Vite project in JavaScript
- [ ] Install dependencies (`react-router-dom`, `recharts`, `lucide-react`, `tailwindcss`, `postcss`, `autoprefixer`)
- [ ] Configure Tailwind CSS and add global index.css variables for dark mode / glassmorphism

### Phase 2: Mock Data & Routing Configuration
- [ ] Create `src/services/mockData.js` with 5 detailed incident logs, diffs, analysis reports, and RCA details
- [ ] Set up routing in `src/App.jsx` with active navigation layout
- [ ] Implement Auth Context or simple Mock login state toggle

### Phase 3: Page Layout & Shared Shell
- [ ] Create `src/components/Sidebar.jsx` and `src/components/Header.jsx` with responsive sidebar logic

### Phase 4: Page Implementations
- [ ] Implement `src/pages/Login.jsx`
- [ ] Implement `src/pages/Dashboard.jsx` (Recharts integration)
- [ ] Implement `src/pages/Upload.jsx` (Drag & drop logic, file validation)
- [ ] Implement `src/pages/Analysis.jsx` (Display findings for each of the 4 agents)
- [ ] Implement `src/pages/Reports.jsx` (Print/download PDF logic, RCA display)
- [ ] Implement `src/pages/Copilot.jsx` (Copilot chat UI, prompt auto-fill)

### Phase 5: Verification & Polishing
- [ ] Verify build via `npm run build`
- [ ] Run application using `npm run dev` and test responsiveness and navigation
