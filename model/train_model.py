from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Sample training data
data = [
    ("show me a roadmap", "roadmap"),
    ("give me a quiz", "quiz"),
    ("explain this topic", "explanation"),
    ("I want to test myself", "quiz"),
    ("how does this work", "explanation"),
    ("what should I learn next", "roadmap")
]

texts, labels = zip(*data)

# Vectorize and train
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)

# Save model
with open("model/intent_classifier.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("Model trained and saved successfully.")