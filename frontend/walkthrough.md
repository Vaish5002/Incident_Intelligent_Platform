# SmartOps AI – Agentic Incident Intelligence Platform Frontend

We have successfully created the complete React + Vite frontend application for **SmartOps AI**. It features a modern, high-fidelity dark glassmorphic design that matches enterprise-level SaaS dashboard aesthetics.

---

## 🛠️ Tech Stack & Key Libraries

1. **Core Framework**: React (v19) + Vite
2. **Styling**: Tailwind CSS v4 (Glassmorphism panels, customized glowing shadows, and animations)
3. **Routing**: React Router (`react-router-dom` v6)
4. **Data Visualization**: Recharts (Pie, Line, Area, and Stacked Bar charts)
5. **Icon System**: Lucide React

---

## 📂 Project Structure Created

We structured the code under `src/` to be clean, modular, and easy to maintain:
- [src/services/mockData.js](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/services/mockData.js): The database defining 5 realistic incident scenarios (Database Connection Pool, Kong API Gateway, NullPointer, WebSocket OOM, stripe outage) and global chart telemetry datasets.
- [src/context/AppContext.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/context/AppContext.jsx): Context file managing global app states (authentication, active incidents list, active incident focus switcher).
- **Layouts & Shell**:
  - [src/components/Sidebar.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/components/Sidebar.jsx): Navigation sidebar with active state highlights, context previews, and mobile drawer transitions.
  - [src/components/Header.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/components/Header.jsx): Header bar featuring mobile hamburger menu, health alerts, profile indicators, and a global active incident dropdown switcher.
  - [src/components/Layout.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/components/Layout.jsx): Grid wrapper providing background mesh glow circles and page outlets.
- **Pages**:
  - [src/pages/Login.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Login.jsx): Futuristic glassmorphic credentials portal.
  - [src/pages/Dashboard.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Dashboard.jsx): Main control room with 4 distinct analytics charts and interactive registry table.
  - [src/pages/Upload.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Upload.jsx): Form and drag-and-drop file interface for log ingestion with dynamic upload simulations.
  - [src/pages/Analysis.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Analysis.jsx): Investigate view showing findings from Log, Timeline, Git (with syntax-colored diff viewer), and Risk Agents.
  - [src/pages/Reports.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Reports.jsx): RCA details template with PDF generation / native print capability.
  - [src/pages/Copilot.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Copilot.jsx): Chat UI with contextual question answering.

---

## 🎨 Design Highlights & Visual Polish

- **Background Elements**: Uses radial gradient highlights in deep indigo and violet (`#1e1b4b` -> `#090a10` -> `#05060b`) to build an immersive, cyber-ops control room.
- **Glassmorphism Panels**: Embedded utility classes (`glass-panel`, `glass-panel-hover`) applying `backdrop-filter: blur(16px)` and subtle, translucent borders.
- **Interactive Context Switcher**: A global dropdown in the header dynamically shifts the telemetry focus. Changing it alters all chart data, timeline steps, Git diff files, RCA documentation, and AI Copilot responses across all tabs!
- **Formatted Git Diffs**: Lines prefixed with `+` are styled in translucent emerald (`text-emerald-400 bg-emerald-500/10`), lines with `-` in translucent rose (`text-rose-400 bg-rose-500/10`), and header lines in indigo.
- **Interactive File Uploads**: Dragging files over the upload target changes the frame style and shows verification results. Uploading an incident runs a progress simulation, compiles SRE findings, and appends the custom case into the global state.

---

## 🧪 Validation & Testing

We verified the codebase compilation by running a production build:
```powershell
npm run build
```
**Build Output**:
```
vite v8.0.16 building client environment for production...
transforming...
✓ 2318 modules transformed.
rendering chunks...
dist/index.html                   0.47 kB │ gzip:   0.30 kB
dist/assets/index-DYYD68zS.css   47.75 kB │ gzip:   8.47 kB
dist/assets/index-Cpn65V5S.js   714.30 kB │ gzip: 211.07 kB
✓ built in 596ms
```
The project compiles successfully with zero warnings and zero linter errors.

### 📈 Recharts Responsive Sizing Warning Resolved
During active execution, a console warning regarding collapsed chart dimensions (`width(-1) and height(-1) of chart should be greater than 0`) was encountered. This was completely resolved by two steps:
1. Setting `minWidth={0}` on all `<ResponsiveContainer>` instances.
2. Converting the height prop from percentage strings (`"100%"`) to exact numeric representations matching their parent elements (`288`, `208`, and `256` pixels) in [Dashboard.jsx](file:///C:/Users/Spoorti%20S%20Rayannavar/Desktop/Incident_Intelligent_Platform/src/pages/Dashboard.jsx). This guarantees that Recharts does not query the unmounted DOM parent heights and renders cleanly without warnings on layout load.


