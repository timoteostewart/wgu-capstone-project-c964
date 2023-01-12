# Standard library
import json
import os
import pickle


def dereference_list_of_ids(list_of_ids):
    res = []
    for id in list_of_ids:
        res.append(book_id_to_slug[id])
    return res


books = []
with open(os.path.join("books.json"), mode="r", encoding="utf-8") as fin:
    books.extend(json.load(fin)["books"])


# load dictionaries from pickles
with open("books_id_to_author_dict.pickle", mode="rb") as fin:
    books_id_to_author = pickle.load(fin)
with open("books_id_to_name_dict.pickle", mode="rb") as fin:
    books_id_to_name = pickle.load(fin)
with open("books_name_to_id_dict.pickle", mode="rb") as fin:
    books_name_to_id = pickle.load(fin)
with open("wikilink_id_to_name_dict.pickle", mode="rb") as fin:
    wikilink_id_to_name = pickle.load(fin)
with open("wikilink_name_to_id_dict.pickle", mode="rb") as fin:
    wikilink_name_to_id = pickle.load(fin)


book_display_name_to_id = dict()
book_id_to_display_name = dict()

list_of_book_tuples = []
for id in books_id_to_name.keys():
    book_name = books_id_to_name[id]
    book_author = books_id_to_author[id]
    if book_author == "not_found":
        list_of_book_tuples.append(
            (
                book_name,
                id,
            )
        )
        book_display_name_to_id[book_name] = id
        book_id_to_display_name[id] = book_name
    else:
        display_name = f"{book_name} by {book_author}"
        list_of_book_tuples.append(
            (
                display_name,
                id,
            )
        )
        book_display_name_to_id[display_name] = id
        book_id_to_display_name[id] = display_name

book_slug_to_id = dict()
book_id_to_slug = dict()
for t in list_of_book_tuples:
    book_slug_to_id[t[0]] = t[1]
    book_id_to_slug[t[1]] = t[0]
