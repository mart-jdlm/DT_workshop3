# client.py
import requests
import json

# URLs des API des modèles et leurs noms correspondants
api_urls = {
    'http://localhost:5000/predict': 'logistic_regression',
    'http://localhost:5001/predict': 'decision_tree',
    'http://localhost:5002/predict': 'knn',
    'http://localhost:5003/predict': 'random_forest'
}

# Poids des modèles (basés sur leur précision)
weights = [0.9, 0.8, 0.7, 0.85]  # Exemple de poids

# Données d'entrée pour la prédiction
input_data = {
    'sepal_length': 6.0,
    'sepal_width': 2.7,
    'petal_length': 5.1,
    'petal_width': 1.6
}

# Charger les soldes des modèles
try:
    with open('model_balances.json', 'r') as f:
        model_balances = json.load(f)
except FileNotFoundError:
    # Initialiser les soldes si le fichier n'existe pas
    model_balances = {
        "logistic_regression": {"balance": 1000, "accuracy": 0.9},
        "decision_tree": {"balance": 1000, "accuracy": 0.8},
        "knn": {"balance": 1000, "accuracy": 0.7},
        "random_forest": {"balance": 1000, "accuracy": 0.85}
    }

# Interroger chaque API et collecter les prédictions
predictions = []
for url, model_name in api_urls.items():
    response = requests.get(url, params=input_data)
    if response.status_code == 200:
        predictions.append(response.json()['prediction'])
    else:
        print(f"Erreur avec {url} : {response.text}")

# Calculer la prédiction consensuelle pondérée
if predictions:
    consensus_prediction = sum(p * w for p, w in zip(predictions, weights)) / sum(weights)
    print(f"Prédictions individuelles : {predictions}")
    print(f"Prédiction consensuelle pondérée : {consensus_prediction}")

    # Appliquer des pénalités pour les prédictions incorrectes
    ground_truth = 2  # Remplacez par la vraie valeur si disponible
    for (url, model_name), prediction in zip(api_urls.items(), predictions):
        if prediction != ground_truth:
            model_balances[model_name]['balance'] -= 100  # Pénalité de 100 euros
            print(f"Pénalité appliquée à {model_name}. Nouveau solde : {model_balances[model_name]['balance']}")
        else:
            print(f"{model_name} a fait une prédiction correcte. Solde inchangé : {model_balances[model_name]['balance']}")

    # Sauvegarder les soldes mis à jour
    with open('model_balances.json', 'w') as f:
        json.dump(model_balances, f, indent=4)
else:
    print("Aucune prédiction valide reçue.")