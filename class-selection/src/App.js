import React, { useEffect, useState } from 'react';
import './App.css';

export default function App() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5000/get-decisions')
      .then(res => res.json())
      .then(data => {
        const parsed = data.map(row => [
          row[0],
          row[1],
          row[2] === '1' ? '1' : '0'
        ]);
        setRows(parsed);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch decisions", err);
        setLoading(false);
      });
  }, []);

  const toggleRow = (index) => {
    const updated = [...rows];
    updated[index][2] = updated[index][2] === '1' ? '0' : '1';
    setRows(updated);
  };

  const handleDone = () => {
    fetch('http://localhost:5000/save-decisions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(rows)
    })
      .then(res => res.json())
      .then(() => alert('Saved!'));
  };

  const handleRefresh = () => {
    fetch('http://localhost:5000/show-all-courses')
      .then(() => {
        window.location.reload();
      })
      .catch((err) => {
        alert("Failed to refresh list");
        console.error(err);
      });
  };

  return (
    <div className="app">
      <h1 className="title">Course Decisions</h1>

      {loading ? (
        <p className="loading">Loading...</p>
      ) : rows.length > 0 ? (
        <div className="tile-grid">
          {rows.map((row, index) => (
            <div
              key={row[0]}
              onClick={() => toggleRow(index)}
              className={`tile ${row[2] === '1' ? 'selected' : ''}`}
            >
              <p className="tile-title">{row[1]}</p>
              <p className="tile-status">
                {row[2] === '1' ? '✅' : '❌'}
              </p>
            </div>
          ))}
          <div className="full-width">
            <button onClick={handleDone} className="done-button">
              Done
            </button>
            <button onClick={handleRefresh} className="refresh-button">
              Refresh List
            </button>
          </div>
        </div>
      ) : (
        <div className="empty-state">
          <p>No courses found.</p>
          <button onClick={handleRefresh} className="refresh-button">
            Refresh List
          </button>
        </div>
      )}
    </div>
  );
}
