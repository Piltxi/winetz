import os
import argparse

import tkinter as tk
from tkinter import Scale, Toplevel, ttk
from tkinter import filedialog
from tkinter import Tk, Frame, Label, Button, Entry, Checkbutton, scrolledtext, PhotoImage
from tkinter import StringVar, IntVar, DoubleVar, BooleanVar
from tkinter import messagebox

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.query import And, AndNot, Not, AndMaybe, Term

from correctionsAnalysis import *
from searcherIO import loadIndex, queryReply, resultFormatter, exportTXT

# from searcherIO import printingResultsCLI

sentimentRequest = {'emotion': None, 'level': None}

def translateSentiment (sentimentRequest): 
    
    corrispondence = {
        "Fear": "fear",
        "Angry": "angry",
        "Sadness": "sadness",
        "Joy": "joy",
        "Low": "L",
        "Middle-Low": "l",
        "Middle-High": "m",
        "High": "M"
    }

    emotion = sentimentRequest.get('emotion')
    level = sentimentRequest.get('level')

    if emotion is None: 
        return None

    if level is None: 
        translated_emotion = corrispondence.get(emotion)
        return ["M", translated_emotion]
    
    translated_emotion = corrispondence.get(emotion)
    translated_level = corrispondence.get(level)

    if translated_emotion is None or translated_level is None:
        print ("] Error in sentiment translator")
        quit()
    
    return [translated_level, translated_emotion]

