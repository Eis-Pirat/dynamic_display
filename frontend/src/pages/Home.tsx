import React, { useEffect, useRef, useState } from 'react';
import { scannerAudience } from '../services/api';
import { Visiteur } from '../types/Visiteur';

const Home: React.FC = () => {
  const [visiteurs, setVisiteurs] = useState<Visiteur[]>([]);
  const [loading, setLoading] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Erreur caméra :", error);
      }
    };
    startCamera();
  }, []);

  const handleScan = async () => {
    setLoading(true);
    try {
      const data = await scannerAudience();
      setVisiteurs(data);
    } catch (error) {
      alert("Erreur API");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'row',
      padding: '2rem',
      backgroundColor: '#f9fafb',
      fontFamily: 'Segoe UI, sans-serif',
      gap: '2rem',
      minHeight: '100vh'
    }}>
      {/* 🎥 Caméra */}
      <div style={{
        flex: 1,
        backgroundColor: '#fff',
        padding: '1rem',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ marginBottom: '1rem' }}>🎥 Caméra en direct</h2>
        <video
          ref={videoRef}
          width="100%"
          height="auto"
          autoPlay
          muted
          style={{ borderRadius: '8px', border: '2px solid #ccc' }}
        />
        <button
          onClick={handleScan}
          disabled={loading}
          style={{
            marginTop: '1rem',
            padding: '0.75rem 1.5rem',
            backgroundColor: loading ? '#ccc' : '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontWeight: 600
          }}
        >
          {loading ? '🔍 Scan en cours...' : '🚀 Scanner les Visiteurs'}
        </button>
      </div>

      {/* 📊 Résultats */}
      <div style={{
        flex: 1.2,
        backgroundColor: '#fff',
        padding: '1rem',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ marginBottom: '1rem' }}>📊 Résultats</h2>
        {visiteurs.length === 0 ? (
          <p style={{ color: '#555' }}>Aucun visiteur détecté pour l’instant.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {visiteurs.map((v) => (
              <div key={v.id} style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '1rem',
                backgroundColor: '#f3f4f6'
              }}>
                <p><strong>👤 ID {v.id}</strong></p>
                <p>🧬 Genre : <strong>{v.genre}</strong></p>
                <p>🎂 Âge estimé : <strong>{v.âge_estimé} ans</strong></p>
                <p>😊 Émotion : <strong>{v.émotion || 'Inconnue'}</strong></p>
                <p>🧍 Posture : <strong>{v.posture || 'Inconnue'}</strong></p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
