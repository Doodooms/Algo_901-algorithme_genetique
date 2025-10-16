from Coordonnees import coordonnees

class individu():
    def __init__(self, id : int, coordonnees : coordonnees):
        self.id = id # Besoin d'un identifiant unique ???
        self.coordonnees = coordonnees
        self.elite = False # Pour s'amuser lol

    def __str__(self):
        return f"L'individu numéro {self.id} a pour coordonnées : {self.coordonnees}"