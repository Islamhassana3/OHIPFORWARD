import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Triage from './pages/Triage';
import Providers from './pages/Providers';
import Features from './pages/Features';
import About from './pages/About';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/triage" element={<Triage />} />
          <Route path="/providers" element={<Providers />} />
          <Route path="/features" element={<Features />} />
          <Route path="/about" element={<About />} />
        </Routes>
        <footer className="App-footer">
          <p>© 2024 OHIPFORWARD - Ontario Healthcare Network</p>
          <p className="footer-links">
            <a href="https://github.com/Islamhassana3/OHIPFORWARD" target="_blank" rel="noopener noreferrer">
              GitHub
            </a>
            {' | '}
            <a href="https://github.com/Islamhassana3/OHIPFORWARD/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">
              MIT License
            </a>
          </p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
