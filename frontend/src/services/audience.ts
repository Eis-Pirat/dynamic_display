export async function envoyerImage(blob: Blob) {
    const formData = new FormData();
    formData.append('file', blob, 'capture.jpg');
  
    const res = await fetch('http://127.0.0.1:8000/audience/analyze-image', {
      method: 'POST',
      body: formData,
    });
  
    if (!res.ok) throw new Error('Erreur de l’analyse');
    return await res.json();
  }
  