import React, { useState, useEffect } from 'react';

function App() {
  const [correctWord, setCorrectWord] = useState('');
  const [guess, setGuess] = useState('');
  const [attempts, setAttempts] = useState([]);
  const [gameOver, setGameOver] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/start')
      .then(res => res.json())
      .then(data => setCorrectWord(data.correct_word));
  }, []);

  const submitGuess = async (e) => {
    e.preventDefault();
    if (guess.length !== 5) return alert('Guess must be 5 letters!');
    const res = await fetch('http://localhost:8000/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guess, correct_word: correctWord })
    });
    const data = await res.json();
    setAttempts([...attempts, { guess, feedback: data.feedback }]);
    if (data.is_correct || attempts.length + 1 >= 6) setGameOver(true);
    setGuess('');
  };

  return (
    <div className="App" style={{ textAlign: 'center', marginTop: '2rem' }}>
      <h1>🟩 Wordle Clone 🎯</h1>
      <p>Guess the hidden word in six tries!</p>

      {attempts.map((a, i) => (
        <div key={i}>
          {a.feedback.map((symbol, j) => (
            <span key={j} style={{ fontSize: '2rem', margin: '0.3rem' }}>{symbol}</span>
          ))}
        </div>
      ))}

      {!gameOver && (
        <form onSubmit={submitGuess}>
          <input
            value={guess}
            onChange={(e) => setGuess(e.target.value.toUpperCase())}
            maxLength={5}
            placeholder="Enter guess"
          />
          <button type="submit">Submit</button>
        </form>
      )}

      {gameOver && (
        <div>
          <h3>Game Over 💀</h3>
          <p>The word was <b>{correctWord}</b></p>
          <button onClick={() => window.location.reload()}>Play Again 💫</button>
        </div>
      )}
    </div>
  );
}

export default App;
