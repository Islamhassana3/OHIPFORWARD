import React from 'react';
import './App.css';

function App() {
  const [symptoms, setSymptoms] = React.useState('');
  const [duration, setDuration] = React.useState('');
  const [severity, setSeverity] = React.useState('moderate');
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const handleTriage = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/api/v1/triage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symptoms: symptoms.split(',').map(s => s.trim()),
          duration: duration,
          severity: severity,
        }),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏥 OHIPFORWARD</h1>
        <p>Healthcare Coordination System</p>
      </header>

      <main className="App-main">
        <div className="container">
          <section className="triage-section">
            <h2>Symptom Triage</h2>
            <form onSubmit={handleTriage}>
              <div className="form-group">
                <label htmlFor="symptoms">Symptoms (comma-separated):</label>
                <input
                  type="text"
                  id="symptoms"
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="e.g., fever, cough, headache"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="duration">Duration:</label>
                <input
                  type="text"
                  id="duration"
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  placeholder="e.g., 3 days"
                />
              </div>

              <div className="form-group">
                <label htmlFor="severity">Severity:</label>
                <select
                  id="severity"
                  value={severity}
                  onChange={(e) => setSeverity(e.target.value)}
                >
                  <option value="mild">Mild</option>
                  <option value="moderate">Moderate</option>
                  <option value="severe">Severe</option>
                </select>
              </div>

              <button type="submit" disabled={loading}>
                {loading ? 'Assessing...' : 'Assess Symptoms'}
              </button>
            </form>
          </section>

          {result && (
            <section className="result-section">
              <h2>Assessment Result</h2>
              <div className={`urgency-badge urgency-${result.urgency}`}>
                {result.urgency.toUpperCase()}
              </div>
              <p className="confidence">
                Confidence: {(result.confidence * 100).toFixed(1)}%
              </p>
              <div className="recommendation">
                <h3>Recommended Action:</h3>
                <p>{result.recommendedAction}</p>
              </div>
              <div className="next-steps">
                <h3>Next Steps:</h3>
                <ol>
                  {result.nextSteps.map((step, index) => (
                    <li key={index} className={`priority-${step.priority}`}>
                      {step.action}
                    </li>
                  ))}
                </ol>
              </div>
            </section>
          )}

          <section className="features-section">
            <h2>System Features</h2>
            <div className="features-grid">
              <div className="feature-card">
                <h3>🤖 AI Triage</h3>
                <p>Intelligent symptom assessment with real-time urgency classification</p>
              </div>
              <div className="feature-card">
                <h3>📅 Smart Scheduling</h3>
                <p>Automated appointment booking with optimal provider matching</p>
              </div>
              <div className="feature-card">
                <h3>🚗 Transportation</h3>
                <p>Integrated Uber Health for seamless ride coordination</p>
              </div>
              <div className="feature-card">
                <h3>📊 Care Monitoring</h3>
                <p>Continuous tracking of patient journeys and care gaps</p>
              </div>
            </div>
          </section>

          <section className="stats-section">
            <h2>System Impact</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">60%</div>
                <div className="stat-label">Wait Time Reduction</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">25%</div>
                <div className="stat-label">Cost Savings</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">100%</div>
                <div className="stat-label">System Coverage</div>
              </div>
            </div>
          </section>
        </div>
      </main>

      <footer className="App-footer">
        <p>OHIPFORWARD - Ontario Healthcare Network</p>
      </footer>
    </div>
  );
}

export default App;
