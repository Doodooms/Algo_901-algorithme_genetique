from abc import ABC, abstractmethod
from core.Coordonnees import Coordonnees


class Codage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def code(self, coord: Coordonnees):
        """
        Fonction qui prends les coordonnées réelles et les encode pour pouvoir faire les autres opérations de l'algo génétique
        """


class CodageBinaire:
    def code(self, variables):
        # codage binaire pour chaque élément
        # A IMPLEMENTER
        pass


class CodageReel:
    def code(self, variables):
        """ "
        Transforme chaque élément de la liste en float
        """
        variables = [float(variables[i]) for i in range(len(variables))]
        return variables


if __name__ == "__main__":
    x = [1, 2.5, 3, 4.7]
    codagereel = CodageReel()
    codagebinaire = CodageBinaire()
    print(codagereel.code(x))
    print(codagebinaire.code(x))
