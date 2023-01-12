# Standard library
import pickle
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.scrolledtext as st
import tkinter.ttk as ttk
from math import floor

# Third-party
from click import launch

# First-party/Local
import config
import data_viz
import my_data
import my_model
import search
import text_utils


def btn_select_book_callback(txt_similar_books):
    similar_books_list_of_tuples = my_model.get_similar_books(
        my_data.book_display_name_to_id[config.cur_selection],
        my_model.book_weights,
        n_similar_books=config.cur_n_similar_books,
    )
    similar_books_list_display = [
        f"{x[0]}\n(similarity: {int(floor(x[1] * 100))}/100)" for x in similar_books_list_of_tuples
    ]
    fill_textbox(txt_similar_books, "\n\n".join(similar_books_list_display))


def wget_slider_callback(new_val, txt_similar_books):
    config.cur_n_similar_books = int(new_val)
    if config.cur_selection:
        similar_books_list_of_tuples = my_model.get_similar_books(
            my_data.book_display_name_to_id[config.cur_selection],
            my_model.book_weights,
            n_similar_books=config.cur_n_similar_books,
        )
        similar_books_list_display = [
            f"{x[0]}\n(similarity: {int(floor(x[1] * 100))}/100)" for x in similar_books_list_of_tuples
        ]
        fill_textbox(txt_similar_books, "\n\n".join(similar_books_list_display))


def fill_textbox(textbox, string):
    textbox.delete(config.tk_BEGIN, tk.END)
    textbox.insert(tk.END, string)


