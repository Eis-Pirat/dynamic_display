// src/components/AudienceScanner.tsx

import React, { useState } from 'react';

function AudienceScanner() {
  const [resultat, setResultat] = useState<any>(null);

  const handleScan = async () => {
    try {
      const res = await fetch('http://localhost:8000/audience/audience/scan');
      const data = await res.json();
      setResultat(data);
    } catch (err) {
      alert("Erreur lors de la détection");
    }
  };

  return (
    <div className="container">
      <h1>Scanner l'Audience</h1>
      <button onClick={handleScan}>Scanner maintenant</button>

      {resultat && (
        <div style={{ marginTop: '20px' }}>
          <h2>Résultat</h2>
          <pre>{JSON.stringify(resultat, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default AudienceScanner;
    