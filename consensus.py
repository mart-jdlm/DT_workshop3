# consensus.py
import requests
import numpy as np

# Exemples de requêtes pour chaque modèle
model_names = ["SVM", "KNN", "LogisticRegression"]
features = {'f1': 5.1, 'f2': 3.5, 'f3': 1.4, 'f4': 0.2}

predictions = []

for model_name in model_names:
    response = requests.get(f'http://localhost:5000/predict', params={**features, 'model': model_name})
    if response.status_code == 200:
        prediction = response.json()['prediction']
        predictions.append(prediction)

# Calculer la prédiction finale en faisant la moyenne
final_prediction = round(np.mean(predictions))

print(f"Consensus Prediction: {final_prediction}")