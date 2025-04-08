import React, { useEffect, useRef, useState } from 'react';
import { scannerAudience } from '../services/api';
import { Visiteur } from '../types/Visiteur';

const AudienceScanner: React.FC = () => {
  const [visiteurs, setVisiteurs] = useState<Visiteur[]>([]);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Erreur d’accès à la caméra :", error);
      }
    };

    const fetchLiveData = async () => {
      try {
        const data = await scannerAudience();
        console.log("📦 Visiteurs détectés :", data); // Pour debug
        setVisiteurs(data);
      } catch (err) {
        console.warn("Erreur lors de l'analyse :", err);
      }
    };

    startCamera();
    const intervalId = setInterval(fetchLiveData, 2000);
    return () => clearInterval(intervalId);
  }, []);

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
          style={{
            width: '100%',
            maxWidth: '100%',
            height: 'auto',
            borderRadius: '8px',
            border: '2px solid #ccc'
          }}
          autoPlay
          muted
        />
        <p style={{ marginTop: '1rem', color: '#555' }}>
          📡 Analyse automatique toutes les 2 secondes
        </p>
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
                <p>📏 Distance : <strong>{v.distance_cm?.toFixed(1) ?? 'N/A'} cm</strong></p>
                <p>👁️ Attention : <strong>{v.temps_attention ?? 0}s</strong></p>
                <p>🚫 Inattention : <strong>{v.temps_inattention ?? 0}s</strong></p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AudienceScanner;
