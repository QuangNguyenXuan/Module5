import random
import pickle
import json
import numpy as np
import nltk
#nltk.download('omw-1.4')
#nltk.download('punkt')

from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

leimatizer = WordNetLemmatizer()

intents = json.load(open('/Users/dinhvinh/PycharmProjects/RuleBasedChatBot/static/intents.json'))

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        documents.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [leimatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

pickle.dump(words, open('/Users/dinhvinh/PycharmProjects/RuleBasedChatBot/static/word.pkl','wb'))
pickle.dump(classes, open('/Users/dinhvinh/PycharmProjects/RuleBasedChatBot/static/classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

print(documents)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [leimatizer.lemmatize(w.lower()) for w in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    out_row = list(output_empty)
    out_row[classes.index(document[1])] = 1
    training.append([bag, out_row])

random.shuffle(training)
training = np.array(training)

print("training", training)

train_x = list(training[:,0])
train_y = list(training[:,1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01,  momentum=0.9)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

model.save('/Users/dinhvinh/PycharmProjects/RuleBasedChatBot/static/chatbot_model.h5',hist)

