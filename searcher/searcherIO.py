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

    UIMode, searchField, priceInterval, wineTypes, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year = parameters
    
    #* parser parameters init
    scoreMethod = scoring.TF_IDF() if algorithm else scoring.BM25F()
    searcher = ix.searcher(weighting=scoreMethod)

    searchingMode = AndGroup if andFlag else OrGroup
    parser = MultifieldParser(searchField, schema=ix.schema, group=searchingMode)

    #* TEXT in query
    mainQuery = parser.parse(queryText)

    #! Todo: thesaurus and correction

    #* PRICE in query
    if priceInterval != None:
        minPrice, maxPrice = priceInterval
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
    
    algoString = "ALGORITHM: BM25F\t"
    if algorithm:
        algoString = "ALGORITHM: TD-IDF\t"

    searchMode = "MODE: OR-Query\t"
    if andFlag:
        searchMode = "MODE: AND-Query\t"

    rObject = objectFormatter (queryText, queryText, mainQuery, combined_filter, searchField, searchMode, sentimentRequest, algoString)
    
    if UIMode:
        print (rObject)

    results = searcher.search(mainQuery, filter = combined_filter, limit=1000)
    return rObject, results

def resultFormatter (result): 
        
        number_mapping = {
            "Red Wine": 1,
            "White Wine": 2,
            "Rosé": 3,
            "Sparkling Wine": 4,
            "Dessert Wine": 7,
            "Fortified Wine": 24
        }

        reverse_mapping = {v: k for k, v in number_mapping.items()}
        typeName = reverse_mapping.get(int(result['wine_type']), "ND type")

        i = result.rank + 1

        wine_type = typeName
        wine_name = result['wine_name']
        wine_year = result['wine_year']
        wine_price = result['wine_price']
        review_note = result['review_note']
        sentiment = result['sentiment']
        score = result.score

        formatted_result = (
            "\n"
            f"{i}] Score: {score:.2f}\n"
            f"{wine_type}: \t"
            f"{wine_name}\t"
            f"|{wine_year}|\t"
            f"Price: {wine_price}\n"
            f"Note: {review_note}\n"
            f"Sentiment: {sentiment}\n"
            f"{'_'*40}\n"
        )

        return formatted_result

def printResultsCLI (rObject, results):

    print (rObject)
    print ("\n")
    print (f"{len(results)} match(es).\n")

    for result in results: 
        print (resultFormatter(result))

    print (f"{'*'*40}\nend of results")

def objectFormatter (inText, queryText, mainQuery, combined_filter, searchField, searchMode, sentimentRequest, algoString): 

    rObject = "\n______request object______\n" + f"inTEXT: [{inText}]\t inQUERY: {queryText}\nQUERY: " + str(mainQuery) + "\nFILTERS: " + str(combined_filter) +"\n" + "FIELD(s): "+ str(searchField) + "\n" + algoString + searchMode + "inSENTIMENT: " + str(sentimentRequest) + "\n" + str("_"*30)

    return rObject

def exportTXT (outPath, data):
    
    rObject = data[0]
    results = data [1]

    with open (outPath, 'w') as fo:
    
            fo.write (rObject)
            for result in results:
                fo.write(resultFormatter(result))
        
    print (f"data exported in {outPath}.\n")

if __name__ == '__main__':

    ix = loadIndex (GUI=False)

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
    #sentimentRequest = (["M", "joy"])

    sentimentRequest = None

    year = None

    parameters = searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year

    while True: 
        queryText = input ("type query> ")
        
        results = queryReply (ix, parameters, queryText)
        printingResultsCLI (results[1])


    results = queryReply (ix)
    printingResultsCLI (results)


