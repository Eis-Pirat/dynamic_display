export interface Visiteur {
  id: number;
  genre: string;
  âge_estimé: number;
  émotion?: string;
  posture?: string;
  temps_attention?: string;
  temps_inattention?: string;
  distance_cm?: number;
}
