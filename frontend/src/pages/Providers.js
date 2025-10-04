import React from 'react';
import './Providers.css';

function Providers() {
  const [providers, setProviders] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [searchTerm, setSearchTerm] = React.useState('');
  const [specialty, setSpecialty] = React.useState('all');

  const loadProviders = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/v1/providers');
      const data = await response.json();
      setProviders(data.providers || []);
    } catch (error) {
      console.error('Error loading providers:', error);
      // Load sample data for demo
      setProviders([
        {
          id: 1,
          name: 'Dr. Sarah Johnson',
          specialty: 'Family Medicine',
          location: 'Toronto General Hospital',
          rating: 4.8,
          availability: 'Available Today',
          waitTime: '2 days'
        },
        {
          id: 2,
          name: 'Dr. Michael Chen',
          specialty: 'Cardiology',
          location: 'Sunnybrook Health Sciences',
          rating: 4.9,
          availability: 'Next Week',
          waitTime: '7 days'
        },
        {
          id: 3,
          name: 'Dr. Emily Rodriguez',
          specialty: 'Pediatrics',
          location: 'SickKids Hospital',
          rating: 4.7,
          availability: 'Available Tomorrow',
          waitTime: '1 day'
        },
        {
          id: 4,
          name: 'Dr. James Wilson',
          specialty: 'Orthopedics',
          location: 'Mount Sinai Hospital',
          rating: 4.6,
          availability: 'Next Month',
          waitTime: '30 days'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  React.useEffect(() => {
    loadProviders();
  }, []);

  const filteredProviders = providers.filter(provider => {
    const matchesSearch = provider.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         provider.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSpecialty = specialty === 'all' || provider.specialty === specialty;
    return matchesSearch && matchesSpecialty;
  });

  const specialties = ['all', ...new Set(providers.map(p => p.specialty))];

  return (
    <div className="providers-page">
      <div className="providers-header">
        <h1>🏥 Find Healthcare Providers</h1>
        <p>Search and connect with qualified healthcare professionals</p>
      </div>

      <div className="providers-container">
        <section className="search-section">
          <div className="search-controls">
            <div className="search-input-group">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                placeholder="Search by name or location..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
            <div className="filter-group">
              <label htmlFor="specialty">Specialty:</label>
              <select
                id="specialty"
                value={specialty}
                onChange={(e) => setSpecialty(e.target.value)}
                className="filter-select"
              >
                {specialties.map(spec => (
                  <option key={spec} value={spec}>
                    {spec === 'all' ? 'All Specialties' : spec}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </section>

        <section className="providers-list">
          {loading ? (
            <div className="loading-state">
              <div className="spinner-large"></div>
              <p>Loading providers...</p>
            </div>
          ) : filteredProviders.length > 0 ? (
            <div className="providers-grid">
              {filteredProviders.map(provider => (
                <div key={provider.id} className="provider-card">
                  <div className="provider-header">
                    <div className="provider-avatar">
                      {provider.name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div className="provider-info">
                      <h3>{provider.name}</h3>
                      <p className="specialty">{provider.specialty}</p>
                    </div>
                  </div>
                  
                  <div className="provider-details">
                    <div className="detail-item">
                      <span className="detail-icon">📍</span>
                      <span>{provider.location}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-icon">⭐</span>
                      <span>{provider.rating} / 5.0</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-icon">⏱️</span>
                      <span>Wait: {provider.waitTime}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-icon">📅</span>
                      <span className="availability">{provider.availability}</span>
                    </div>
                  </div>

                  <div className="provider-actions">
                    <button className="btn-book">Book Appointment</button>
                    <button className="btn-details">View Details</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <h3>No providers found</h3>
              <p>Try adjusting your search criteria</p>
            </div>
          )}
        </section>

        <section className="info-banner">
          <h3>💡 How to Choose a Provider</h3>
          <div className="tips-grid">
            <div className="tip-item">
              <span className="tip-icon">⭐</span>
              <p>Check ratings and reviews from other patients</p>
            </div>
            <div className="tip-item">
              <span className="tip-icon">📍</span>
              <p>Consider location and transportation options</p>
            </div>
            <div className="tip-item">
              <span className="tip-icon">⏱️</span>
              <p>Review wait times and availability</p>
            </div>
            <div className="tip-item">
              <span className="tip-icon">🎯</span>
              <p>Match specialty to your specific needs</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Providers;