def launchApp():
    book_trie = search.get_book_trie()
    search_results_font_size = 16

    title_font = {"font": ("Arial", 18)}
    user_input_font = {"font": ("Arial", 25)}
    search_results_font = {"font": ("Arial", 12)}
    footer_font = {"font": ("Arial", 14)}
    frame_attrs = {"height": 500, "width": 500, "relief": tk.GROOVE, "padding": 20, "borderwidth": 0, "relief": "flat"}

    active_selection_style = {
        "tagName": "selected_line",
        "font": ("Arial", search_results_font["font"][1], "bold"),
        "borderwidth": 2,
        "relief": "solid",
    }

    # create UI
    window = tk.Tk()
    window.title("Tim's Book Recommender")
    window.geometry("1700x1000")

    frm_title_bar = ttk.Frame(master=window, padding=40)
    tk.Label(master=frm_title_bar, text="Tim's Book Recommender", **title_font).pack()
    frm_title_bar.pack()

    frm_body0 = ttk.Frame(master=window)

    frm_body1 = ttk.Frame(master=frm_body0, **frame_attrs)
    # tk.Text(master=frame_body1, height=25).pack()

    frm_user_input = ttk.Frame(master=frm_body1)
    lbl_user_input = tk.Label(master=frm_user_input, text="Search by title or author:", justify=tk.LEFT)
    lbl_user_input.pack(anchor=tk.W)
    ent_user_input = tk.Entry(master=frm_user_input, **user_input_font)
    ent_user_input.pack()
    frm_user_input.pack()

    stxt_search_results = st.ScrolledText(master=frm_body1, height=15, width=45, **search_results_font)
    stxt_search_results.pack()

    btn_select_book = tk.Button(
        master=frm_body1, text="Show me similar books!", command=lambda: btn_select_book_callback(stxt_similar_books)
    )
    btn_select_book.pack()
    frm_body1.pack(side=tk.LEFT)

    frm_body2 = ttk.Frame(master=frm_body0, **frame_attrs)
    lbl_choose_n = tk.Label(master=frm_body2, text="How many similar books do you want to see?", justify=tk.LEFT)
    lbl_choose_n.pack(anchor=tk.W)
    wgt_slider = tk.Scale(
        master=frm_body2,
        from_=1,
        to=20,
        orient=tk.HORIZONTAL,
        command=lambda new_val: wget_slider_callback(new_val, stxt_similar_books),
    )
    wgt_slider.set(config.cur_n_similar_books)
    wgt_slider.pack()
    stxt_similar_books = st.ScrolledText(master=frm_body2, height=15, width=45, **search_results_font)
    stxt_similar_books.pack()
    frm_body2.pack(side=tk.LEFT)

    frm_body3 = ttk.Frame(master=frm_body0, **frame_attrs)
    lbl_choose_dataviz = tk.Label(master=frm_body3, text="Please select a data visualization:", justify=tk.LEFT)
    lbl_choose_dataviz.pack(anchor=tk.W)

    nb_dataviz = ttk.Notebook(frm_body3, width=325)
    nb_dataviz.pack(pady=10)

    DATA_VIZ_WIDTH = 300
    DATA_VIZ_HEIGHT = 200

    viz1 = ttk.Frame(nb_dataviz, width=DATA_VIZ_WIDTH, height=DATA_VIZ_HEIGHT)
    var_msg_viz1_desc = tk.StringVar()
    var_msg_viz1_desc.set(
        "This data visualization shows the selected book in blue with similar books in green. The remaining books in the deep-learning model are plotted in yellow. Please note that it can take up to 5 minutes to generate this plot, even on a powerful PC."
    )
    msg_viz1_desc = tk.Message(master=viz1, textvariable=var_msg_viz1_desc)
    msg_viz1_desc.pack()
    btn_viz1 = tk.Button(
        master=viz1, text="Create a plot of similar books.", command=lambda: data_viz.plot_similar_books()
    )
    btn_viz1.pack()

    viz2 = ttk.Frame(nb_dataviz, width=DATA_VIZ_WIDTH, height=DATA_VIZ_HEIGHT)
    var_msg_viz2_desc = tk.StringVar()
    var_msg_viz2_desc.set(
        "This data visualization shows all the books by the selected author. The remaining books in the deep-learning model are plotted in yellow. Please note that it can take up to 5 minutes to generate this plot, even on a powerful PC."
    )
    msg_viz2_desc = tk.Message(master=viz2, textvariable=var_msg_viz2_desc)
    msg_viz2_desc.pack()
    btn_viz2 = tk.Button(
        master=viz2, text="Create a plot of this author's books.", command=lambda: data_viz.plot_same_author()
    )
    btn_viz2.pack()

    viz3 = ttk.Frame(nb_dataviz, width=DATA_VIZ_WIDTH, height=DATA_VIZ_HEIGHT)
    var_msg_viz3_desc = tk.StringVar()
    var_msg_viz3_desc.set(
        "This data visualizatoin shows the books in the top 10 most common book genres, plotted in different colors. Please note that it can take up to 5 minutes to generate this plot, even on a powerful PC."
    )
    msg_viz3_desc = tk.Message(master=viz3, textvariable=var_msg_viz3_desc)
    msg_viz3_desc.pack()
    btn_viz3 = tk.Button(
        master=viz3, text="Create a plot of the top 10 genres.", command=lambda: data_viz.plot_all_genres()
    )
    btn_viz3.pack()

    viz1.pack(fill=tk.BOTH, expand=True)
    viz2.pack(fill=tk.BOTH, expand=True)
    viz3.pack(fill=tk.BOTH, expand=True)

    nb_dataviz.add(viz1, text="Plot similar books")
    nb_dataviz.add(viz2, text="Plot same author")
    nb_dataviz.add(viz3, text="Plot all genres")

    frm_body3.pack(side=tk.LEFT)

    frm_body0.pack()

    frm_footer = ttk.Frame(master=window, padding=40)
    tk.Label(master=frm_footer, text="Thank you for using Tim's Book Recommender", **footer_font).pack()
    frm_footer.pack()

    previous_state_query_entry = ""
    previous_index_location = config.tk_BEGIN

    stxt_search_results.tag_add("selected_line", f"1.0", f"1.0")
    stxt_search_results.tag_configure(**active_selection_style)

    while True:

        # check whether we need to highlight a line in the results box
        cur_index_location = stxt_search_results.index(tk.INSERT)
        if cur_index_location != previous_index_location:
            fill_textbox(stxt_similar_books, "")
            cur_row = cur_index_location[slice(0, cur_index_location.index("."))]
            if cur_row != "1":
                stxt_search_results.tag_delete("selected_line")
                stxt_search_results.tag_add("selected_line", f"{cur_row}.0", f"{cur_row}.0 lineend")
                stxt_search_results.tag_configure(**active_selection_style)
                config.cur_selection = stxt_search_results.get(f"{cur_row}.0", f"{cur_row}.0 lineend")
                previous_index_location = cur_index_location

        # check whether we need to update the results
        cur_state_query_entry = ent_user_input.get()

        if not cur_state_query_entry:
            previous_state_query_entry = cur_state_query_entry
            fill_textbox(stxt_search_results, config.search_box_prompt)
            fill_textbox(stxt_similar_books, "")
            config.cur_selection = ""
            config.cur_selection_book_id = -1

        elif cur_state_query_entry.strip() != previous_state_query_entry:
            fill_textbox(stxt_similar_books, "")
            search_terms = cur_state_query_entry.strip("\ ").split(" ")
            search_terms = [text_utils.sanitize_trie_term(x) for x in search_terms]

            if not search_terms:
                # clear results box
                fill_textbox(stxt_search_results, config.search_box_prompt)
                config.cur_selection = ""
                config.cur_selection_book_id = -1

            else:
                if len(search_terms) == 1:
                    search_results_as_ids = book_trie.getHitsOnPrefix(search_terms[0])
                    search_results_for_display = text_utils.match_count_display(0)
                    if search_results_as_ids:
                        search_results_as_titles = [my_data.book_id_to_slug[id] for id in search_results_as_ids]
                        search_results_for_display = text_utils.match_count_display(len(search_results_as_ids))
                        search_results_for_display += "\n".join(sorted(search_results_as_titles))
                    fill_textbox(stxt_search_results, search_results_for_display)

                else:  # `len(search_terms) > 1`
                    ids_with_hits = []
                    noHits = False  # flag to indicate that a search term matches nothing in the library

                    # do exact search with all but the last search term
                    for each_search_term in search_terms[:-1]:
                        if not each_search_term:
                            pass
                        res = book_trie.getHitsOnExactWord(each_search_term)
                        if not res:
                            noHits = True
                            break
                        else:
                            ids_with_hits.append(res)

                    # do prefix search with the last search term
                    if noHits:
                        pass  # we already know it's "no matches"
                    else:
                        res = book_trie.getHitsOnPrefix(search_terms[-1])
                        if not res:
                            noHits = True
                        else:
                            ids_with_hits.append(res)

                    if noHits:
                        fill_textbox(stxt_search_results, text_utils.match_count_display(0))
                    else:
                        # ensure that `ids_with_hits` is a list of non-empty sets
                        ids_with_hits = [x for x in ids_with_hits if isinstance(x, set) and len(x) > 0]

                        if ids_with_hits:
                            results_set = set(ids_with_hits[-1])

                            for ids in ids_with_hits[0:-1]:
                                results_set.intersection_update(set(ids))

                            what_to_show = text_utils.match_count_display(len(results_set))
                            what_to_show += "\n".join(sorted(my_data.dereference_list_of_ids(list(results_set))))
                            fill_textbox(stxt_search_results, what_to_show)
                        else:
                            fill_textbox(stxt_search_results, text_utils.match_count_display(0))

            previous_state_query_entry = cur_state_query_entry

        # continue mainloop()
        window.update_idletasks()
        window.update()


if __name__ == "__main__":

    # launchApp()
    launchApp()
