# Quick Deployment & Preview Guide

## 🚀 One-Command Preview

### For Local Development:

```bash
# Clone the repository
git clone https://github.com/Islamhassana3/OHIPFORWARD.git
cd OHIPFORWARD/frontend

# Install and run
npm install && npm start
```

The application will open automatically at `http://localhost:3000`

## 🌐 Deploy to Netlify (Free Hosting)

### Option 1: Using Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build the project
cd frontend
npm run build

# Deploy
netlify deploy --prod --dir=build
```

### Option 2: Using Netlify Dashboard

1. Fork the repository on GitHub
2. Go to [Netlify](https://netlify.com)
3. Click "New site from Git"
4. Select your forked repository
5. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
6. Click "Deploy site"

Your site will be live at: `https://[your-site-name].netlify.app`

## 🔷 Deploy to Vercel (Free Hosting)

### Using Vercel CLI:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel
```

### Using Vercel Dashboard:

1. Go to [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Framework**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. Deploy

Your site will be live at: `https://[your-project].vercel.app`

## 📦 Deploy to GitHub Pages

1. **Update package.json:**

```json
{
  "homepage": "https://[your-username].github.io/OHIPFORWARD"
}
```

2. **Install gh-pages:**

```bash
cd frontend
npm install --save-dev gh-pages
```

3. **Add deploy scripts to package.json:**

```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

4. **Deploy:**

```bash
npm run deploy
```

Your site will be live at: `https://[your-username].github.io/OHIPFORWARD`

## 🐳 Docker Deployment

### Build and Run:

```bash
# From project root
docker-compose up -d
```

Frontend will be available at `http://localhost:3000`
Backend will be available at `http://localhost:5000`

## ☁️ Cloud Deployment Options

### AWS S3 + CloudFront

```bash
# Build the app
cd frontend
npm run build

# Upload to S3 (requires AWS CLI)
aws s3 sync build/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### Google Cloud Platform

```bash
# Build the app
cd frontend
npm run build

# Deploy to Firebase Hosting
firebase deploy
```

### Azure Static Web Apps

1. Push code to GitHub
2. Go to Azure Portal
3. Create a new Static Web App
4. Connect to GitHub repository
5. Set build configuration:
   - **App location**: `/frontend`
   - **Output location**: `build`

## 🔗 Preview URLs

After deployment, your UI will be accessible at:

- **Local**: `http://localhost:3000`
- **Netlify**: `https://[site-name].netlify.app`
- **Vercel**: `https://[project-name].vercel.app`
- **GitHub Pages**: `https://[username].github.io/OHIPFORWARD`

## 📱 Mobile Preview

To preview on mobile devices on the same network:

1. Start the development server: `npm start`
2. Note the "On Your Network" URL (e.g., `http://192.168.1.100:3000`)
3. Open this URL on your mobile device

## 🎯 Quick Testing

After deployment, test these URLs:

- `/` - Home page
- `/triage` - Symptom assessment
- `/providers` - Healthcare providers
- `/features` - Platform features
- `/about` - About page

## 📊 Performance Optimization

For production deployments:

```bash
# Build with production optimizations
cd frontend
npm run build

# Analyze bundle size
npm install -g source-map-explorer
source-map-explorer build/static/js/*.js
```

## 🔒 Environment Configuration

For production deployment with backend:

1. Create `.env.production` in frontend:

```env
REACT_APP_API_URL=https://your-backend-api.com
```

2. Update API calls to use environment variable:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

## 🆘 Troubleshooting

### Build Fails

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Port Already in Use

```bash
# Use different port
PORT=3001 npm start
```

### Deployment Issues

- Check build logs for errors
- Verify build directory is correct
- Ensure all dependencies are in package.json
- Check for environment-specific issues

## 📚 Additional Resources

- **Full Preview Guide**: [PREVIEW.md](PREVIEW.md)
- **Project Documentation**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)

## ✨ Features Available in Preview

✅ Full UI/UX with 5 pages
✅ Responsive design (mobile, tablet, desktop)
✅ Navigation and routing
✅ Sample provider data
✅ Interactive forms
✅ Animations and transitions
✅ Modern design system

## 🎉 Ready to Explore!

Choose any deployment method above and start exploring the OHIPFORWARD healthcare coordination platform!

For questions or issues, visit: [GitHub Issues](https://github.com/Islamhassana3/OHIPFORWARD/issues)
