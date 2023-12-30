import os
import argparse

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import Tk, Frame, Label, Button, Entry, Checkbutton, scrolledtext, PhotoImage
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from tkinter import messagebox

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.query import And, AndNot, Not, AndMaybe, Term

from correctionsAnalysis import *
from searcherIO import loadIndex, queryReply

from searcherIO import printingResultsCLI


def loadGUI (ix): 

    global lastResearch

    def exportReport (): 
        outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        with open (outputPath, 'w') as fo:
            
            rObject, results = lastResearch

            fo.write (rObject)

            for i, result in enumerate(results):
                print(i, "] ",result["wine_name"], "\n\n",result["review_note"], "\n\n", f"sentiment: {result['sentiment']}", "Price: ", result["wine_price"])

                strResponse = f"{i} ] {result['wine_name']}\n\n{result['review_note']}\n\nsentiment: {result['sentiment']} Price: {result['wine_price']}"
                print ("RISPOTA: ", strResponse)

                fo.write(strResponse)

            # for i, result in enumerate (results): 
            #     fo.write (i, "] ",result["wine_name"], "\n\n",result["review_note"], "\n\n", f"sentiment: {result['sentiment']}", "Price: ", result["wine_price"])

            # for result in enumerate(results):
            #     fo.write (i, "] ",result["wine_name"], "tipo:", result["wine_type"], "\n", f"sentiment: {result['sentiment']}", "Price: ", result["wine_price"], "\n\n")
        
        print ("exported.")


    def loadIndexFromDialog():
        inputPath = filedialog.askdirectory()
        
        try:
            ix = open_dir(inputPath)
        except Exception as e:
            print ("Error in loading index from: ", inputPath)
            messagebox.showerror('wineTz', 'The index was not loaded.')

        print ("Loaded new index from: ", inputPath)
        print ("rebooting...")
        root.destroy()
        loadGUI(ix)

    def cleanParam (): 
        pass

    def disable_event(event):
        return "break"

    def searcherButton (): 
        query_string = queryText.get()

        default = ["wine_name", "style_description", "review_note", "wine_winery"]
        priceInterval = None
        sentimentRequest = (["M", "joy"])

        algorithm = False
        if not bm25Flag.get():
            if tfidfFlag.get():
                algorithm = True

        selected_numbers = [number_mapping[wine_type] for wine_type, var in zip(wine_types, wineTypes) if var.get() == 1]

        yearV = yearEntry.get()
        yearV = int(yearV) if yearV.strip() else None

        minPV = minPriceEntry.get()
        minPV = float(minPV) if minPV.strip() else None

        MaxPV = maxPriceEntry.get()
        MaxPV = float(MaxPV) if MaxPV.strip() else None
        
        if minPV == None and MaxPV == None:
            priceInterval = None 
        else:
            priceInterval = [minPV, MaxPV]

        selectedFields = combo.get()

        if selectedFields == "in: [All fields]":
            searchField = default
        else: 
            searchField = [mappingFields[selectedFields]]

        print ("Wine Type: ", wineTypes)
        print ("Wine Type: ", selected_numbers)
        print ("YYYY : ", yearV)
        print ("YYYY : ", minPV)
        print ("YYYY : ", MaxPV)

        parameters = searchField, priceInterval, selected_numbers, sentimentRequest, algorithm, thesaurusFlag, andFlag.get(), autoCorrectionFlag, yearV
        question, results = queryReply (ix, parameters, query_string)

        global lastResearch 
        lastResearch = [question, results]

        result_text.delete(1.0, tk.END)
        for i, result in enumerate(results):
            result_text.insert(tk.END, f"{i + 1}] {result['wine_name']}\n\n{result['review_note']}\n\nSentiment: {result['sentiment']}\n\n")

    #* main window config
    root = tk.Tk()
    
    root.title("wineTz")
    root.configure(bg="white")
    root.minsize(850, 450)
    root.maxsize(850, 450)

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
    wineTypes = [IntVar() for _ in range(len(wine_types))]

    typeBar = Frame(left_frame, width=180, height=185, bg="#7b191a")
    typeBar.grid(row=1, column=0, padx=5, pady=5, sticky="n")

    for i, wine_type in enumerate(wine_types):
        row_num = i // 2 + 2
        col_num = i % 2
        Checkbutton(typeBar, text=wine_type, variable=wineTypes[i]).grid(row=row_num, column=col_num, padx=5, pady=3, sticky="w")

    #* BAR: Price and Year
    priceBar = Frame(left_frame, width=180, height=185, bg="#e3cf87")
    priceBar.grid(row=3, column=0, padx=5, pady=5, sticky="n")
    Label(priceBar, text="Price", relief="raised").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    minPriceEntry = StringVar ()
    maxPriceEntry = StringVar ()
    Entry(priceBar, width=4, textvariable=minPriceEntry).grid(row=0, column=1, padx=5, pady=2, sticky="w")
    Entry(priceBar, width=4, textvariable=maxPriceEntry).grid(row=0, column=2, padx=5, pady=2, sticky="w")
    
    yearEntry = StringVar()
    Label(priceBar, text="Year", relief="raised").grid(row=0, column=3, padx=5, pady=5, sticky="w")
    Entry(priceBar, width=4, textvariable=yearEntry).grid(row=0, column=4, padx=5, pady=2, sticky="w")

    #* BAR: Sentiment
    sentimentBar = Frame(left_frame, width=180, height=185, bg="#fdf7d5")
    sentimentBar.grid(row=4, column=0, padx=5, pady=5, sticky="n")
    Button(sentimentBar, text="sentiment", width=5, highlightthickness=0, bd=0).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_below_sentiment = tk.Entry(sentimentBar, width=15)
    entry_below_sentiment.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    #* BAR: Field search for multifield and AND button
    fieldBar = Frame(left_frame, width=180, height=185, bg="#cb8e92")
    fieldBar.grid(row=5, column=0, padx=5, pady=5, sticky="n")
    Label(fieldBar, text="Field", relief="raised").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    combo_options = ["in: [All fields]", "in: [Wine Name]", "in: [Vinery]", "in: [Review]", "in: [Description]"]
    default = ["wine_name", "style_description", "review_note", "wine_winery"]
    mappingFields = {
        "in: [All fields]" : default,
        "in: [Wine Name]" : "wine_name", 
        "in: [Vinery]" : "wine_winery",
        "in: [Review]" : "review_note",
        "in: [Description]" : "style_description"
    }
    combo = ttk.Combobox(fieldBar, values=combo_options)
    combo.grid(row=0, column=1, padx=10, pady=10)
    combo.set("in: [All fields]")

    andFlag = BooleanVar(value=False)
    Checkbutton(fieldBar, text="AND", variable=andFlag).grid(row=0, column=2, padx=10, pady=5, sticky="w")

    #* BAR: Environment
    var = True
    var = tk.BooleanVar(value=True)

    downBar = Frame(left_frame, width=180, height=185, bg="#d5833f", highlightthickness=0, bd=0)
    downBar.grid(row=6, column=0, padx=5, pady=5, sticky="n")
    Button(downBar, text="export", width=5, highlightthickness=0, bd=0, command=exportReport).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    Button(downBar, text="refresh", width=5, highlightthickness=0, bd=0).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    
    autoCorrectionFlag = BooleanVar(value=True)
    thesaurusFlag = BooleanVar(value=False)
    tfidfFlag = BooleanVar(value=False)
    bm25Flag = BooleanVar(value=True)

    environmentBar = Frame(left_frame, width=180, height=185, bg="#420705",highlightthickness=0, bd=0)
    environmentBar.grid(row=7, column=0, padx=5, pady=5, sticky="n")
    Checkbutton(environmentBar, text="Ac", variable=autoCorrectionFlag).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="Th", variable=thesaurusFlag).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="TF-IDF", variable=tfidfFlag).grid(row=0, column=3, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="BM25F", variable=bm25Flag).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    
    Button(environmentBar, text="index", width=5, highlightthickness=0, bd=0, command=loadIndexFromDialog).grid(row=0, column=5, padx=10, pady=5, sticky="w")

    #* Right Frame -> query and results
    queryText = Entry(right_frame, width=20)
    queryText.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    Button(right_frame, text="Search", width=10, highlightthickness=0, bd=0, command=searcherButton).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    result_text = scrolledtext.ScrolledText(right_frame, wrap="word", width=50, height=20, font=("Helvetica", 12))
    result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="n")
    result_text.bind("<Key>", disable_event)

    root.mainloop()

if __name__ == '__main__':

    ix = loadIndex (GUI=True)
    
    correctionTool = initCorrectionTool ()

    loadGUI(ix)