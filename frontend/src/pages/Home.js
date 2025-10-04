import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Welcome to OHIPFORWARD</h1>
          <p className="hero-subtitle">
            Transforming Healthcare Through AI-Powered Coordination
          </p>
          <p className="hero-description">
            Experience seamless healthcare coordination with intelligent symptom assessment,
            smart scheduling, and integrated transportation services.
          </p>
          <div className="hero-buttons">
            <Link to="/triage" className="btn btn-primary">
              Get Started
            </Link>
            <Link to="/about" className="btn btn-secondary">
              Learn More
            </Link>
          </div>
        </div>
      </section>

      <section className="stats-showcase">
        <div className="container">
          <h2 className="section-title">System Impact</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-icon">⏱️</div>
              <div className="stat-value">60%</div>
              <div className="stat-label">Wait Time Reduction</div>
              <p className="stat-description">
                Average reduction in patient wait times through AI optimization
              </p>
            </div>
            <div className="stat-item">
              <div className="stat-icon">💰</div>
              <div className="stat-value">25%</div>
              <div className="stat-label">Cost Savings</div>
              <p className="stat-description">
                Healthcare cost reduction through efficient resource allocation
              </p>
            </div>
            <div className="stat-item">
              <div className="stat-icon">🌐</div>
              <div className="stat-value">100%</div>
              <div className="stat-label">System Coverage</div>
              <p className="stat-description">
                Complete integration across Ontario's healthcare network
              </p>
            </div>
            <div className="stat-item">
              <div className="stat-icon">🤖</div>
              <div className="stat-value">24/7</div>
              <div className="stat-label">AI Availability</div>
              <p className="stat-description">
                Round-the-clock intelligent triage and care coordination
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="features-preview">
        <div className="container">
          <h2 className="section-title">Core Features</h2>
          <div className="features-grid">
            <div className="feature-item">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Triage</h3>
              <p>
                Advanced symptom analysis with real-time urgency classification
                and personalized care recommendations.
              </p>
              <Link to="/triage" className="feature-link">
                Try Now →
              </Link>
            </div>
            <div className="feature-item">
              <div className="feature-icon">📅</div>
              <h3>Smart Scheduling</h3>
              <p>
                Automated appointment booking with intelligent provider matching
                based on urgency and availability.
              </p>
              <Link to="/providers" className="feature-link">
                Find Providers →
              </Link>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🚗</div>
              <h3>Transportation Integration</h3>
              <p>
                Seamless Uber Health integration for accessible and optimized
                transportation to appointments.
              </p>
              <Link to="/features" className="feature-link">
                Learn More →
              </Link>
            </div>
            <div className="feature-item">
              <div className="feature-icon">📊</div>
              <h3>Care Monitoring</h3>
              <p>
                Continuous tracking of patient journeys with automated follow-ups
                and care gap identification.
              </p>
              <Link to="/features" className="feature-link">
                Explore →
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Transform Your Healthcare Experience?</h2>
          <p>Start your journey with intelligent healthcare coordination today.</p>
          <Link to="/triage" className="btn btn-large">
            Start Symptom Assessment
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Home;
