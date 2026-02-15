"""
Classe : Selection
Description : Défini plusieurs méthodes de sélection pour obtenir un échantillon de la population
"""

from core.Coordonnees import Coordonnees
from core.Individu import Individu
from core.Population import Population
from operators.Performance import Performance
from abc import ABC, abstractmethod
import numpy as np
import random


class Selection(ABC):
    def __init__(self, population: Population):
        self.population = population
    
    @abstractmethod
    # Oblige à avaoir une méthode selection dans les classes filles
    def selection(self):
        pass


class Selection_tournoi(Selection):
    def __init__(
        self, population: Population, taille_tournoi: int, taille_selection: int
    ):
        super().__init__(population)
        self.taille_tournoi = taille_tournoi
        self.taille_selection = taille_selection

    def selection(self):

        if self.taille_selection > len(self.population.liste_individus):
            raise ValueError(
                "La taille de la sélection dépasse la taille de la population disponible."
            )

        selection = set()
        # Copie de la population pour éviter de modfiier la population originale
        copie_pop = Population(self.population.liste_individus.copy())

        # Réalisation de tournois jusqu'à avoir le nombre d'individus selectionnés souhaité
        while len(selection) < self.taille_selection:

            if len(copie_pop.liste_individus) < self.taille_tournoi:
                print(
                    f"Il n'y a pas assez d'individu pour faire un tournois de taille {self.taille_tournoi}."
                )
                print(
                    f"On réalise le tournois sur les {len(copie_pop.liste_individus)} individus restants."
                )
                participants = copie_pop.liste_individus

            else:
                # Sélection aléatoire de participants au tournoi
                participants = random.sample(
                    copie_pop.liste_individus, self.taille_tournoi
                )

            # Tri des participants selon leur fitness (plus bas = meilleur)
            participants.sort(key=lambda ind: ind.fitness)

            # Ajoute le meilleur individu du tournoi à notre sélection
            selection.add(participants[0])

            # Suppression du meilleur individu dans la copie de la population
            copie_pop.retirer(participants[0])

        return selection


class Selection_roulette(Selection):
    def __init__(self, population: Population, taille_selection: int):
        super().__init__(population)
        self.taille_selection = taille_selection

    def selection(self):

        if self.taille_selection > len(self.population.liste_individus):
            raise ValueError(
                "La taille de la sélection dépasse la taille de la population disponible."
            )

        # Récupération des fitness pour chaque individu
        fitness_values = np.array(
            [ind.fitness for ind in self.population.liste_individus]
        )
        # Somme de tous les fitness
        total_fitness = np.sum(fitness_values)

        # Normalisation de la probabilité d'obtenir chaque individu
        probabilities = fitness_values / total_fitness

        # Calcul des probabilités cumulatives
        cumulative_sum = np.cumsum(probabilities)

        selection = set()

        # Lancement de la roue pour obtenir un individu jusqu'à obtenir la taille de sélection souhaitée
        while len(selection) < self.taille_selection:
            # Tirage aléatoire d'une probabilité selon une loi Uniforme
            r = np.random.uniform(0, 1)

            # Initialisation de l'index pour parcourir la liste d'individu
            index = 0

            # Recherche de l'individu
            while r > cumulative_sum[index]:
                index += 1

            # Récupération de l'individu sélectionné
            individu_selectionne = self.population.liste_individus[index]

            # Ajout de l'individu sélectionné
            selection.add(individu_selectionne)

        return selection


class Selection_naturelle(Selection):

    def __init__(self, population: Population, nb_individu_a_supprimer: int):
        super().__init__(population)
        self.delete = nb_individu_a_supprimer

    def selection(self):

        if self.delete > len(self.population.liste_individus):
            raise ValueError(
                "Le nombre d'individu à supprimer est supérieur à la taille de la population."
            )

        # Tri des individus par fitness croissante
        individus_tries = sorted(
            self.population.liste_individus, key=lambda ind: ind.fitness
        )

        # Sélection des plus faibles
        individus_a_supprimer = individus_tries[: self.delete]

        # Suppression
        self.population.retirer(individus_a_supprimer)
        return self.population.liste_individus


class Selection_Crossover(Selection):

    def __init__(self, population: Population):
        super().__init__(population)

    def selection(self, parent1, parent2, enfant1, enfant2):
        # Regrouper les 4 individus
        candidats = [parent1, parent2, enfant1, enfant2]

        # Trier par fitness décroissante
        meilleurs = sorted(candidats, key=lambda ind: ind.fitness, reverse=True)[:2]

        # Ajoute des enfants à la population
        self.population.ajouter(enfant1)
        self.population.ajouter(enfant2)

        # Retirer les individus avec les moins bons fitness
        ind_a_supprimer = [ind for ind in candidats if ind not in meilleurs]
        self.population.retirer(ind_a_supprimer)


if __name__ == "__main__":

    population = Population(
        [Individu(i, Coordonnees(np.array([1, 0, 0, 1, 0, 1]))) for i in range(10)]
    )

    def carre(x):
        return np.sum(x**2)

    perf = Performance(carre)
    for indiv in population.liste_individus:
        indiv.fitness = perf.evaluer(indiv)
    selection1 = Selection_tournoi(population, 5, 6).selection()
    selection2 = Selection_roulette(population, 5).selection()

    print(selection1)
    print(selection2)