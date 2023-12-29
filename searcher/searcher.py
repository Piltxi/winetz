import os
import argparse

import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import Tk, Frame, Label, Button, Entry, Checkbutton, IntVar, scrolledtext, PhotoImage

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser

def update_selection():
    selected_numbers = [number_mapping[wine_type] for wine_type, var in zip(wine_types, check_vars) if var.get() == 1]
    print("Selected numbers:", selected_numbers)

def loadIndexCLI ():

    indexPath = input("Type the path to the index directory [or press enter]> ")
    indexPath = indexPath if indexPath else "../index"

    if not os.path.exists(indexPath) and os.path.isdir(indexPath):
        print ("] error during loading index: directory not found.\n")
        quit()

    ix = open_dir(indexPath)
    
    print (f"Number of items in loaded index: {ix.doc_count_all()}")
    
    return ix

def loadIndexGUI ():

    inputPath = filedialog.askdirectory()
    ix = open_dir(inputPath)

    return ix

def exportReport (): 

    outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

def search_and_display_results(ix, query_string, search_field=["wine_name", "style_description", "review_note", "wine_winery"]):
    searcher = ix.searcher()
    query_parser = MultifieldParser(search_field, ix.schema)
    query = query_parser.parse(query_string)
    results = searcher.search(query)
   
    return results

def loadGUI (ix): 
    def on_search_click():
        query_string = queryText.get()
        results = search_and_display_results(ix, query_string)
        result_text.delete(1.0, tk.END)  # Clear previous results
        for i, result in enumerate(results):
            result_text.insert(tk.END, f"{i + 1}] {result['wine_name']}\n\n{result['review_note']}\n\nSentiment: {result['sentiment']}\n\n")

    #* main window config
    root = tk.Tk()
    
    root.title("wineTz")
    root.configure(bg="white")
    root.minsize(850, 500)
    root.maxsize(850, 500)

    top_frame = Frame(root, relief="solid", borderwidth=0, bg="white")
    top_frame.pack(side="top", fill="both", expand=True)
    
    left_frame = Frame(root, relief="solid", borderwidth=0, bg="DodgerBlue2")
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = Frame(root, relief="solid", borderwidth=0, bg="lawn green")
    right_frame.pack(side="right", fill="both", expand=True)

    #* Image init
    imageBG = PhotoImage(file="static/wineTz2.gif")
    imageBG = imageBG.subsample(5, 5)
    imgLabel = Label(top_frame, image=imageBG, border=0)
    imgLabel.pack()

    #* BAR: Wine Type
    wine_types = ["Red Wine", "White Wine", "Rosé", "Sparkling Wine", "Dessert Wine", "Fortified Wine"]
    number_mapping = {
        "Red Wine": 1,
        "White Wine": 2,
        "Rosé": 3,
        "Sparkling Wine": 4,
        "Dessert Wine": 7,
        "Fortified Wine": 24
    }
    check_vars = [IntVar() for _ in range(len(wine_types))]

    typeBar = Frame(left_frame, width=180, height=185, bg="#7b191a")
    typeBar.grid(row=1, column=0, padx=5, pady=5, sticky="n")

    for i, wine_type in enumerate(wine_types):
        row_num = i // 2 + 2
        col_num = i % 2
        Checkbutton(typeBar, text=wine_type, variable=check_vars[i]).grid(row=row_num, column=col_num, padx=5, pady=3, sticky="w")

    #* BAR: Price
    priceBar = Frame(left_frame, width=180, height=185, bg="#e3cf87")
    priceBar.grid(row=3, column=0, padx=5, pady=5, sticky="n")
    Label(priceBar, text="Price", relief="raised").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    Entry(priceBar, width=4).grid(row=0, column=1, padx=5, pady=2, sticky="w")
    Entry(priceBar, width=4).grid(row=0, column=2, padx=5, pady=2, sticky="w")

    #* BAR: Sentiment
    sentimentBar = Frame(left_frame, width=180, height=185, bg="#fdf7d5")
    sentimentBar.grid(row=4, column=0, padx=5, pady=5, sticky="n")
    Button(sentimentBar, text="sentiment", width=5, highlightthickness=0, bd=0).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_below_sentiment = tk.Entry(sentimentBar, width=15)
    entry_below_sentiment.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    #* BAR: Field search for multifield
    selected_value = tk.StringVar()
    fieldBar = Frame(left_frame, width=180, height=185, bg="#cb8e92")
    fieldBar.grid(row=5, column=0, padx=5, pady=5, sticky="n")
    Label(fieldBar, text="Field", relief="raised").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    combo_options = ["Default", "Opzione 2", "Opzione 3", "Opzione 4"]
    combo = ttk.Combobox(fieldBar, values=combo_options, textvariable=selected_value)
    combo.grid(row=0, column=1, padx=10, pady=10)

    combo.set("Opzione predefinita")

    #* BAR: Environment
    var = True
    var = tk.BooleanVar(value=True)

    downBar = Frame(left_frame, width=180, height=185, bg="#d5833f", highlightthickness=0, bd=0)
    downBar.grid(row=6, column=0, padx=5, pady=5, sticky="n")
    Button(downBar, text="export", width=5, highlightthickness=0, bd=0, command=exportReport).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    Button(downBar, text="refresh", width=5, highlightthickness=0, bd=0).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    
    environmentBar = Frame(left_frame, width=180, height=185, bg="#420705",highlightthickness=0, bd=0)
    environmentBar.grid(row=7, column=0, padx=5, pady=5, sticky="n")
    Checkbutton(environmentBar, text="Ac", variable=var).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="Th", variable=var).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="TF-IDF", variable=var).grid(row=0, column=3, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="BM25F", variable=var).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    Button(environmentBar, text="index", width=5, highlightthickness=0, bd=0, command=loadIndexGUI).grid(row=0, column=5, padx=10, pady=5, sticky="w")

    #* Right Frame -> query and results
    queryText = Entry(right_frame, width=20)
    queryText.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    Button(right_frame, text="Search", width=10, highlightthickness=0, bd=0, command=on_search_click).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    result_text = scrolledtext.ScrolledText(right_frame, wrap="word", width=50, height=20, font=("Helvetica", 12))
    result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="n")

    root.mainloop()

if __name__ == '__main__':

    ix = loadIndexCLI ()
    
    loadGUI(ix)