def loadGUI (ix): 

    global lastResearch

    def changeAlgorithm (): 
        
        #! To do
        
        bm25Flag.set(0)
        tfidfFlag.set(0)

    def updateSentimentInfo (sentimentRequest): 
        
        """
            change info views in sentiment label on new choice event
        """

        entry_below_sentiment.delete(0, tk.END)
        
        if sentimentRequest['emotion'] == None: 
            entry_below_sentiment.config(fg="blue")
            entry_below_sentiment.insert(0, "Not Defined")

        else:
            entry_below_sentiment.config(fg="red")
            if sentimentRequest['level'] == None:
                entry_below_sentiment.insert(0, f"High -> {sentimentRequest['emotion']}")
            else: 
                entry_below_sentiment.insert(0, f"{sentimentRequest['level']} -> {sentimentRequest['emotion']}")

    def setSentimentConfig(): 

        """
            setSentimentConfig :: load window to insert sentiment filters
            
            when user press "sentiment" button, GUI loads new window in order 
            to insert sentiment configuration filter by two sliders. 
            first slider allows emotion choice between ["Fear", "Angry", "Sadness", "Joy"]
            second slider allows level emotion choice between ["Low", "Middle-Low", "Middle-High", "High"]

            idea: represent emotion by stars

        """

        def update_emotion(value):
            current_emotion = emotions[int(value)]
            emotion_label.config(text=f"Emotion: {current_emotion}")
            sentimentRequest['emotion'] = current_emotion
            print ("up emotion: ", sentimentRequest['emotion'])
            sentimentRequest['level'] = None

        def update_level(value):
            current_level = levels[int(value)]
            level_label.config(text=f"Level: {current_level}")
            sentimentRequest['level'] = current_level
            print ("up level: ", sentimentRequest['level'])

        sentimentWindow = Toplevel(root)
        sentimentWindow.title("Sentiment Configuration")
    
        emotion_label = tk.Label(sentimentWindow, text="Emotion: ")
        emotion_label.grid(row=0, column=0, columnspan=4)

        slider = tk.Scale(sentimentWindow, from_=0, to=3, orient=tk.HORIZONTAL, command=update_emotion, showvalue=0, length=300)
        slider.grid(row=1, column=0, columnspan=4)

        emotions = ["Fear", "Angry", "Sadness", "Joy"]
        for i, emotion in enumerate(emotions):
            tk.Label(sentimentWindow, text=emotion).grid(row=2, column=i)

        level_label = tk.Label(sentimentWindow, text="Level: ")
        level_label.grid(row=3, column=0, columnspan=4)

        sliderLevel = tk.Scale(sentimentWindow, from_=0, to=3, orient=tk.HORIZONTAL, command=update_level, showvalue=0, length=300)
        sliderLevel.grid(row=4, column=0, columnspan=4)

        levels = ["Low", "Middle-Low", "Middle-High", "High"]
        for i, level in enumerate(levels):
            tk.Label(sentimentWindow, text=level).grid(row=5, column=i)
        
        entry_below_sentiment.config(text=f"{str(sentimentRequest)}")

        sentimentWindow.resizable(False, False)

    def exportReport (): 

        """
            when user press "export" button
            GUI loads new window to load output report path

            after this, by searcherIO function, wineTz provides a .txt export of last research. 

            idea: save and check output for query

        """

        outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        exportTXT(outputPath, lastResearch)

    def loadIndexFromDialog():

        """

            when user press "index" button, GUI loads new window
            in order to select new index path. 

            with invalid path wineTz loads GUI, but user can't insert quey

            idea: change index data during wineTz execution

        """

        inputPath = filedialog.askdirectory()
        
        try:
            ix = open_dir(inputPath)
        except Exception as e:
            print ("] Error in loading index from: ", inputPath)
            messagebox.showerror('wineTz', 'The index was not loaded.')
            quit()

        print ("Loaded new index from: ", inputPath)
        print ("rebooting...")
        root.destroy()
        loadGUI(ix)

    def cleanParam (): 

        """
            idea: wineTz works with a lot of filters research.
            user must can refresh research to all parameters, in order to re-insert them
        """

        for flag in wineTypes:
            flag.set(0)

        sentimentRequest = {'emotion': None, 'level': None}

        minPriceEntry.set("")
        maxPriceEntry.set("")
        yearEntry.set("")

        andFlag.set(0)
        bm25Flag.set(0)
        tfidfFlag.set(0)
        thesaurusFlag.set(0)
        autoCorrectionFlag.set(0)

        combo.set("in: [All fields]")

        queryText.delete(0, tk.END)
        result_text.delete(1.0, tk.END)
        entry_below_sentiment.delete(0, tk.END)

    def disable_event(event):

        """
            disable event useful method to lock status of label
        """

        return "break"

    def searcherButton (): 
        query_string = queryText.get()

        default = ["wine_name", "style_description", "review_note", "wine_winery"]
        sentimentInQuery = translateSentiment (sentimentRequest)
        selected_numbers = [number_mapping[wine_type] for wine_type, var in zip(wine_types, wineTypes) if var.get() == 1]

        algorithm = False
        if not bm25Flag.get():
            if tfidfFlag.get():
                algorithm = True

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

        updateSentimentInfo (sentimentRequest)

        UIMode = True
        parameters = UIMode, searchField, priceInterval, selected_numbers, sentimentInQuery, algorithm, thesaurusFlag, andFlag.get(), autoCorrectionFlag, yearV
        question, results = queryReply (ix, parameters, query_string)

        global lastResearch 
        lastResearch = [question, results]


        if results:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"{len(results)} match(es).\n")
            
            for i, result in enumerate(results):  
                result_text.insert(tk.END, resultFormatter(result))

        else: 
            result_text.delete(1.0, tk.END)
            result_text.config( fg="white", bg="black")
            result_text.insert(tk.END, "NO MATCHES FOUND")
            result_text.tag_configure("custom_tag", foreground="red", font=("Helvetica", 14, "bold"), justify='center')
            result_text.tag_add("custom_tag", "1.0", "end")
    

    #* main window config
    root = tk.Tk()
    
    root.title("wineTz")
    root.configure(bg="white")
    root.minsize(800, 450)
    root.maxsize(800, 450)

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
    Button(sentimentBar, text="sentiment", width=5, highlightthickness=0, bd=0, command=setSentimentConfig).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_below_sentiment = tk.Entry(sentimentBar, width=15)
    entry_below_sentiment.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    entry_below_sentiment.bind("<Key>", disable_event)

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

    downBar = Frame(left_frame, width=180, height=185, bg="#d5833f", highlightthickness=0, bd=0)
    downBar.grid(row=6, column=0, padx=5, pady=5, sticky="n")
    Button(downBar, text="export", width=5, highlightthickness=0, bd=0, command=exportReport).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    Button(downBar, text="refresh", width=5, highlightthickness=0, bd=0, command=cleanParam).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    Button(downBar, text="index", width=5, highlightthickness=0, bd=0, command=loadIndexFromDialog).grid(row=0, column=3, padx=10, pady=5, sticky="w")

    autoCorrectionFlag = BooleanVar(value=True)
    thesaurusFlag = BooleanVar(value=False)
    tfidfFlag = BooleanVar(value=False)
    bm25Flag = BooleanVar(value=True)

    environmentBar = Frame(left_frame, width=180, height=185, bg="#420705",highlightthickness=0, bd=0)
    environmentBar.grid(row=7, column=0, padx=5, pady=5, sticky="n")
    Checkbutton(environmentBar, text="Ac", variable=autoCorrectionFlag).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="Th", variable=thesaurusFlag).grid(row=0, column=2, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="TF-IDF", variable=tfidfFlag, command=changeAlgorithm).grid(row=0, column=3, padx=10, pady=5, sticky="w")
    Checkbutton(environmentBar, text="BM25F", variable=bm25Flag, command=changeAlgorithm).grid(row=0, column=4, padx=10, pady=5, sticky="w")
    
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