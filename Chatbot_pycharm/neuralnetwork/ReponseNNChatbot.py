import random
import pickle
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
leimatizer = WordNetLemmatizer()

file_path_json = 'static/intents.json'
file_path_word = 'static/word.pkl'
file_path_classes = 'static/classes.pkl'
file_path_model = 'static/chatbot_model.h5'

# file_path_json = 'intents.json'
# file_path_word = 'word.pkl'
# file_path_classes = 'classes.pkl'
# file_path_model = 'chatbot_model.h5'

intents = json.load(open(file_path_json))
words = pickle.load(open(file_path_word,'rb'))
classes = pickle.load(open(file_path_classes,'rb'))
model = load_model(file_path_model)

leimatizer = WordNetLemmatizer()

def cleanup_sentense(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [leimatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = cleanup_sentense(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    p = bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    print(res)
    CONFIDENT_SCORE = 0.5
    results = [[i, r] for i, r in enumerate(res) if r > CONFIDENT_SCORE]

    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

import time

def getResponse(intent_list, intent_json):
    result = ""
    try:
        tag = intent_list[0]['intent']
        list_of_intents = intent_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                if tag == 'currenttime':
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    result = random.choice(i['responses']) + current_time
                else:
                    result = random.choice(i['responses'])
                break
    except IndexError:
        result = "I don't understand!"
    return result

