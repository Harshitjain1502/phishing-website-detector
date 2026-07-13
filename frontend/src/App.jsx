import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert, Loader2 } from 'lucide-react';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Sends the URL to your running Flask Backend
      const response = await fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }
      setResult(data);
    } catch (err) {
      setError(err.message || 'Could not connect to Flask server. Make sure app.py is running!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', backgroundColor: '#f3f4f6', minHeight: '100vh', padding: '40px 20px' }}>
      <div style={{ maxWidth: '600px', margin: '0 auto', backgroundColor: '#ffffff', borderRadius: '12px', padding: '32px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}>
        
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{ fontSize: '28px', color: '#1f2937', marginBottom: '8px' }}>🛡️ Phishing Website Detector</h1>
          <p style={{ color: '#6b7280' }}>Analyze URLs instantly using Machine Learning heuristics</p>
        </div>

        {/* Input Form */}
        <form onSubmit={handleAnalyze} style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
          <input
            type="text"
            placeholder="Paste suspicious URL here (e.g., secure-login-bank.com)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ flex: 1, padding: '12px 16px', borderRadius: '8px', border: '1px solid #d1d5db', fontSize: '16px', outline: 'none' }}
          />
          <button
            type="submit"
            disabled={loading}
            style={{ backgroundColor: '#2563eb', color: '#fff', padding: '12px 24px', borderRadius: '8px', border: 'none', fontWeight: 'bold', fontSize: '16px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>

        {error && (
          <div style={{ backgroundColor: '#fee2e2', color: '#dc2626', padding: '12px', borderRadius: '8px', marginBottom: '24px', fontSize: '14px' }}>
            ⚠️ Error: {error}
          </div>
        )}

        {/* Result Dashboard */}
        {result && (
          <div style={{ borderTop: '2px solid #e5e7eb', paddingTop: '24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', padding: '16px', borderRadius: '8px', backgroundColor: result.is_phishing ? '#fee2e2' : '#dcfce7', marginBottom: '24px' }}>
              {result.is_phishing ? <ShieldAlert size={40} color="#dc2626" /> : <ShieldCheck size={40} color="#16a34a" />}
              <div>
                <h3 style={{ margin: 0, fontSize: '20px', color: result.is_phishing ? '#991b1b' : '#166534' }}>
                  {result.is_phishing ? 'Suspicious / Phishing Site' : 'Safe / Legitimate Site'}
                </h3>
                <p style={{ margin: '4px 0 0 0', color: '#4b5563' }}>Phishing Probability: <strong>{result.probability}%</strong></p>
              </div>
            </div>

            <h4 style={{ color: '#374151', marginBottom: '12px' }}>Extracted Heuristic Metrics:</h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '14px', color: '#4b5563' }}>
              <div style={{ padding: '8px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>📏 URL Length: <strong>{result.details.url_length}</strong></div>
              <div style={{ padding: '8px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>🔴 Dots Count: <strong>{result.details.qty_dots}</strong></div>
              <div style={{ padding: '8px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>➖ Hyphens: <strong>{result.details.qty_hyphen}</strong></div>
              <div style={{ padding: '8px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>🔒 Valid SSL: <strong>{result.details.has_valid_ssl ? 'Yes ✅' : 'No ❌'}</strong></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;