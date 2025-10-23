from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

training_data = [
    ("show me a roadmap", "roadmap"),
    ("give me a quiz", "quiz"),
    ("explain this topic", "explanation"),
    ("I want to test myself", "quiz"),
    ("how does this work", "explanation"),
    ("what should I learn next", "roadmap"),
    ("start a quiz", "quiz"),
    ("help me understand this", "explanation"),
    ("suggest a learning path", "roadmap"),
    ("give me a advance math quiz", "advancem")
]

texts, labels = zip(*training_data)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

model_path = os.path.join("model", "intent_classifier.pkl")
with open(model_path, "wb") as f:
    pickle.dump((vectorizer, model), f)

print("✅ Model trained and saved to 'model/intent_classifier.pkl'")
