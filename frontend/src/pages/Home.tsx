import React, { useState } from 'react';
import { scannerAudience } from '../services/api';
import { Visiteur } from '../types/Visiteur';

const Home: React.FC = () => {
  const [visiteurs, setVisiteurs] = useState<Visiteur[]>([]);
  const [loading, setLoading] = useState(false);

  const handleScan = async () => {
    setLoading(true);
    const data = await scannerAudience();
    setVisiteurs(data);
    setLoading(false);
  };

  return (
    <div className='p-4'>
      <h1>Système Intelligent</h1>
      <button onClick={handleScan} disabled={loading}>
        {loading ? 'Scan en cours...' : 'Scanner les Visiteurs'}
      </button>
      <ul>
        {visiteurs.map((v) => (
          <li key={v.id}>
            👤 {v.genre} — {v.âge_estimé} ans
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Home;
