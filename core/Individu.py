from core.Coordonnees import Coordonnees

class Individu():
    def __init__(self, id : int, coordonnees : Coordonnees, fitness = None):
        self.id = id 
        self.coordonnees = coordonnees
        self.elite = False 
        self.fitness = fitness

    def __str__(self):
        return f"ID : {self.id}, coordonnées : {self.coordonnees}"
    
    def __repr__(self):
        return f"ID : {self.id}, coordonnées : {self.coordonnees}"
    
if __name__ == "__main__":
    import numpy as np
    c = coordonnees(np.array([1,2,3]))
    c.coordonnees_codees = np.array([1, 0, 0, 1, 0, 1])
    ind = individu(1, c)
    print(ind)