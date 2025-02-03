# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Charger les modèles sauvegardés
models = {
    "SVM": joblib.load('models/SVM_model.pkl'),
    "KNN": joblib.load('models/KNN_model.pkl'),
    "LogisticRegression": joblib.load('models/LogisticRegression_model.pkl')
}

@app.route('/predict', methods=['GET'])
def predict():
    # Récupérer les arguments de la requête
    model_name = request.args.get('model')
    features = [float(request.args.get('f1')), float(request.args.get('f2')), 
                float(request.args.get('f3')), float(request.args.get('f4'))]
    
    # Vérifier si le modèle est valide
    if model_name not in models:
        return jsonify({'error': 'Invalid model name'}), 400
    
    # Effectuer la prédiction
    model = models[model_name]
    prediction = model.predict([features])[0]
    
    return jsonify({'model': model_name, 'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)