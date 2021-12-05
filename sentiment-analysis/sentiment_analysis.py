import pandas as pd
import re
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from numpy import array
from numpy import asarray
from numpy import zeros
from keras.layers import Input
from keras.layers.embeddings import Embedding
from keras.layers import Flatten, LSTM
from keras.layers.core import Activation, Dropout, Dense
from keras.models import Model
from tensorflow.keras.models import Sequential, save_model, load_model
import numpy as np

sentiment_data = pd.DataFrame(None)
labels = ['strongly positive','positive','negative','strongly negative']
model = None
vocab_size = None
tokenizer = None
X_train, X_test = None, None
y1_train, y1_test, y2_train, y2_test = None, None, None, None
y3_train, y3_test, y4_train, y4_test = None, None, None, None

def read_file(input_file):
    global sentiment_data
    sentiment_data = pd.read_csv(input_file)
    sentiment_data = sentiment_data.dropna()

def preprocess_comments(comment):
    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', comment)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)

def create_dataset():
    global X_train, X_test, y1_train, y1_test, y2_train, y2_test, y3_train, y3_test, y4_train, y4_test
    X = []
    sentences = list(sentiment_data["comment"])

    for sen in sentences:
        X.append(preprocess_comments(sen))

    y = sentiment_data[['strongly positive','positive','negative','strongly negative']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    X_train, X_test = tokenize()

    y1_train = y_train[["strongly positive"]].values
    y1_test =  y_test[["strongly positive"]].values

    y2_train = y_train[["positive"]].values
    y2_test =  y_test[["positive"]].values

    y3_train = y_train[["negative"]].values
    y3_test =  y_test[["negative"]].values

    y4_train = y_train[["strongly negative"]].values
    y4_test =  y_test[["strongly negative"]].values


def tokenize():
    global vocab_size, X_train, X_test, tokenizer

    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(X_train)

    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)

    vocab_size = len(tokenizer.word_index) + 1

    maxlen = 100

    X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
    X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

    return X_train, X_test

def embeddings():
    global tokenizer

    embeddings_dictionary = dict()

    glove_file = open('glove.6B.100d.txt', encoding="utf8")

    for line in glove_file:
        records = line.split()
        word = records[0]
        vector_dimensions = asarray(records[1:], dtype='float32')
        embeddings_dictionary[word] = vector_dimensions
    glove_file.close()

    embedding_matrix = zeros((vocab_size, 100))
    for word, index in tokenizer.word_index.items():
        embedding_vector = embeddings_dictionary.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector

    return embedding_matrix

def create_model():
    input = Input(shape=(100,))
    embedding_layer = Embedding(vocab_size, 100, weights=[embeddings()], trainable=False)(input)
    LSTM_Layer1 = LSTM(128)(embedding_layer)

    output1 = Dense(1, activation='sigmoid')(LSTM_Layer1)
    output2 = Dense(1, activation='sigmoid')(LSTM_Layer1)
    output3 = Dense(1, activation='sigmoid')(LSTM_Layer1)
    output4 = Dense(1, activation='sigmoid')(LSTM_Layer1)

    model = Model(inputs=input, outputs=[output1, output2, output3, output4])
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

def run_model():
    global X_train, X_test, y1_train, y2_train, y3_train, y4_train
    history = model.fit(X_train, y=[y1_train, y2_train, y3_train, y4_train], batch_size=128, epochs=10, verbose=1, validation_split=0.3)

def evaluate_model():
    global X_test, y1_test, y2_test, y3_test, y4_test
    score = model.evaluate(x=X_test, y=[y1_test, y2_test, y3_test, y4_test], verbose=1)

    print("Test Score:", score[0])
    print("Test Accuracy:", score[1])

def save_model():
    global model
    # Save the model
    filepath = './saved_model'
    save_model(model, filepath)
    # Load the model
    model = load_model(filepath, compile = True)

def predict(input):
    global tokenizer, model, labels

    seq = tokenizer.texts_to_sequences(input)
    padded = pad_sequences(seq, maxlen=100)
    pred = model.predict(padded)
    return labels[np.argmax(pred)]

def main(input):
    return predict(input)

if __name__ == "__main__":
    main()