import os

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, AndGroup, OrGroup, QueryParser
from whoosh.query import And, AndNot, Not, AndMaybe, Term, Or
from whoosh.query import NumericRange
from whoosh import scoring
from autocorrect import Speller

def loadIndexCLI ():

    indexPath = input("Type the path to the index directory [or press enter]> ")
    indexPath = indexPath if indexPath else "../index"

    if not os.path.exists(indexPath) and os.path.isdir(indexPath):
        print ("] error during loading index: directory not found.\n")
        quit()

    ix = open_dir(indexPath)
    
    print (f"Number of items in loaded index: {ix.doc_count_all()}")
    
    return ix

def queryReply (ix, parameters, queryText): 

    searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag = parameters
    
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
                mainQuery = AndNot([Term("sentiment", sentimentRequest[1]), mainQuery])

            case "l":
                mainQuery = AndMaybe(mainQuery, Not(Term("sentiment", sentimentRequest[1])))

            case "M":
                mainQuery = And([Term("sentiment", sentimentRequest[1]), mainQuery])
            
            case "m":
                mainQuery = AndMaybe([Term("sentiment", sentimentRequest[1]), mainQuery])

            case _:
                print ("\n\n] error detected: sentiment score attribution in query exploration.\n\n")
                quit()
    
    #* TYPE in query
    if wineType:
        print(wineType)
        wineTypeQueries = [Term("wine_type", wt) for wt in wineType]
        wineTypeQuery = Or(wineTypeQueries)
        mainQuery = And([mainQuery, wineTypeQuery])

    if wineType:
        for wt in wineType:
            

    results = searcher.search(mainQuery, limit=100)
    return results

def printingResultsCLI (results):

    print ("Printing results: ")
    for i, result in enumerate(results):
            print(i, "] ",result["wine_name"], "tipo:", result["wine_type"], "\n", f"sentiment: {result['sentiment']}", "Price: ", result["wine_price"], "\n\n")

if __name__ == '__main__':

    ix = loadIndexCLI ()

    searchField = ["wine_name", "style_description", "review_note", "wine_winery"]
    priceInterval = [(8.55), (10.00)]
    # wineType = ["1"]
    sentimentRequest = (["M", "joy"])
    algorithm = False
    andFlag = False
    thesaurusFlag = False
    correctionFlag = False

    priceInterval = None
    wineType = ["1"]
    sentimentRequest = (["M", "joy"])


    parameters = searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag 

    while True: 
        queryText = input ("type query> ")
        
        results = queryReply (ix, parameters, queryText)
        printingResultsCLI (results)


    results = queryReply (ix)
    printingResultsCLI (results)


