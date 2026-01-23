from abc import ABC, abstractmethod
from core.Coordonnees import Coordonnees
import numpy as np


class Codage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def code(self, coord: Coordonnees):
        """
        Fonction qui prends les coordonnées réelles et les encode pour pouvoir faire les autres opérations de l'algo génétique
        """
        pass


class CodageBinaire(Codage):
    def code(self, coord: Coordonnees):
        # Exemple simple
        coord.coordonnees_codees =  np.array([bin(int(v)) for v in coord.valeurs])


class CodageReel(Codage):
    def code(self, coord: Coordonnees):
        """ "
        Transforme chaque élément de la liste en float
        """
        coord.coordonnees_codees = coord.valeurs.astype(float)

if __name__ == "__main__":
    x = np.array([1, 2.5, 3, 4.7])
    coord = Coordonnees(x)

    codage_reel = CodageReel()
    codage_binaire = CodageBinaire()

    codage_reel.code(coord)
    print(coord)
    
    codage_binaire.code(coord)
    print(coord)
