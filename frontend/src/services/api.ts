
import { Visiteur } from '../types/Visiteur';

const API_URL = 'http://127.0.0.1:8000';

export async function scannerAudience(): Promise<Visiteur[]> {
  const response = await fetch("http://127.0.0.1:8000/audience/audience/live");
  const data = await response.json();
  return data.visitors || [];
}
