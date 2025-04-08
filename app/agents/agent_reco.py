def recommander_contenu(genre: str, age: int, emotion: str = "neutral") -> dict:
    recommandations = []
    images = []

    # Offres par tranche d'âge
    if age < 18:
        recommandations.append("Offre Code 18")
        images.append("/static/images/code18-big.jpg")
    elif 18 <= age <= 30:
        recommandations.extend(["Pack Intilak", "Carte Code 30"])
        images.append("/static/images/code30-ad.jpg")
        if genre == "Femme":
            recommandations.append("Offre Club Sayidati")
            images.append("/static/images/sayidati.jpg")
        if emotion == "happy":
            recommandations.append("Offre Go / Duo")
            images.append("/static/images/offreduoo.png")
    elif 30 < age <= 45:
        recommandations.extend(["Pack Imtiyaz", "Carte Visa Gold"])
        # (à compléter si une image est dispo)
    else:
        recommandations.extend(["Pack Raha", "Carte Visa Platinum / MasterCard Elite"])
        images.append("/static/images/raha.jpeg")

    # Offres basées sur l’émotion détectée
    if emotion == "angry":
        recommandations.append("Pack Raha (support complet)")
        images.append("/static/images/raha.jpeg")
    elif emotion == "happy":
        recommandations.append("Offre GO ou DUO pour MRE")
        images.append("/static/images/code212.jpg")

    return {
        "recommandation": recommandations,
        "images": images,
        "profil": {"genre": genre, "âge": age, "émotion": emotion}
    }
