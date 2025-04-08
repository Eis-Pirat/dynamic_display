import React, { useEffect, useRef, useState } from 'react';
import { scannerAudience, getRecommandation } from '../services/api';
import { Visiteur } from '../types/Visiteur';

interface RecoResponse {
  recommandation: string[];
  images: string[];
  profil: {
    genre: string;
    âge_estimé: number;
    émotion: string;
  };
}

const AudienceScanner: React.FC = () => {
  const [visiteurs, setVisiteurs] = useState<Visiteur[]>([]);
  const [reco, setReco] = useState<RecoResponse | null>(null);
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
        setVisiteurs(data);

        if (data.length > 0) {
          const recoResponse = await getRecommandation();
          setReco(recoResponse);
          console.log("🎯 Recommandation CIH :", recoResponse);
        } else {
          setReco(null);
        }
      } catch (err) {
        console.warn("Erreur :", err);
      }
    };

    startCamera();
    const intervalId = setInterval(fetchLiveData, 3000);
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
        <h2>🎥 Caméra en direct</h2>
        <video
          ref={videoRef}
          style={{ width: '100%', borderRadius: '8px', border: '2px solid #ccc' }}
          autoPlay
          muted
        />
        <p style={{ marginTop: '1rem', color: '#555' }}>📱 Analyse automatique toutes les 3 secondes</p>
      </div>

      {/* 📊 Résultats */}
      <div style={{
        flex: 1.2,
        backgroundColor: '#fff',
        padding: '1rem',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <h2>📊 Résultats</h2>
        {visiteurs.length === 0 ? (
          <p style={{ color: '#888' }}>Aucun visiteur détecté</p>
        ) : (
          <div>
            <p><strong>👤 Profil détecté</strong></p>
            <p>🧜 Genre : {reco?.profil.genre ?? '...'}</p>
            <p>🎂 Âge estimé : {reco?.profil.âge_estimé ?? '...'} ans</p>
            <p>😊 Émotion : {reco?.profil.émotion ?? '...'}</p>
            <p>🧕 Posture : {visiteurs[0]?.posture ?? 'Inconnue'}</p>
            <p>📏 Distance : {visiteurs[0]?.distance_cm?.toFixed(1) ?? 'N/A'} cm</p>
            <p>👁️ Attention : {visiteurs[0]?.temps_attention ?? 0}s</p>
            <p>❌ Inattention : {visiteurs[0]?.temps_inattention ?? 0}s</p>
          </div>
        )}

        {/* 🏱 Recommandations */}
        {reco && reco.recommandation.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h3>🏱 Recommandations CIH</h3>
            <ul>
              {reco.recommandation.map((r, index) => (
                <li key={index} style={{ marginBottom: '0.5rem' }}>{r}</li>
              ))}
            </ul>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginTop: '1rem' }}>
              {reco.images.map((img, index) => (
                <img
                  key={index}
                  src={`http://127.0.0.1:8000${img}`}
                  alt={`Offre ${index}`}
                  style={{ width: '200px', borderRadius: '8px', border: '1px solid #ddd' }}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AudienceScanner;