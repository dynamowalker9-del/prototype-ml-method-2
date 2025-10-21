import pickle
import os

def load_model():
    model_path = os.path.join("model", "intent_classifier.pkl")
    with open(model_path, "rb") as f:
        vectorizer, model = pickle.load(f)
    return vectorizer, model

def predict_intent(text):
    vectorizer, model = load_model()
    X_input = vectorizer.transform([text])
    return model.predict(X_input)[0]
