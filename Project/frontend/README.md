# SmartOps AI - Frontend

React-based frontend application for incident investigation and RCA visualization.

## Structure

```
frontend/
├── public/              # Static assets
│   ├── favicon.svg
│   └── icons.svg
├── src/                 # Source code
│   ├── components/      # React components
│   │   ├── DashboardCard.jsx
│   │   ├── Header.jsx
│   │   ├── IncidentForm.jsx
│   │   ├── Layout.jsx
│   │   ├── Navbar.jsx
│   │   ├── ProgressTracker.jsx
│   │   ├── Recommendations.jsx
│   │   ├── ResultCard.jsx
│   │   └── Sidebar.jsx
│   ├── pages/           # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Investigation.jsx
│   │   ├── Results.jsx
│   │   ├── Login.jsx
│   │   ├── Analysis.jsx
│   │   ├── Reports.jsx
│   │   ├── Copilot.jsx
│   │   └── Upload.jsx
│   ├── services/        # API services
│   │   ├── api.js
│   │   └── mockData.js
│   ├── context/         # State management
│   │   └── AppContext.jsx
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── tests/               # Test files
│   ├── setup.js
│   └── e2e/
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── vercel.json          # Vercel deployment config
└── .env.example         # Environment template

```

## Quick Start

### 1. Install Dependencies

```bash
npm install --legacy-peer-deps
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and set VITE_API_URL
```

Example `.env`:
```env
VITE_API_URL=http://localhost:8002
```

### 3. Run Development Server

```bash
npm run dev
```

Server runs at: http://localhost:5173

## Environment Variables

Required:
- `VITE_API_URL` - Backend API URL (e.g., http://localhost:8002)

For production:
```env
VITE_API_URL=https://your-backend.onrender.com
```

## Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm test             # Run tests
npm run test:e2e     # Run end-to-end tests
npm run test:coverage # Run tests with coverage
```

## Features

- Investigation Workflow
- Real-time Progress Tracking
- Interactive Results Dashboard
- PDF Report Download
- Timeline Visualization
- Risk Assessment Display
- AI Recommendations
- Copilot Chat Interface

## Key Components

### Pages
- **Dashboard** - Overview of recent investigations
- **Investigation** - Start new investigation with GitHub URL
- **Results** - View detailed RCA results
- **Reports** - Historical reports and analytics
- **Login** - Authentication page

### Components
- **IncidentForm** - GitHub URL and description input
- **ProgressTracker** - Multi-step investigation progress
- **ResultCard** - Display investigation results
- **Recommendations** - AI-powered action items

## Routing

- `/` - Login page
- `/dashboard` - Main dashboard
- `/investigation` - New investigation
- `/results` - Investigation results
- `/analysis` - Analysis view
- `/reports` - Reports archive
- `/copilot` - AI Copilot chat

## Deployment

See [deployment documentation](../../STEP_BY_STEP_DEPLOYMENT.md) for detailed instructions.

### Vercel Deployment

```bash
# Automatic via vercel.json
# Just connect GitHub repository
# Add VITE_API_URL environment variable
```

### Manual Build

```bash
# Build
npm run build

# Output: dist/ folder
# Serve with any static hosting
```

## Tech Stack

- React 19 - UI library
- Vite 8 - Build tool
- Tailwind CSS 4 - Styling
- React Router v7 - Routing
- Axios - HTTP client
- Recharts - Charts
- Lucide React - Icons

## Demo Credentials

For testing:
```
Email: operator@smartops.ai
Password: password123
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT
