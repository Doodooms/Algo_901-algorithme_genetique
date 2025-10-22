class Performance:
    from core.Individu import Individu
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def evaluer(self, individu : Individu) -> None:
        """
        Évalue un individu en utilisant la fonction de fitness fournie
        et met à jour son score de performance."""
        return self.fitness_function(individu.coordonnees.coordonnees)