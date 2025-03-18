# Atelier : Redondance des données et calcul distribué

Ce projet illustre la création d'un système de prédiction décentralisé en utilisant Flask. Chaque modèle est exposé via une API, et un client agrège les prédictions pour générer une prédiction consensuelle pondérée. Un mécanisme de pénalités (slashing) est également implémenté pour décourager les prédictions incorrectes.

## Structure du projet

- **`create_models.py`** : Entraîne et sauvegarde les modèles (`logistic_regression`, `decision_tree`, `knn`, `random_forest`).
- **`app.py`** : Expose un modèle via une API Flask sur un port spécifié.
- **`client.py`** : Interroge les API des modèles, calcule une prédiction consensuelle pondérée et applique des pénalités.
- **`model_balances.json`** : Stocke les soldes et les précisions des modèles.
- **`requirements.txt`** : Liste des dépendances Python nécessaires.

## Prérequis

- Python 3.8 ou supérieur
- Les dépendances listées dans `requirements.txt`

## Installation

1. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Entrainez les modèles :

```bash
python create_models.py
```

## Utilisation

1. Démarrez les API Flask pour chaque modèle (dans des terminaux séparés) :
   
```bash
python app.py --port=5000 --model=logistic_regression
python app.py --port=5001 --model=decision_tree
python app.py --port=5002 --model=knn
python app.py --port=5003 --model=random_forest
```

2. Exécutez le client pour interroger les API et générer une prédiction consensuelle :
   
```bash
python client.py
```

## Résultat attendu

Le client affichera :

* Les prédictions individuelles de chaque modèle.

* La prédiction consensuelle pondérée.

* Les pénalités appliquées aux modèles qui ont fait des prédictions incorrectes.

Exemple de sortie :

```bash
Prédictions individuelles : [2, 1, 2, 1]
Prédiction consensuelle pondérée : 1.63
Pénalité appliquée à decision_tree. Nouveau solde : 900
Pénalité appliquée à random_forest. Nouveau solde : 900
logistic_regression a fait une prédiction correcte. Solde inchangé : 1000
knn a fait une prédiction correcte. Solde inchangé : 1000
```