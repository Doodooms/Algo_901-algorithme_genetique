M2 MMAA
PELHATRE Thomas
BLANQUET Faosto
LUAYU Israel
MAILHEBIAU Phoebus
HERAUX Clémence
------
# <center> Algo_901-algorithme_genetique </center>
<center> <i>Ce projet propose une implémentation <b>orientée objet</b> d’un algorithme génétique. Il permet de gérer une population d'individus, d'appliquer des opéarteurs génétiques et de simuler une évolution sur plusieurs générations. </i></center>

------


## Structure du projet


## Description des dossiers
### `core/` - Composants centraux

- **AlgorithmeGenetique.py** : Point d'entrée du porjet, centralise toutes les classes et fournit un exemple d'éxécution de l'algorithme.
- **Coordonnees.py** : Gestion des coordonnées des individus (ADN)
- **Individu.py** : Définition d'un individus et propriétés associées (fitness, ...)
- **Population.py** : Gestion d'une population sous forme de liste d'individus. 

### `operators/` - Composants centraux

- **Codage.py** : Permet de coder les coordonnées d'un individu.
- **Crossover.py** : Permet de croiser l'ADN des individus.
- **Mutation.py** : Permet de créer des mutations génétiques dans l'ADN d'individus
- **Selection.py** : Regroupe différentes méthodes de sélection de parents pour créer de nouveaux individus (roulette, tournoi, naturelle).
- **MantisseExposant.py** : Outil de manipulation numérique utilisant la représentation mantisse/exposant.

## Utilisation

La classe `AlgorithmeGenetique` permet de lancer une simulation complète:
1. Initialisation de la population
2. Selection des individus
3. Croisement
4. Muation
5. Evolution sur plusieurs générations

Exemple :
```python
from core.AlgorithmeGenetique import AlgorithmeGenetique
# Exemple d'utilisation de la classe AlgorithmeGenetique
def exemple_fitness_function(coordonnees: np.ndarray) -> float:
  return -np.sum(coordonnees**2) + 10

  # Initialiser les opérateurs (exemples simples)
  #codage = Codage() # Remplacer par une implémentation concrète
  crossover = SimpleCrossover()
  mutation = Mutation(0.05) # Remplacer par une implémentation concrète
  codage = MantisseExposant()
  tournoi = Selection_tournoi(Population()) # Population sera définie plus tard
  tournoi_params = 5

  # Créer une instance de l'algorithme génétique
  ag = AlgorithmeGenetique(
      population_size=50,
      dimension=2,
      bounds=[(-5, 5), (-5, 5)],
      codage_operator=codage,
      crossover_operator=crossover,
      mutation_operator=mutation,
      selection_operator_type=tournoi,
      fitness_function=exemple_fitness_function,
      maximize_fitness=True,
      taux_mutation=0.05,
      selection_params=tournoi_params,
      taux_crossover=0.7,
      num_generations=100
  )

  # Initialiser la population
  ag._initialiser_population()
  print(ag.population)
  ag._selectionner_parents()
  ag._reproduire()
```
