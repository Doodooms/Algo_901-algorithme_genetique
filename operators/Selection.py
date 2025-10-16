from core.Individu import individu
from core.Population import population
from abc import ABC, abstractmethod

class selection(ABC):
    def __init__(self, population: population):
        self.population = population
    
    @abstractmethod
    # Oblige à avaoir une méthode selection dans les classes filles
    def selection(self):
        pass
    
class selection_tournoi(selection):
    def __init__(self, population: population):
        self.population = population
    
class selection_roulette(selection):
    def __init__(self, population: population):
        self.population = population