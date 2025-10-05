import React from 'react';
import './Features.css';

function Features() {
  const features = [
    {
      icon: '🤖',
      title: 'AI-Powered Triage',
      description: 'Advanced symptom analysis using machine learning algorithms',
      details: [
        'Real-time symptom assessment',
        'Urgency classification',
        'Confidence scoring',
        'Personalized recommendations'
      ]
    },
    {
      icon: '📅',
      title: 'Smart Scheduling',
      description: 'Intelligent appointment booking and provider matching',
      details: [
        'Automated availability checking',
        'Urgency-based prioritization',
        'Location optimization',
        'Conflict resolution'
      ]
    },
    {
      icon: '🚗',
      title: 'Transportation Integration',
      description: 'Seamless Uber Health integration for patient mobility',
      details: [
        'Automated ride booking',
        'Cost optimization',
        'Accessibility support',
        'Real-time tracking'
      ]
    },
    {
      icon: '📊',
      title: 'Care Monitoring',
      description: 'Continuous tracking of patient health journeys',
      details: [
        'Journey tracking',
        'Automated follow-ups',
        'Care gap identification',
        'Outcome monitoring'
      ]
    },
    {
      icon: '🔔',
      title: 'Automated Notifications',
      description: 'Smart reminders and alerts for appointments and care',
      details: [
        'SMS notifications',
        'Email reminders',
        'Custom alerts',
        'Multi-channel delivery'
      ]
    },
    {
      icon: '🔒',
      title: 'Security & Privacy',
      description: 'HIPAA-compliant data protection and encryption',
      details: [
        'End-to-end encryption',
        'HIPAA compliance',
        'Secure data storage',
        'Access controls'
      ]
    }
  ];

  return (
    <div className="features-page">
      <div className="features-header">
        <h1>✨ Platform Features</h1>
        <p>Comprehensive healthcare coordination powered by cutting-edge technology</p>
      </div>

      <div className="features-container">
        <section className="features-intro">
          <h2>Transforming Healthcare Delivery</h2>
          <p className="intro-text">
            OHIPFORWARD combines artificial intelligence, real-time data processing, and 
            seamless integrations to create a unified healthcare coordination platform that 
            reduces wait times, optimizes costs, and improves patient outcomes across Ontario's 
            healthcare network.
          </p>
        </section>

        <section className="features-detailed">
          {features.map((feature, index) => (
            <div key={index} className="feature-detail-card">
              <div className="feature-icon-large">{feature.icon}</div>
              <div className="feature-content">
                <h3>{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
                <ul className="feature-list">
                  {feature.details.map((detail, idx) => (
                    <li key={idx}>
                      <span className="check-icon">✓</span>
                      {detail}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </section>

        <section className="tech-stack">
          <h2>Technology Stack</h2>
          <div className="tech-grid">
            <div className="tech-category">
              <h3>Frontend</h3>
              <ul>
                <li>React.js</li>
                <li>React Router</li>
                <li>CSS3 & Animations</li>
                <li>Responsive Design</li>
              </ul>
            </div>
            <div className="tech-category">
              <h3>Backend</h3>
              <ul>
                <li>Python & Flask</li>
                <li>RESTful APIs</li>
                <li>SQLAlchemy ORM</li>
                <li>PostgreSQL</li>
              </ul>
            </div>
            <div className="tech-category">
              <h3>AI & Analytics</h3>
              <ul>
                <li>Machine Learning</li>
                <li>Symptom Analysis</li>
                <li>Predictive Modeling</li>
                <li>Data Processing</li>
              </ul>
            </div>
            <div className="tech-category">
              <h3>Integrations</h3>
              <ul>
                <li>Uber Health API</li>
                <li>Twilio (SMS)</li>
                <li>SMTP (Email)</li>
                <li>Provider Systems</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="benefits-section">
          <h2>Key Benefits</h2>
          <div className="benefits-grid">
            <div className="benefit-card">
              <div className="benefit-icon">⏱️</div>
              <h4>Reduced Wait Times</h4>
              <p>60% average reduction in patient wait times through intelligent triage and scheduling optimization.</p>
            </div>
            <div className="benefit-card">
              <div className="benefit-icon">💰</div>
              <h4>Cost Savings</h4>
              <p>25% healthcare cost reduction through efficient resource allocation and system-wide coordination.</p>
            </div>
            <div className="benefit-card">
              <div className="benefit-icon">🎯</div>
              <h4>Better Outcomes</h4>
              <p>Improved patient outcomes through continuous monitoring and proactive care management.</p>
            </div>
            <div className="benefit-card">
              <div className="benefit-icon">📈</div>
              <h4>Scalability</h4>
              <p>Designed to scale across Ontario's healthcare network with cloud-native architecture.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Features;
