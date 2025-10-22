import numpy as np

class Coordonnees:
    def __init__(self, coordonnees: np.array):
        self.coordonnees = coordonnees
        self.coordonnees_codees = None

    def __str__(self):
        return f"Coordonnées : {self.coordonnees}, Coordonnées codées : {self.coordonnees_codees}"
    
if __name__ == "__main__":
    c = Coordonnees(np.array([1.5, 2.5, 3.5]))
    print(c)
    c.coordonnees_codees = np.array([1, 0, 1, 0, 1, 0])
    print(c)