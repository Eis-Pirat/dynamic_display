def recommander_contenu(genre: str, age: int) -> dict:
    if genre == "Homme":
        if age < 25:
            contenu = "Casques gaming & sneakers tendance"
        elif age < 40:
            contenu = "Montres connectées et gadgets tech"
        else:
            contenu = "Golf, voitures de luxe et whisky premium"
    else:
        if age < 25:
            contenu = "Soins de peau & accessoires de mode"
        elif age < 40:
            contenu = "Fitness, bien-être et parentalité"
        else:
            contenu = "Beauté anti-âge & voyages bien-être"

    return {
        "recommandation": contenu,
        "profil": {"genre": genre, "âge": age}
    }
