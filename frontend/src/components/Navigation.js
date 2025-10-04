import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <span className="logo-icon">🏥</span>
          <span className="logo-text">OHIPFORWARD</span>
        </Link>
        <ul className="nav-menu">
          <li>
            <Link to="/" className={`nav-link ${isActive('/')}`}>
              Home
            </Link>
          </li>
          <li>
            <Link to="/triage" className={`nav-link ${isActive('/triage')}`}>
              Symptom Triage
            </Link>
          </li>
          <li>
            <Link to="/providers" className={`nav-link ${isActive('/providers')}`}>
              Find Providers
            </Link>
          </li>
          <li>
            <Link to="/features" className={`nav-link ${isActive('/features')}`}>
              Features
            </Link>
          </li>
          <li>
            <Link to="/about" className={`nav-link ${isActive('/about')}`}>
              About
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navigation;
