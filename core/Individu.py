from Coordonnees import Coordonnees


class Individu:
    def __init__(self, coordonnees: Coordonnees):
        self.coordonnees = coordonnees
        self.elite = False  # Pour s'amuser lol

    def __str__(self):
        return f"L'individu numéro a pour coordonnées : {self.coordonnees}"
