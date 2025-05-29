// src/services/recommendation.ts
export const getAdRecommendation = async (
  genre: string,
  age: number,
  emotion: string
): Promise<string | null> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/reco/ad", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        genre: genre,
        âge_estimé: age,
        émotion: emotion,
      }),
    });

    const data = await response.json();
    return data.recommandation; // e.g. "ad_code18"
  } catch (error) {
    console.error("API error:", error);
    return null;
  }
};
