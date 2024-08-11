import React, { useState, useEffect } from 'react';
import './App.css';

function LiveStream() {
  const [detectionResults, setDetectionResults] = useState({});
  const [dateTime, setDateTime] = useState(new Date());
  const [location, setLocation] = useState({ lat: null, lon: null });

  useEffect(() => {
    const intervalId = setInterval(() => {
      console.log("Attempting to fetch detection results...");
      fetch('http://localhost:5001/detection_results')
        .then(response => {
          console.log("Response received:", response);
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log("Fetched detection results:", data);
          setDetectionResults(data); 
        })
        .catch(error => console.error('Error fetching detection results:', error));

      setDateTime(new Date());
    }, 1000); 

    // Get location
    navigator.geolocation.getCurrentPosition((position) => {
      setLocation({
        lat: position.coords.latitude.toFixed(4),
        lon: position.coords.longitude.toFixed(4)
      });
    });

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="live-stream-container">
      <header>
        <h1>Real-Time Object Detection</h1>
        <div className="info-bar">
          <span>{dateTime.toLocaleString()}</span>
          {location.lat && location.lon && (
            <span> | Lat: {location.lat} Lon: {location.lon}</span>
          )}
        </div>
      </header>
      <div className="video-container">
        <img src="http://localhost:5001/video_feed" alt="Live Stream" />
      </div>
      <div className="detection-results">
        <h2>Detected Objects:</h2>
        {Object.keys(detectionResults).length > 0 ? (
          <ul>
            {Object.entries(detectionResults).map(([label, count], index) => (
              <li key={index}>{count} {label}</li>
            ))}
          </ul>
        ) : (
          <p>No objects detected</p>
        )}
      </div>
      <footer>
        Developed by Mahedi Hasan
      </footer>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <LiveStream />
    </div>
  );
}

export default App;
