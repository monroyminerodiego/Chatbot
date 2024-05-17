from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

# Cargar datos
data_url = "training_data.xlsx"
data = pd.read_excel(data_url)
data = data.loc[data['labels'].isin(['assault', 'sexual abuse'])]
X = data['data']
y = data['labels']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Función para crear y entrenar modelos
def makeModel(classifier, X_train, y_train):
    pipeline = Pipeline([
        ('bow', CountVectorizer()),  # strings to token integer counts
        ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
        ('classifier', classifier),  # train on TF-IDF vectors with classifier
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

# Entrenar y guardar modelos
forest = makeModel(RandomForestClassifier(), X_train, y_train)
pickle.dump(forest, open("randomForest.p", "wb"))

supportV = makeModel(SVC(), X_train, y_train)
pickle.dump(supportV, open("NewSVC.p", "wb"))

bayes = makeModel(MultinomialNB(), X_train, y_train)
pickle.dump(bayes, open("MultiNB.p", "wb"))
