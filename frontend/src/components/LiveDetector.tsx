import React, { useEffect, useRef, useState } from 'react';
import { envoyerImage } from '../services/audience';
import { getAdRecommendation } from '../services/recommendation'; // ✅ NEW

const adImageMap: Record<string, string> = { // ✅ NEW
  ad_code18: "http://127.0.0.1:8000/static/images/code18-big.jpg",
  ad_code30: "http://127.0.0.1:8000/static/images/code30.jpg",
  ad_code212: "http://127.0.0.1:8000/static/images/code212.jpg",
  ad_duo: "http://127.0.0.1:8000/static/images/offreduoo.jpg",
  ad_raha: "http://127.0.0.1:8000/static/images/raha.jpeg",
  ad_sayidati: "http://127.0.0.1:8000/static/images/sayidati.jpg",
};

const LiveDetector: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [data, setData] = useState<any>(null);
  const [ad, setAd] = useState<string | null>(null); // ✅ NEW

  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (error) {
        console.error("Erreur d'accès à la caméra :", error);
      }
    };

    const analyze = async () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (!video || !canvas) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(async (blob) => {
        if (!blob) return;
        try {
          const result = await envoyerImage(blob);
          setData(result);

          // ✅ Request ad recommendation when analysis is ready
          if (result.genre && result.âge_estimé && result.émotion) {
            const adLabel = await getAdRecommendation(result.genre, result.âge_estimé, result.émotion);
            setAd(adLabel);
          }

        } catch (err) {
          console.warn("Erreur d'analyse :", err);
        }
      }, 'image/jpeg');
    };

    startCamera();
    const intervalId = setInterval(analyze, 4000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'row', padding: '2rem', backgroundColor: '#f9fafb', fontFamily: 'Segoe UI, sans-serif', gap: '2rem', minHeight: '100vh' }}>
      {/* Caméra */}
      <div style={{ flex: 1, backgroundColor: '#fff', padding: '1rem', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h2>🎥 Caméra en direct</h2>
        <video ref={videoRef} autoPlay muted style={{ width: '100%', borderRadius: '8px', border: '2px solid #ccc' }} />
        <canvas ref={canvasRef} style={{ display: 'none' }} />
        <p style={{ marginTop: '1rem', color: '#555' }}>📸 Capture toutes les 4 secondes</p>
      </div>

      {/* Résultats + Ad */}
      <div style={{ flex: 1.2, backgroundColor: '#fff', padding: '1rem', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h2>📊 Résultats</h2>
        {!data ? (
          <p style={{ color: '#888' }}>🙈 Analyse en attente...</p>
        ) : (
          <div>
            <p><strong>🧜 Genre :</strong> {data.genre}</p>
            <p><strong>🎂 Âge estimé :</strong> {data.âge_estimé} ans</p>
            <p><strong>😊 Émotion :</strong> {data.émotion}</p>
            <p><strong>🧕 Posture :</strong> {data.posture}</p>
            <p><strong>📏 Distance :</strong> {data.distance_cm ? `${data.distance_cm.toFixed(1)} cm` : 'N/A'}</p>

            <h3>👗 Style vestimentaire</h3>
            <p><strong>🌈 Style :</strong> {data.style_vestimentaire?.style}</p>
            <p><strong>🌟 Couleur dominante :</strong> {data.style_vestimentaire?.couleur}</p>
            <p><strong>🌆 Motif :</strong> {data.style_vestimentaire?.motif}</p>
            <p><strong>🧱 Texture :</strong> {data.style_vestimentaire?.texture}</p>

            {ad && (
              <>
                <h3 style={{ marginTop: '2rem' }}>🎯 Publicité recommandée :</h3>
                <img
                  src={adImageMap[ad]}
                  alt="Ad"
                  style={{ width: '100%', maxWidth: '400px', borderRadius: '10px', marginTop: '1rem' }}
                />
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default LiveDetector;
