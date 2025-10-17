from Individu import Individu


class Population:
    def __init__(self, liste_individus: list[Individu]):
        self.liste_individus = liste_individus

    def __str__(self):
        return f"La population est composée des individus suivants : {self.liste_individus}"
