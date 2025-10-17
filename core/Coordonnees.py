import numpy as np

class coordonnees:
    def __init__(self, coordonnees: np.array, coordonnees_codees: np.array):
        self.coordonnees = coordonnees
        self.coordonnees_codees = coordonnees_codees

    def __str__(self):
        return str(self.coordonnees)