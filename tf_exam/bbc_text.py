# Question
#
# For this task you will train a classifier on the bbc news text archive
# Your classifier should be trained on the 6 categories shown below, and your final layer
# should be as shown -- Dense layer with 6 neurons and softmax activation.
# Your model will be tested against unseen sentences and you will be scored on whether they
# are correctly classified or not.


import csv
import tensorflow as tf
import numpy as np
import urllib
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences


def solution_model():
    url = 'https://storage.googleapis.com/download.tensorflow.org/data/bbc-text.csv'
    urllib.request.urlretrieve(url, 'bbc-text.csv')

    # DO NOT CHANGE THE VALUES OF THESE CONSTANTS OR THE TESTS MAY FAIL
    vocab_size = 1000
    embedding_dim = 16
    max_length = 120
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = "<OOV>"
    training_size = 20000
    sentences = []
    labels = []
    stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
                 "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did",
                 "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have",
                 "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
                 "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's",
                 "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only",
                 "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd",
                 "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
                 "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
                 "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we",
                 "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's",
                 "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll",
                 "you're", "you've", "your", "yours", "yourself", "yourselves"]

    with open("bbc-text.csv", 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)

        for row in csv_reader:
            labels.append(row[0])
            sentence = row[1]

            for word in stopwords:
                token = ' ' + word + ' '
                sentence = sentence.replace(token, ' ').replace('  ', ' ')

            sentences.append(sentence)
    training_portion = 8
    print(len(labels))
    print(len(sentences))
    print(sentences[0])
    # YOUR CODE HERE
    train_size = int(len(sentences) * training_portion)

    train_sentences = sentences[:train_size]
    train_labels = labels[:train_size]

    validation_sentences = sentences[train_size:]
    validation_labels = labels[train_size:]

    print(train_size)
    print(len(train_sentences))
    print(len(train_labels))
    print(len(validation_sentences))
    print(len(validation_labels))
    tokenizer = Tokenizer(
        num_words=vocab_size,
        oov_token=oov_tok
    )
    tokenizer.fit_on_texts(train_sentences)
    word_index = tokenizer.word_index

    train_sequences = tokenizer.texts_to_sequences(train_sentences)

    train_padded = pad_sequences(
        train_sequences,
        padding=padding_type,
        maxlen=max_length
    )

    print(len(train_sequences[0]))
    print(len(train_padded[0]))

    print(len(train_sequences[1]))
    print(len(train_padded[1]))

    print(len(train_sequences[10]))
    print(len(train_padded[10]))
    validation_sequences = tokenizer.texts_to_sequences(validation_sentences)
    validation_padded = pad_sequences(
        validation_sequences,
        padding=padding_type,
        maxlen=max_length
    )

    print(len(validation_sequences))
    print(validation_padded.shape)
    label_tokenizer = Tokenizer()
    label_tokenizer.fit_on_texts(labels)

    training_label_seq = np.array(label_tokenizer.texts_to_sequences(train_labels))
    validation_label_seq = np.array(label_tokenizer.texts_to_sequences(validation_labels))

    print(training_label_seq[0])
    print(training_label_seq[1])
    print(training_label_seq[2])
    print(training_label_seq.shape)

    # print(validation_label_seq[0])
    # print(validation_label_seq[1])
    # print(validation_label_seq[2])
    # print(validation_label_seq.shape)
    model = tf.keras.Sequential([
        # YOUR CODE HERE
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(24, activation='relu'),
        # tf.keras.layers.Dense(6, activation='softmax')
        # PLEASE NOTE -- WHILE THERE ARE 5 CATEGORIES, THEY ARE NUMBERED 1 THROUGH 5 IN THE DATASET
        # SO IF YOU ONE-HOT ENCODE THEM, THEY WILL END UP WITH 6 VALUES, SO THE OUTPUT LAYER HERE
        # SHOULD ALWAYS HAVE 6 NEURONS AS BELOW. MAKE SURE WHEN YOU ENCODE YOUR LABELS THAT YOU USE
        # THE SAME FORMAT, OR THE TESTS WILL FAIL
        # 0 = UNUSED
        # 1 = SPORT
        # 2 = BUSINESS
        # 3 = POLITICS
        # 4 = TECH
        # 5 = ENTERTAINMENT

        tf.keras.layers.Dense(6, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    num_epochs = 30
    history = model.fit(
        train_padded,
        training_label_seq,
        epochs=num_epochs,
        validation_data=(validation_padded, validation_label_seq),
        verbose=2
    )
    # YOUR CODE HERE
    return model


# Note that you'll need to save your model as a .h5 like this
# This .h5 will be uploaded to the testing infrastructure
# and a score will be returned to you
if __name__ == '__main__':
    model = solution_model()
    model.save("mymodel.h5")