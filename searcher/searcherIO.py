import os

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, AndGroup, OrGroup, QueryParser
from whoosh.query import And, AndNot, Not, AndMaybe, Term, Or
from whoosh.query import NumericRange
from whoosh import scoring
from autocorrect import Speller

import tkinter as tk
from tkinter import Tk, messagebox

def loadIndex (GUI):

    if GUI:
        indexPath = "../index"
        
        if not os.path.exists(indexPath) and not os.path.isdir(indexPath):
            
            root = Tk()
            root.withdraw()
            messagebox.showerror('wineTz', 'The index was not loaded. \n\nThe interface will launch, but enter the index manually via the button.')
            root.after(1, root.destroy)
            root.mainloop()
            
            return None
        
        ix = open_dir(indexPath)
        return ix

    indexPath = input("Type the path to the index directory [or press enter]> ")
    indexPath = indexPath if indexPath else "../index"

    if not os.path.exists(indexPath) and not os.path.isdir(indexPath):
        print ("] error during loading index: directory not found.\n")
        quit()

    ix = open_dir(indexPath)
    
    print (f"Number of items in loaded index: {ix.doc_count_all()}")
    
    return ix

def queryReply (ix, parameters, queryText): 

    searchField, priceInterval, wineTypes, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year = parameters
    
    #* parser parameters init
    scoreMethod = scoring.TF_IDF() if algorithm else scoring.BM25F()
    searcher = ix.searcher(weighting=scoreMethod)

    searchingMode = AndGroup if andFlag else OrGroup
    parser = MultifieldParser(searchField, schema=ix.schema, group=searchingMode)

    #* TEXT in query
    mainQuery = parser.parse(queryText)

    #! Todo: thesaurus and correction

    #* PRICE in query
    if priceInterval:
        minPrice, maxPrice = map(float, priceInterval)
        priceQuery = NumericRange("wine_price", minPrice, maxPrice, startexcl=True, endexcl=True)
        mainQuery = And([mainQuery, priceQuery])

    #* SENTIMENT in query
    if sentimentRequest:
        match sentimentRequest [0]:
            case "L":
                mainQuery = AndNot(mainQuery, Term("sentiment", sentimentRequest[1]))

            case "l":
                mainQuery = AndMaybe(mainQuery, Not(Term("sentiment", sentimentRequest[1])))

            case "M":
                mainQuery = And([Term("sentiment", sentimentRequest[1]), mainQuery])
            
            case "m":
                mainQuery = AndMaybe([Term("sentiment", sentimentRequest[1]), mainQuery])

            case _:
                print ("\n\n] error detected: sentiment score attribution in query exploration.\n\n")
                quit()
    
    combined_filter = None
    
    #* TYPE in query
    wineFilters = None
    if wineTypes:
        filter_conditions = [Term("wine_type", wt) for wt in wineTypes]
        wineFilters = Or(filter_conditions)

        if combined_filter:
            combined_filter = And ([combined_filter, wineFilters])
        else:
            combined_filter = wineFilters

    #* YEAR in query
    yearFilter = None
    if year: 
        yearFilter = Term ("wine_year", year)

        if combined_filter:
            combined_filter = And ([combined_filter, yearFilter])
        else:
            combined_filter = yearFilter
    
    rObject = "\n______request object______\n" + f"TEXT: [{queryText}]\t QUERY: {queryText}\nPARAMETERS: " + str(mainQuery) + "\nFILTERS: " + str(combined_filter) + "\n" + str("_"*30) + "\n"
    print (rObject)

    results = searcher.search(mainQuery, filter = combined_filter, limit=100)
    return rObject, results

def printingResultsCLI (results):

    print ("Printing results: ")
    for i, result in enumerate(results):
            print(i, "] ",result["wine_name"], "tipo:", result["wine_type"], "\n", f"sentiment: {result['sentiment']}", "Price: ", result["wine_price"], "\n\n")

if __name__ == '__main__':

    ix = loadIndex (GUI=True)
    

    searchField = ["wine_name", "style_description", "review_note", "wine_winery"]
    priceInterval = [(None), (None)]
    # wineType = ["1"]
    sentimentRequest = (["M", "joy"])
    algorithm = False
    andFlag = False
    thesaurusFlag = False
    correctionFlag = False

    priceInterval = None
    wineType = ["1", "2"]
    sentimentRequest = (["M", "joy"])

    year = 2021

    parameters = searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year

    while True: 
        queryText = input ("type query> ")
        
        results = queryReply (ix, parameters, queryText)
        printingResultsCLI (results[1])


    results = queryReply (ix)
    printingResultsCLI (results)


