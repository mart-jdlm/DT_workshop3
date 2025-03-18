from flask import Flask, request, jsonify
import pickle
import numpy as np
import argparse

# Créer un analyseur d'arguments
parser = argparse.ArgumentParser(description='Démarrer une API Flask pour un modèle prédictif.')
parser.add_argument('--port', type=int, required=True, help='Le port sur lequel démarrer le serveur Flask.')
parser.add_argument('--model', type=str, required=True, help='Le nom du modèle à utiliser (logistic_regression, decision_tree, knn, random_forest).')
args = parser.parse_args()

app = Flask(__name__)

# Charger le modèle spécifié
try:
    with open(f'{args.model}.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"Erreur : Le modèle '{args.model}' n'existe pas.")
    exit(1)

# Route pour la prédiction
@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Récupérer les arguments de la requête
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))

        # Créer un tableau numpy pour la prédiction
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        # Faire la prédiction
        prediction = model.predict(input_data)
        return jsonify({'model': args.model, 'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)})

# Démarrer l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=args.port)