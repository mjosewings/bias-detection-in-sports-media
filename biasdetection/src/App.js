import React, { useState, useEffect } from 'react';
import './App.css';

/*  LeagueSelector Component - Handles league selection and video URL input */
function LeagueSelector({ onSelect }) {
  const [step, setStep] = useState('select');
  const [selection, setSelection] = useState('');
  const [videoUrlNBA, setVideoUrlNBA] = useState('');
  const [videoUrlWNBA, setVideoUrlWNBA] = useState('');
  const [videoUrlSingle, setVideoUrlSingle] = useState('');
  const [validationError, setValidationError] = useState(null);

  /* Function to extract video ID from YouTube URL */
  const extractVideoId = (url) => {
    const match = url.match(/(?:v=|\.be\/)([\w-]{11})/);
    return match ? match[1] : null;
  };
  /* Function to handle league selection and URL validation */
  const handleSelection = async (choice) => {
    setSelection(choice);
    setValidationError(null);
  
    if (choice === 'both') {
      const idNBA = extractVideoId(videoUrlNBA);
      const idWNBA = extractVideoId(videoUrlWNBA);
  
      if (!idNBA || !idWNBA) {
        setValidationError('Both YouTube URLs must be valid.');
        return;
      }
  
      setStep('scraping');
      onSelect({ league: 'both', videoId_nba: idNBA, videoId_wnba: idWNBA });
      return;
    }
    
    /* If single league is selected, validate the URL */
    const videoId = extractVideoId(videoUrlSingle);
    if (!videoId) {
      setValidationError('Invalid YouTube URL format.');
      return;
    }
  
    setStep('scraping');
    onSelect({ league: choice, videoId });
  };
  
  /* Function to handle back navigation */
  const handleBack = () => {
    setStep('select');
    setSelection('');
    setVideoUrlNBA('');
    setVideoUrlWNBA('');
    setVideoUrlSingle('');
    setValidationError(null);
  };

  /* Function to handle video URL input change */
  return (
    <div className="league-selector">
      {step === 'select' && (
        <div className="selector">
          <h2>
            {selection === 'both' ? 'Paste NBA and WNBA Video URLs:' : 'Paste a YouTube Video URL:'}
          </h2>

          {selection !== 'both' ? (
            <input
              type="text"
              placeholder="https://youtube.com/...?v=..."
              value={videoUrlSingle}
              onChange={(e) => setVideoUrlSingle(e.target.value)}
              style={{ padding: '0.5rem', width: '60%', marginBottom: '1rem' }}
            />
          ) : (
            <>
              <input
                type="text"
                placeholder="NBA Video URL"
                value={videoUrlNBA}
                onChange={(e) => setVideoUrlNBA(e.target.value)}
                style={{ padding: '0.5rem', width: '60%', marginBottom: '0.5rem' }}
              />
              <input
                type="text"
                placeholder="WNBA Video URL"
                value={videoUrlWNBA}
                onChange={(e) => setVideoUrlWNBA(e.target.value)}
                style={{ padding: '0.5rem', width: '60%', marginBottom: '1rem' }}
              />
            </>
          )}

          <h2>Select League to Analyze:</h2>
          <div className="selector-buttons">
          {selection !== 'both' ? (
            <div>
              <button onClick={() => handleSelection('nba')}>NBA</button>
              <button onClick={() => handleSelection('wnba')}>WNBA</button>
              <button onClick={() => setSelection('both')}>Both (Comparison)</button>
            </div>
          ) : (
            <button onClick={() => handleSelection('both')}>Analyze Both</button>
        )}
      </div>


          {validationError && <p style={{ color: 'red', marginTop: '1rem' }}>{validationError}</p>}
        </div>
      )}

      {step !== 'select' && (
        <div className="back-wrapper">
          <button onClick={handleBack} className="back-button">⬅ Back</button>
        </div>
      )}
    </div>
  );
}

/* App Component - Main application component */
function App() {
  const [visualizations, setVisualizations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectionData, setSelectionData] = useState(null);
  const [activeIndex, setActiveIndex] = useState(null);

  /* Effect to fetch visualizations based on selection data */
  useEffect(() => {
    if (!selectionData) return;
  
    /* Function to fetch visualizations from the backend */
    const fetchVisualizations = async () => {
      try {
        let body;
  
        if (selectionData.league === 'both') {
          body = {
            league: 'both',
            videoId_nba: selectionData.videoId_nba,
            videoId_wnba: selectionData.videoId_wnba,
          };
        } else {
          body = {
            league: selectionData.league,
            videoId: selectionData.videoId,
          };
        }
        
        /* Fetch visualizations from the backend API */
        const response = await fetch('http://localhost:5000/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
  
        const data = await response.json();
        console.log("Backend response:", data);
  
        if (!Array.isArray(data)) {
          setError(data.error || "Unexpected response format.");
          setVisualizations([]);
          return;
        }
  
        setVisualizations(data);
        setError(null);
  
      } catch (err) {
        setError(err.message);
        console.error('Fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
  
    fetchVisualizations();
  }, [selectionData]);
  
  /* Function to handle visualization click */
  return (
    <div className="App">
      <header className="App-header">
        <h1>Basketball Media Bias Visualizations</h1>

        {!selectionData && <LeagueSelector onSelect={setSelectionData} />}

        {selectionData && loading && <div>Loading visualizations...</div>}

        {selectionData && error && (
          <div className="error">
            Error: {error}
            <button onClick={() => window.location.reload()}>Retry</button>
          </div>
        )}
        {selectionData && !loading && !error && (
          <div className="back-wrapper">
            <button className="back-button" onClick={() => window.location.reload()}>
              ⬅ Back
            </button>
          </div>
        )}

        {selectionData && !loading && !error && (
          <div className="visualization-grid">
            {visualizations.map((viz, index) => (
              <div key={index} className="visualization-card" onClick={() => setActiveIndex(index)}>
                <h2>{viz.title}</h2>
                <img 
                  src={`data:image/png;base64,${viz.image}`} 
                  alt={viz.title}
                  className="visualization-image"
                />
              </div>
            ))}
          </div>
        )}

        {activeIndex !== null && (
          <div className="modal" onClick={() => setActiveIndex(null)}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
              <h2>{visualizations[activeIndex].title}</h2>
              <img 
                src={`data:image/png;base64,${visualizations[activeIndex].image}`} 
                alt={visualizations[activeIndex].title}
                style={{ width: '100%', height: 'auto' }}
              />
              <button onClick={() => setActiveIndex(null)}>Close</button>
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
