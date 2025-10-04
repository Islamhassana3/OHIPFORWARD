import React from 'react';
import './Triage.css';

function Triage() {
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
      alert('Error connecting to server. Please make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="triage-page">
      <div className="triage-header">
        <h1>🩺 Symptom Triage</h1>
        <p>Get intelligent assessment of your symptoms and recommended care actions</p>
      </div>

      <div className="triage-container">
        <section className="triage-form-section">
          <h2>Tell Us About Your Symptoms</h2>
          <form onSubmit={handleTriage} className="triage-form">
            <div className="form-group">
              <label htmlFor="symptoms">
                <span className="label-icon">🔍</span>
                Symptoms (comma-separated)
              </label>
              <input
                type="text"
                id="symptoms"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="e.g., fever, cough, headache, fatigue"
                required
                className="form-input"
              />
              <small className="input-hint">
                Enter multiple symptoms separated by commas
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="duration">
                <span className="label-icon">⏱️</span>
                Duration
              </label>
              <input
                type="text"
                id="duration"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                placeholder="e.g., 3 days, 1 week, 2 hours"
                className="form-input"
              />
              <small className="input-hint">
                How long have you been experiencing these symptoms?
              </small>
            </div>

            <div className="form-group">
              <label htmlFor="severity">
                <span className="label-icon">📊</span>
                Severity Level
              </label>
              <select
                id="severity"
                value={severity}
                onChange={(e) => setSeverity(e.target.value)}
                className="form-select"
              >
                <option value="mild">Mild - Minor discomfort</option>
                <option value="moderate">Moderate - Noticeable impact</option>
                <option value="severe">Severe - Significant distress</option>
              </select>
              <small className="input-hint">
                Rate the severity of your symptoms
              </small>
            </div>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Assessing...
                </>
              ) : (
                <>
                  <span>🤖</span>
                  Assess Symptoms
                </>
              )}
            </button>
          </form>
        </section>

        {result && (
          <section className="result-section">
            <div className="result-header">
              <h2>📋 Assessment Result</h2>
              <div className={`urgency-badge urgency-${result.urgency}`}>
                {result.urgency?.toUpperCase() || 'UNKNOWN'}
              </div>
            </div>
            
            <div className="confidence-bar-container">
              <label>AI Confidence Score</label>
              <div className="confidence-bar">
                <div 
                  className="confidence-fill"
                  style={{ width: `${(result.confidence || 0) * 100}%` }}
                >
                  {((result.confidence || 0) * 100).toFixed(1)}%
                </div>
              </div>
            </div>

            <div className="recommendation-card">
              <h3>💡 Recommended Action</h3>
              <p className="recommendation-text">
                {result.recommendedAction || 'No recommendation available'}
              </p>
            </div>

            {result.nextSteps && result.nextSteps.length > 0 && (
              <div className="next-steps-card">
                <h3>📝 Next Steps</h3>
                <ol className="steps-list">
                  {result.nextSteps.map((step, index) => (
                    <li key={index} className={`step-item priority-${step.priority}`}>
                      <span className="step-number">{index + 1}</span>
                      <span className="step-text">{step.action}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}

            <div className="result-actions">
              <button 
                onClick={() => setResult(null)} 
                className="btn-secondary"
              >
                New Assessment
              </button>
            </div>
          </section>
        )}

        {!result && (
          <section className="info-section">
            <h3>ℹ️ How It Works</h3>
            <div className="info-grid">
              <div className="info-item">
                <div className="info-icon">1️⃣</div>
                <h4>Enter Symptoms</h4>
                <p>Describe your symptoms, their duration, and severity</p>
              </div>
              <div className="info-item">
                <div className="info-icon">2️⃣</div>
                <h4>AI Analysis</h4>
                <p>Our AI engine analyzes your symptoms using medical data</p>
              </div>
              <div className="info-item">
                <div className="info-icon">3️⃣</div>
                <h4>Get Recommendations</h4>
                <p>Receive personalized care recommendations and next steps</p>
              </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

export default Triage;
