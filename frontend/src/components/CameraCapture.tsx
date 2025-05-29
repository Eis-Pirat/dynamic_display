import React, { useRef, useEffect, useState } from 'react';

const CameraCapture = () => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const getCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error('Erreur accès caméra :', err);
      }
    };
    getCamera();
  }, []);

  const captureAndSend = async () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;

    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context?.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
      if (!blob) return;
      const formData = new FormData();
      formData.append('file', blob, 'capture.jpg');

      const res = await fetch('http://127.0.0.1:8000/audience/analyze-image', {
        method: 'POST',
        body: formData,
      });

      const json = await res.json();
      setResult(json);
    }, 'image/jpeg');
  };

  return (
    <div>
      <h2>🎥 Analyse Visiteur via Caméra</h2>
      <video ref={videoRef} autoPlay style={{ width: '400px' }} />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      <br />
      <button onClick={captureAndSend}>Analyser l'image</button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Résultat :</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default CameraCapture;
