import { Visiteur } from '../types/Visiteur';

const API_URL = 'http://127.0.0.1:8000';

export async function scannerAudience(): Promise<Visiteur[]> {
  try {
    const response = await fetch(`${API_URL}/audience/audience/live`);
    if (!response.ok) throw new Error(`Erreur API: ${response.status}`);
    const data = await response.json();
    return data.visitors || [];
  } catch (error) {
    console.error("Erreur scannerAudience:", error);
    return [];
  }
}

export async function getRecommandation() {
  try {
    const response = await fetch(`${API_URL}/full/full/recommandation`);
    if (!response.ok) throw new Error(`Erreur API: ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Erreur getRecommandation:", error);
    return null;
  }
}
