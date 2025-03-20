import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense
from tensorflow.keras.utils import to_categorical
from PIL import Image
import pickle

# Load Pre-trained ResNet50 Model (Feature Extractor)
base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
feature_extractor = Model(inputs=base_model.input, outputs=base_model.output)

def extract_features(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
    return feature_extractor.predict(img_array)

# Example captions dataset
captions = {
    "image1.jpg": "a cat sitting on the table",
    "image2.jpg": "a dog running in the park",
    "image3.jpg": "a child playing with a ball"
}

# Tokenizing captions
tokenizer = Tokenizer()
tokenizer.fit_on_texts(list(captions.values()))
vocab_size = len(tokenizer.word_index) + 1

# Prepare sequences
max_length = max(len(c.split()) for c in captions.values())
X, y = [], []

for img, caption in captions.items():
    seq = tokenizer.texts_to_sequences([caption])[0]
    for i in range(1, len(seq)):
        X.append(seq[:i])
        y.append(seq[i])

X = pad_sequences(X, maxlen=max_length, padding='post')
y = np.array(y)
y = to_categorical(y, num_classes=vocab_size)

# Define LSTM Model
inputs = Input(shape=(max_length,))
embedding = Embedding(vocab_size, 256)(inputs)
lstm = LSTM(256, return_sequences=False)(embedding)
out = Dense(vocab_size, activation='softmax')(lstm)
model = Model(inputs, out)

model.compile(loss='categorical_crossentropy', optimizer='adam')

# Train the model (Dummy Training Step)
# model.fit(X, y, epochs=10)

def generate_caption(image_path):
    features = extract_features(image_path)
    caption = "<start>"
    for _ in range(max_length):
        seq = tokenizer.texts_to_sequences([caption])[0]
        seq = pad_sequences([seq], maxlen=max_length, padding='post')
        pred = np.argmax(model.predict(seq))
        word = tokenizer.index_word.get(pred, '')
        if word == '<end>' or word == '':
            break
        caption += ' ' + word
    return caption.replace('<start>', '').strip()

# Example: generate_caption('image1.jpg')
