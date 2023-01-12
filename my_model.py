# Standard library
import random
from collections import Counter

# Third-party
import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.layers import Dense, Dot, Embedding, Input, Reshape
from keras.models import Model
from sklearn.manifold import TSNE
from umap import UMAP

# First-party/Local
import config
import my_data

# parameters
MINIMUM_FREQUENCY_FOR_WIKILINKS = 5
plt.style.use("fivethirtyeight")
plt.rcParams["font.size"] = 15
random.seed(100)

pairs_set = set()
pairs_list = list()


# def book_embedding_model(embedding_size=50, classification=False):
#     """Model to embed books and wikilinks using the functional API.
#     Trained to discern if a link is present in a article"""

#     # Both inputs are 1-dimensional
#     book = Input(name="book", shape=[1])
#     link = Input(name="link", shape=[1])

#     # Embedding the book (shape will be (None, 1, 50))
#     book_embedding = Embedding(
#         name="book_embedding", input_dim=len(my_data.books_id_to_name), output_dim=embedding_size
#     )(book)

#     # Embedding the link (shape will be (None, 1, 50))
#     link_embedding = Embedding(
#         name="link_embedding", input_dim=len(my_data.wikilink_id_to_name), output_dim=embedding_size
#     )(link)

#     # Merge the layers with a dot product along the second axis (shape will be (None, 1, 1))
#     merged = Dot(name="dot_product", normalize=True, axes=2)([book_embedding, link_embedding])

#     # Reshape to be a single number (shape will be (None, 1))
#     merged = Reshape(target_shape=[1])(merged)

#     # If classifcation, add extra layer and loss function is binary cross entropy
#     if classification:
#         merged = Dense(1, activation="sigmoid")(merged)
#         model = Model(inputs=[book, link], outputs=merged)
#         model.compile(optimizer="Adam", loss="binary_crossentropy", metrics=["accuracy"])

#     # Otherwise loss function is mean squared error
#     else:
#         model = Model(inputs=[book, link], outputs=merged)
#         model.compile(optimizer="Adam", loss="mse")

#     return model


# def generate_batch(pairs, n_positive=50, negative_ratio=1.0, classification=False):
#     """Generate batches of samples for training"""
#     batch_size = n_positive * (1 + negative_ratio)
#     batch = np.zeros((batch_size, 3))

#     # Adjust label based on task
#     if classification:
#         neg_label = 0
#     else:
#         neg_label = -1

#     # This creates a generator
#     while True:
#         # randomly choose positive examples
#         for idx, (book_id, link_id) in enumerate(random.sample(pairs, n_positive)):
#             batch[idx, :] = (book_id, link_id, 1)

#         # Increment idx by 1
#         idx += 1

#         # Add negative examples until reach batch size
#         while idx < batch_size:

#             # random selection
#             random_book = random.randrange(len(my_data.books))
#             random_link = random.randrange(len(my_data.wikilink_name_to_id))

#             # Check to make sure this is not a positive example
#             if (random_book, random_link) not in pairs_set:

#                 # Add to batch and increment index
#                 batch[idx, :] = (random_book, random_link, neg_label)
#                 idx += 1

#         # Make sure to shuffle order
#         np.random.shuffle(batch)
#         yield {"book": batch[:, 0], "link": batch[:, 1]}, batch[:, 2]


def get_similar_books(book_id, weights, n_similar_books=10):

    config.cur_selection_book_id = book_id

    n_similar_books += 1  # since we're dropping the match to itself

    name = my_data.books_id_to_name[book_id]
    index = my_data.books_name_to_id
    rindex = my_data.books_id_to_name

    # Calculate dot product between book and all others
    dists = np.dot(weights, weights[book_id])

    # Sort distance indexes from smallest to largest
    sorted_dists = np.argsort(dists)

    # Take the last n sorted distances
    closest = sorted_dists[-n_similar_books:]
    config.cur_n_similar_books_ids = list(closest)

    res = [(my_data.book_id_to_display_name[c], dists[c]) for c in list(reversed(closest))[1:]]
    return res


model = keras.models.load_model("model3.h5")
book_weights = model.get_layer("book_embedding").get_weights()[0]
book_weights = book_weights / np.linalg.norm(book_weights, axis=1).reshape((-1, 1))
