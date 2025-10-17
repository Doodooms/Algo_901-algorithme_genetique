from core.Coordonnees import coordonnees


class individu:
    def __init__(self, id: int, coordonnees: coordonnees):
        self.id = id  # Besoin d'un identifiant unique ???
        # Si on en a besoin, il faudrait que cet attribut soit générer automatiquement avec un attribut général pour la classe qui s'incrémente
        self.coordonnees = coordonnees
        self.elite = False  # Pour s'amuser lol

    def __str__(self):
        return f"ID : {self.id}, coordonnées : {self.coordonnees}"


if __name__ == "__main__":
    import numpy as np

    c = coordonnees(np.array([1, 2, 3]))
    c.coordonnees_codees = np.array([1, 0, 0, 1, 0, 1])
    ind = individu(1, c)
    print(ind)
