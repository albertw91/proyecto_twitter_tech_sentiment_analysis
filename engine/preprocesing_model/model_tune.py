import re
import time
import pandas as pd
import numpy as np

import mlflow
import mlflow.sklearn


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score

# Ejemplo con Stack de RNNs
from keras.layers import Embedding, SimpleRNN
from keras.layers import Dense
from keras.models import Sequential


import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
mlflow.set_tracking_uri("http://localhost:5000")



if __name__ == "__main__":

    corpus_train_esA = pd.read_csv("tweets_search_etiquetas_clean.csv", sep = ";", encoding = "latin-1" )
    corpus_dev_esA = pd.read_csv("tweets_search_etiquetas_clean_test.csv", sep = ";", encoding = "latin-1")
    corpus_dev_esA.head()


    train_idA = corpus_train_esA[corpus_train_esA.columns[0]]
    X_train_textA = corpus_train_esA[corpus_train_esA.columns[3]].fillna(' ')
    y_train_hsA = corpus_train_esA[corpus_train_esA.columns[5]]

    test_idA = corpus_dev_esA[corpus_train_esA.columns[0]]
    X_test_textA = corpus_dev_esA[corpus_dev_esA.columns[3]].fillna(' ')
    y_test_hsA = corpus_dev_esA[corpus_dev_esA.columns[5]]


    cvectorizer = CountVectorizer(
        # lowercase=True,
        #stop_words=[word.decode('utf-8') for word in nltk.corpus.stopwords.words('spanish')],
        #token_pattern=r'\b\w+\b', #selects tokens of 2 or more alphanumeric characters 
        ngram_range=(1,3),#n-grams de palabras n = 1 a n = 3 (unigramas, bigramas y trigramas)
        min_df=5,#ignorando los términos que tienen una frecuencia de documento estrictamente inferior a 5
    ).fit(X_train_textA)

    X_train_cvectorized = cvectorizer.transform(X_train_textA).toarray()
    print(X_train_cvectorized.shape)

    X_test_cvectorized = cvectorizer.transform(X_test_textA).toarray()
    print(X_test_cvectorized.shape)


    with mlflow.start_run():

        mlflow.tensorflow.autolog()
        

        max_features = 10000  # tamaño del diccionario de palabras comunes
                            # (número de palabras a utilizar)
        maxlen = X_test_cvectorized.shape[1] #1775         # longitud máxima de cada secuencia 
        batch_size = 32


        model = Sequential()
        # Capa embedding
        # input_dim : tamaño del vocabulario
        # output_dim: dimensión del vector al que se mapea
        model.add(Embedding(input_dim=max_features, output_dim=32))
        model.add(SimpleRNN(32, return_sequences=True))
        model.add(SimpleRNN(32))
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        model.compile(
            optimizer='rmsprop', 
            loss='binary_crossentropy',
            metrics=['acc', "mse"]
        )

        tic = time.time()
        history_stackRNN = model.fit(
            X_train_cvectorized, y_train_hsA,
            epochs=15,
            batch_size=128,
            validation_split=0.2,
            verbose=2
        )
        print('Tiempo de entrenamiento:', time.time()-tic)

        # evaluate the model
        scores = model.evaluate(X_test_cvectorized, y_test_hsA, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[0], scores[0]*100))
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        print("%s: %.2f%%" % (model.metrics_names[2], scores[2]*100))

        

        
        run_id = mlflow.active_run().info.run_id


        # make predictions
        testPredict_stackRNN = model.predict(X_test_cvectorized)
        print('\t', 'Accuracy', accuracy_score(y_test_hsA, testPredict_stackRNN.round()))


        corpus_dev_esA["predict_test"] = testPredict_stackRNN.round()

        corpus_dev_esA.to_csv("tweets_search_etiquetas_clean_test_predict.csv", sep="\t", encoding = "latin-1")

        """
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(lr, "model")

        """