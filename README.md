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

Algo_901-algorithme_genetique/  
│  
├── core/  
│   ├── AlgorithmeGenetique.py   
│   ├── Coordonnees.py  
│   ├── Individu.py  
│   └── Population.py  
│  
└── operators/   
    ├── Codage.py  
    ├── Crossover.py  
    ├── Mutation.py  
    ├── Selection.py  
    └── MantisseExposant.py  

  
## Description des dossiers
### `core/` - Composants centraux

- **AlgorithmeGenetique.py** : Point d'entrée du porjet, centralise toutes les classes et fournit un exemple d'éxécution de l'algorithme.
- **Coordonnees.py** : Gestion des coordonnées des individus (ADN)
- **Individu.py** : Définition d'un individus et propriétés associées (fitness, ...)
- **Population.py** : Gestion d'une population sous forme de liste d'individus. 

### `operators/` - Opérateurs génétiques

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
# Exemple d'utilisation de la classe AlgorithmeGenetique
def exemple_fitness_function(coordonnees: np.ndarray) -> float:
    return -np.sum(coordonnees**2) + 10

# Initialiser les opérateurs
codage = MantisseExposant()
crossover = SimpleCrossover(codage)
mutation = Mutation(0.05, codage)

tournoi = Selection_tournoi(
    None, taille_tournoi=3, taille_selection=10
)  # Population sera définie plus tard

# Créer une instance de l'algorithme génétique
ag = AlgorithmeGenetique(
    population_size=50,
    dimension=2,
    bounds=[(-5, 5), (-5, 5)],
    codage_operator=codage,
    crossover_operator=crossover,
    mutation_operator=mutation,
    selection_operator=tournoi,
    fitness_function=exemple_fitness_function,
    maximize_fitness=True,
    taux_mutation=0.05,
    num_generations=100,
)

# Initialiser la population
ag._initialiser_population()
ag._evaluer_population()
for t in range(
    ag.num_generations
):  # On fait évoluer la  population sur num_generations
    parents = ag._selectionner_parents()
    nouvelle_generation = ag._reproduire(parents)
    ag._remplacer_population(nouvelle_generation)
    ag._evaluer_population()
print(ag.history)

# On vérifie la convergence 
print(f"Le résultat attendu est 10 et le résultat de l'algo est : {ag.history['best_fitness'][-1]}")
```
