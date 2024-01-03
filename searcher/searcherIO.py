import os

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, AndGroup, OrGroup
from whoosh.query import And, AndNot, Not, AndMaybe, Term, Or
from whoosh.query import NumericRange
from whoosh import scoring
from nltk.corpus import wordnet

import tkinter as tk
from tkinter import Tk, messagebox

def loadIndex (GUI):

    if GUI:
        indexPath = "../index"
        
        if not os.path.exists(indexPath) and not os.path.isdir(indexPath):
            
            root = Tk()
            root.withdraw()
            messagebox.showerror('wineTz', 'The index was not loaded. \n\nThe interface will launch, but you have to load the index manually via the button.')
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

def searchFromThesaurus (sentence): 
    words = sentence.split()
    synonyms = []

    for word in words:
        synonyms = [lemma.name() for syn in wordnet.synsets(word, lang='ita') for lemma in syn.lemmas('ita')]
        synonyms.extend(synonyms)

    synonyms = list(set(synonyms))

    return synonyms

def updateQuery (UImode, sentCorrected, sentNotCorrected): 

    if UImode:
        result = messagebox.askyesno("wineTz", f"Did you mean '{sentCorrected}' ?")
        if result:
            return sentCorrected
        else:
            return sentNotCorrected
    else: 
        choice = input (f"Did you mean {sentCorrected}? y/N")
        
        if choice == 'y':
            return sentCorrected
        else:
            return sentNotCorrected

def queryReply (ix, parameters, queryText): 

    """
        specialized and extended query parser to consider all available parameters
    Returns:
        rObject: formatted string object of users request
        results: list of results of the corresponding query
    """

    UIMode, searchField, priceInterval, wineTypes, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year = parameters
    
    #* parser parameters init
    scoreMethod = scoring.TF_IDF() if algorithm else scoring.BM25F()
    searcher = ix.searcher(weighting=scoreMethod)

    searchingMode = AndGroup if andFlag else OrGroup
    parser = MultifieldParser(searchField, schema=ix.schema, group=searchingMode)

    #* TEXT in query
    mainQuery = parser.parse(queryText)
    
    queryCopy = queryText
    queryInWork = [queryCopy, queryCopy, queryCopy]

    # Whoosh correction tool 
    if correctionFlag: 
        corrected_query = searcher.correct_query(mainQuery, queryText) 
        if corrected_query.query != mainQuery:
            updated = updateQuery (UIMode, corrected_query.string, queryText)
            queryInWork = [queryCopy, updated, updated]
            mainQuery = parser.parse(updated)
    
    # Wordnet tool 
    if thesaurusFlag:
        synonyms = searchFromThesaurus (queryInWork[1])
        stringResearch = f"{' '.join(synonyms)}" if synonyms else queryInWork[1]
        if stringResearch != queryInWork[1]:
            queryInWork = [queryCopy, queryInWork[1], stringResearch]
            mainQuery = parser.parse(stringResearch)
            print ("with thesaurus extension: ", stringResearch)
            if UIMode:
                    messagebox.showinfo("wineTz", f"matches \"{stringResearch}\"")

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
    
    results = searcher.search(mainQuery, filter = combined_filter, limit=None)

    '''
        the following lines are useful to extend the search as much as possible.
        the user's choice is always considered.
    '''

    if not correctionFlag:
        if len(results) == 0:
            choice = messagebox.askyesno("wineTz", "No matches found\nEnable tools for search extension?")
            if choice:
                mainQuery = parser.parse(queryText)
                corrected_query = searcher.correct_query(mainQuery, queryText) 
                if corrected_query.query != mainQuery:
                    return queryReply(ix, parameters, corrected_query.string)

    rObject = objectFormatter (queryInWork[0], queryInWork[1], queryInWork[2], mainQuery, combined_filter, searchField, andFlag, sentimentRequest, algorithm, len(results), correctionFlag, thesaurusFlag)
    
    if UIMode:
        print (rObject)

    return rObject, results

def resultFormatter (result): 
        
    """
        useful for reading the request result in the most readable format
    """
    
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
    wine_winery = result['wine_winery']
    wine_price = result['wine_price']
    review_note = result['review_note']
    sentiment = result['sentiment']
    score = result.score

    formatted_result = (
        f"{i}] Score: {score:.2f}\t| Sentiment Score: {sentiment} |\n"
        f"{wine_type}: "
        f"{wine_name}\t"
        f"|{wine_year}|\t"
        f"Winery: {wine_winery}\t"
        f"|{wine_price}€|\n"
        f"Note: {review_note}\n"
        f"{'_'*40}\n"
    )

    return formatted_result

def printResultsCLI (rObject, results):

    """
        printing of results and formatted request object
        useful when starting from CLI interface
    """

    print (rObject)
    print ("\n")
    print (f"{len(results)} match(es).\n")

    for result in results: 
        print (resultFormatter(result))

    print (f"{'*'*40}\nend of results")

def objectFormatter (inText, inQuery, finalText, mainQuery, combined_filter, searchField, andFlag, sentimentRequest, algorithm, nMatches, correctionFlag, thesaurusFlag): 

    """
        useful for reading the request object in the most readable format
    """

    algoString = "ALGORITHM: BM25F\t"
    if algorithm:
        algoString = "ALGORITHM: TD-IDF\t"

    searchMode = "MODE: OR-Query\t"
    if andFlag:
        searchMode = "MODE: AND-Query\t"

    corrString = "correction tools: disabled\t"
    if correctionFlag:
        corrString = "correction tools: enabled\t"

    thString = "thesaurus tools: disabled\n"
    if thesaurusFlag:
        thString = "thesaurus tools: enabled\n"

    rObject = (
        "\n______request object______\n"
        f"inTEXT: [{inText}]\t inQUERY: [{inQuery}]\n"
        f"extended inQUERY: [{finalText}]\n"
        f"QUERY: {str(mainQuery)}\n"
        f"FILTERS: {str(combined_filter)}\n"
        f"FIELD(s): {str(searchField)}\n"
        f"{algoString} {searchMode} inSENTIMENT: {str(sentimentRequest)} \n"
        f"{corrString} {thString}"
        f"\n{nMatches}  match(es).\n"
        f"{str('_'*30)}"
    ) if inQuery != finalText else (
            "\n______request object______\n"
            f"inTEXT: [{inText}]\t inQUERY: [{inQuery}]\n"
            f"QUERY: {str(mainQuery)}\n"
            f"FILTERS: {str(combined_filter)}\n"
            f"FIELD(s): {str(searchField)}\n"
            f"{algoString} {searchMode} inSENTIMENT: {str(sentimentRequest)} \n"
            f"{corrString} {thString}"
            f"\n{nMatches}  match(es).\n"
            f"{str('_'*30)}"
        )

    return rObject

def exportTXT (outPath, data):
    
    rObject = data[0]
    results = data [1]

    with open (outPath, 'w') as fo:
    
            fo.write (rObject)
            for result in results:
                fo.write(resultFormatter(result))
        
    print (f"data exported in {outPath}.\n")

if __name__ == "__main__":
    raise ImportError("This is not an executable program: run searcher.py")