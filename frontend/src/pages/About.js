import React from 'react';
import './About.css';

function About() {
  return (
    <div className="about-page">
      <div className="about-header">
        <h1>ℹ️ About OHIPFORWARD</h1>
        <p>Transforming healthcare coordination for Ontario</p>
      </div>

      <div className="about-container">
        <section className="mission-section">
          <h2>Our Mission</h2>
          <p className="mission-text">
            OHIPFORWARD is dedicated to revolutionizing healthcare coordination in Ontario by 
            leveraging artificial intelligence and modern technology to create seamless patient 
            experiences, reduce wait times, and optimize healthcare resource utilization across 
            the entire healthcare network.
          </p>
        </section>

        <section className="vision-section">
          <div className="vision-content">
            <div className="vision-text">
              <h2>Our Vision</h2>
              <p>
                We envision a healthcare system where every patient receives timely, coordinated, 
                and personalized care through intelligent automation and seamless integration of 
                healthcare services.
              </p>
              <ul className="vision-points">
                <li>✓ Zero wait time barriers</li>
                <li>✓ Intelligent care coordination</li>
                <li>✓ Accessible healthcare for all</li>
                <li>✓ Data-driven decision making</li>
              </ul>
            </div>
            <div className="vision-graphic">
              <div className="graphic-item">🏥</div>
              <div className="graphic-item">🤖</div>
              <div className="graphic-item">👥</div>
              <div className="graphic-item">📊</div>
            </div>
          </div>
        </section>

        <section className="impact-section">
          <h2>Our Impact</h2>
          <div className="impact-grid">
            <div className="impact-stat">
              <div className="impact-number">60%</div>
              <div className="impact-label">Reduction in Wait Times</div>
              <p>Through intelligent triage and optimized scheduling</p>
            </div>
            <div className="impact-stat">
              <div className="impact-number">25%</div>
              <div className="impact-label">Cost Savings</div>
              <p>Via efficient resource allocation and coordination</p>
            </div>
            <div className="impact-stat">
              <div className="impact-number">100%</div>
              <div className="impact-label">System Coverage</div>
              <p>Comprehensive integration across Ontario's network</p>
            </div>
            <div className="impact-stat">
              <div className="impact-number">24/7</div>
              <div className="impact-label">AI Availability</div>
              <p>Round-the-clock intelligent care coordination</p>
            </div>
          </div>
        </section>

        <section className="how-it-works">
          <h2>How It Works</h2>
          <div className="workflow-steps">
            <div className="workflow-step">
              <div className="step-number">1</div>
              <h3>Patient Assessment</h3>
              <p>
                Patients enter their symptoms through our intuitive interface. Our AI engine 
                analyzes the information and determines urgency level.
              </p>
            </div>
            <div className="workflow-arrow">→</div>
            <div className="workflow-step">
              <div className="step-number">2</div>
              <h3>Smart Matching</h3>
              <p>
                The system intelligently matches patients with appropriate healthcare providers 
                based on urgency, specialty, location, and availability.
              </p>
            </div>
            <div className="workflow-arrow">→</div>
            <div className="workflow-step">
              <div className="step-number">3</div>
              <h3>Coordination</h3>
              <p>
                Automated appointment booking, transportation arrangement, and continuous 
                care monitoring ensure seamless healthcare delivery.
              </p>
            </div>
          </div>
        </section>

        <section className="team-section">
          <h2>Built for Ontario</h2>
          <p className="team-description">
            OHIPFORWARD is an open-source project designed specifically for Ontario's healthcare 
            network. We're committed to improving healthcare accessibility, reducing system strain, 
            and ensuring every patient receives timely, quality care.
          </p>
          <div className="values-grid">
            <div className="value-card">
              <div className="value-icon">🎯</div>
              <h4>Patient-Centered</h4>
              <p>Every decision prioritizes patient needs and outcomes</p>
            </div>
            <div className="value-card">
              <div className="value-icon">🔒</div>
              <h4>Privacy & Security</h4>
              <p>HIPAA-compliant with end-to-end encryption</p>
            </div>
            <div className="value-card">
              <div className="value-icon">🌐</div>
              <h4>Open Source</h4>
              <p>Transparent, collaborative, and community-driven</p>
            </div>
            <div className="value-card">
              <div className="value-icon">⚡</div>
              <h4>Innovation</h4>
              <p>Leveraging cutting-edge AI and technology</p>
            </div>
          </div>
        </section>

        <section className="cta-about">
          <h2>Join Us in Transforming Healthcare</h2>
          <p>
            Whether you're a patient, healthcare provider, or developer, OHIPFORWARD is here 
            to make healthcare coordination seamless and efficient.
          </p>
          <div className="cta-buttons">
            <a href="https://github.com/Islamhassana3/OHIPFORWARD" target="_blank" rel="noopener noreferrer" className="btn-github">
              <span>⭐</span> Star on GitHub
            </a>
            <a href="https://github.com/Islamhassana3/OHIPFORWARD/issues" target="_blank" rel="noopener noreferrer" className="btn-contribute">
              <span>🤝</span> Contribute
            </a>
          </div>
        </section>
      </div>
    </div>
  );
}

export default About;
