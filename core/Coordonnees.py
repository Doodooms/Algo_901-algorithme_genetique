from typing import List, Optional, Any


class Coordonnees:
    """
    Classe des coordonnéees des individus.
    Les coordonnées et encoded_coordonnes sont Optionnal.
    Pour la population initiale, les individus seront crées à partir de coordonnees sans les encoded_coord
    Mais pour les enfants, ils seront crées à partir des encoded_coordonnees et les coordonnees
    seront calculées si l'enfant est effectivement sélectionné pour intégrer la population
    """

    def __init__(
        self,
        coordonnees: Optional[List[float]] = None,
        encoded_coordonnees: Optional[List[Any]] = None,
    ):
        self.coordonnees = coordonnees
        self.encoded_coord = encoded_coordonnees

    def __str__(self):
        return str(self.coordonnees)
