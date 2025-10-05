# OHIPFORWARD UI/Frontend Preview Guide

## 🎨 Overview

This document provides instructions for previewing the OHIPFORWARD healthcare coordination system's user interface.

## 🚀 Quick Start - Local Development

### Prerequisites
- Node.js 14+ installed
- npm package manager

### Starting the Frontend

#### Option 1: Using the Preview Script (Recommended)
The easiest way to start the application with automatic port detection:

**Linux/Mac:**
```bash
./scripts/preview.sh
```

**Windows:**
```cmd
scripts\preview.bat
```

The script will:
- Automatically install dependencies if needed
- Find an available port (starting from 3000)
- Start the development server
- Open the application in your browser

#### Option 2: Manual Start

1. **Navigate to the frontend directory:**
```bash
cd frontend
```

2. **Install dependencies (if not already installed):**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

The application will automatically open in your browser at `http://localhost:3000` (or prompt you if port 3000 is in use)

## 📱 Available Pages

The OHIPFORWARD application includes five main pages:

### 1. **Home Page** (`/`)
- **URL**: `http://localhost:3000/`
- **Features**:
  - Hero section with call-to-action buttons
  - System impact statistics (60% wait time reduction, 25% cost savings)
  - Core features showcase
  - Responsive design with animations

### 2. **Symptom Triage** (`/triage`)
- **URL**: `http://localhost:3000/triage`
- **Features**:
  - Interactive symptom input form
  - Severity level selection
  - Duration tracking
  - AI-powered assessment (requires backend)
  - Results display with urgency classification
  - Confidence scoring visualization
  - Recommended actions and next steps

### 3. **Find Providers** (`/providers`)
- **URL**: `http://localhost:3000/providers`
- **Features**:
  - Search functionality by name or location
  - Filter by specialty
  - Provider cards with detailed information
  - Ratings and wait time display
  - Sample provider data (fallback when backend is unavailable)
  - Book appointment and view details buttons

### 4. **Features** (`/features`)
- **URL**: `http://localhost:3000/features`
- **Features**:
  - Detailed feature descriptions
  - Technology stack overview
  - Key benefits section
  - Six core feature highlights:
    - AI-Powered Triage
    - Smart Scheduling
    - Transportation Integration
    - Care Monitoring
    - Automated Notifications
    - Security & Privacy

### 5. **About** (`/about`)
- **URL**: `http://localhost:3000/about`
- **Features**:
  - Mission and vision statements
  - System impact metrics
  - How it works workflow
  - Core values showcase
  - Links to GitHub repository
  - Call-to-action for contributions

## 🎨 UI Features

### Design System
- **Color Palette**:
  - Primary: Purple gradient (#667eea to #764ba2)
  - Background: Light gray (#f8f9fa)
  - Text: Dark gray (#333) and medium gray (#555)
  - Success: Green (#00c851)
  - Warning: Orange (#ff8800)
  - Error: Red (#ff4444)

### Responsive Design
- Mobile-optimized layouts
- Breakpoint at 768px for tablet/mobile
- Flexible grid systems
- Touch-friendly buttons and controls

### Animations & Interactions
- Smooth page transitions
- Hover effects on cards and buttons
- Loading states and spinners
- Fade-in animations on page load
- Scale and transform effects

### Navigation
- Sticky top navigation bar
- Active link highlighting
- Consistent across all pages
- Mobile-responsive menu

## 🔧 Backend Integration

### With Backend Running

To get full functionality including live triage results:

1. **Start the backend server:**
```bash
# From the project root
python src/main.py
```

2. **Verify backend is running:**
```bash
curl http://localhost:5000/api/v1/health
```

3. **Start the frontend:**
```bash
cd frontend
npm start
```

### Without Backend (Demo Mode)

The frontend includes fallback data for demonstration:
- **Providers page**: Shows 4 sample healthcare providers
- **Triage page**: Form is functional but requires backend for results
- All other pages work fully without backend

## 📦 Production Build

To create an optimized production build:

```bash
cd frontend
npm run build
```

The build artifacts will be in the `frontend/build/` directory and can be served with any static file server:

```bash
# Install serve globally (if not already installed)
npm install -g serve

# Serve the build
serve -s build
```

## 🌐 Deployment Options

### Static Hosting
- **Netlify**: Connect GitHub repo and deploy
- **Vercel**: Automatic deployment from GitHub
- **GitHub Pages**: Use `npm run build` and deploy build folder
- **AWS S3**: Upload build folder to S3 bucket

### With Backend
- **Docker**: Use docker-compose for full stack
- **Cloud Platforms**: AWS, GCP, Azure with container services
- **Heroku**: Deploy frontend and backend separately

## 📸 Screenshots

The following screenshots showcase the enhanced UI:

### Home Page
- Modern hero section with gradient background
- Statistics cards with impact metrics
- Feature preview cards
- Call-to-action sections

### Triage Page
- Clean form design with icons
- Severity level selection
- Real-time validation
- Results display with urgency badges

### Providers Page
- Search and filter functionality
- Provider cards with avatars
- Rating display
- Availability indicators

### Features Page
- Detailed feature descriptions
- Technology stack showcase
- Benefits grid

### About Page
- Mission and vision sections
- Impact statistics
- Workflow visualization
- Core values

## 🔗 Preview Access

### Local Development
- **Main URL**: `http://localhost:3000` (or next available port if 3000 is in use)
- **Network URL**: Available on local network (shown when starting dev server)

### Port Configuration
The preview scripts **always** automatically detect and use an available port starting from 3000. This ensures that the preview will never fail due to port conflicts. If port 3000 is already in use (e.g., by another application), the script will automatically find and use the next available port (3001, 3002, etc., up to 3100).

**Automatic port detection runs every time** to guarantee a free port is always available, preventing any conflicts with other applications or services.

## 🛠️ Development Tools

### Browser DevTools
- React DevTools extension recommended
- Network tab for API monitoring
- Console for debugging

### Hot Reload
The development server includes hot module replacement - changes are reflected immediately without full page reload.

## ℹ️ Additional Information

### Browser Support
- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance
- Production build is optimized and minified
- Code splitting for faster initial load
- CSS is extracted and minimized
- Images are optimized

### Accessibility
- Semantic HTML structure
- ARIA labels where appropriate
- Keyboard navigation support
- Color contrast compliance

## 📞 Support

For issues or questions:
- **GitHub Issues**: [Report a bug](https://github.com/Islamhassana3/OHIPFORWARD/issues)
- **Documentation**: Check `/docs` directory
- **Examples**: Review `/examples` directory

## 🎯 Next Steps

1. Explore all pages and features
2. Test responsive design on different devices
3. Review the code structure in `frontend/src/`
4. Customize styling in CSS files
5. Extend functionality as needed

---

**Note**: The frontend is fully functional for UI demonstration. Backend integration enhances functionality with real-time AI triage and live provider data.
