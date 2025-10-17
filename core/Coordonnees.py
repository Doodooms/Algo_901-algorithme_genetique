import numpy as np

class coordonnees:
    def __init__(self, coordonnees: np.array):
        self.coordonnees = coordonnees

    def __str__(self):
        return str(self.coordonnees)