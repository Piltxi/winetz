import math
import sys

sys.path.append('../searcher')
from searcherIO import loadIndex, queryReply, printResultsCLI, resultFormatter

'''
    code to add search parameters 

    UIMode, searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year = parameters

    UIMode = False

    searchField = ["wine_name", "review_note", "wine_winery"]
    priceInterval = [(None), (10)]
    wineType = ["1"]
    sentimentRequest = (["M", "joy"])
    algorithm = False
    andFlag = False
    thesaurusFlag = False
    correctionFlag = False
    year = None

    parameters = UIMode searchField                                   priceInterval    wineType     sentimentRequest    algorithm,  thesaurusFlag   andFlag     correctionFlag  year
    parameters = [False, ["wine_name", "review_note", "wine_winery"], [(None), (20)], ["1", "2"],   (["M", "joy"]),     False,      False,          False,       False,           None]
'''

def dcg (scores):
    gains=[scores[0]]
    dg=[scores[0]]

    for s in range(1, len(scores)):
        dg.append(scores[s]/math.log(1+s, 2))
        gains.append(round(gains[s-1]+dg[s], 3))
    
    return gains

def ndcg(scores):
    lenght = len(scores)-1
    num = dcg(scores)[lenght]
    
    scores.sort(reverse=True)
    
    return round(num/dcg(scores)[lenght], 3)

def applyRelevance (rObject, results): 

    print ("Query inserted: ", rObject)

    relevance = []
    for result in results: 
        print (resultFormatter(result))
        relevance.append(int(input("Insert relevance about this result: ")))

    return relevance

def benchmarksQueries(ix): 

    # About "valpolicella" wine
    queryText = "Valpolicella"
    parameters = [False, ["wine_name"], None, ["1"], (None), False, False, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject)
    
    # About "Valdo" winery
    queryText = "Valdo"
    parameters = [False, ["wine_winery"], None, None, (None), False, False, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About "Montepulciano" wine, high->joy sentiment requests, 10:20 price interval
    queryText = "Montepulciano"
    parameters = [False, ["wine_name"], [(10), (20)], ["1"], (["M", "joy"]), False, False, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About white wine, meat and fish, high->joy sentiment requests
    queryText = "carne e pesce"
    parameters = [False, ["review_note"], [(20), (30)], ["1", "2"], (["M", "joy"]), False, False, True, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About white wine, meat and fish, high->joy sentiment requests
    queryText = "carne e pesce"
    parameters = [False, ["review_note"], [(20), (30)], ["1", "2"], (["M", "joy"]), False, False, True, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About steak [without and with th.extension]
    queryText = "bistecca"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), False, False, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    queryText = "bistecca"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), False, True, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About cheap wines, high->sadness sentiment requests
    queryText = "economico"
    parameters = [False, ["review_note"], None, None, (["M", "sadness"]), False, False, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About wines to celebrate, high->joy sentiment requests, price 0:20 [without and with th.extension]
    queryText = "festa"
    parameters = [False, ["review_note"], [(None), (20)], None, (["M", "joy"]), False, False, False, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    queryText = "festa"
    parameters = [False, ["review_note"], [(None), (20)], None, (["M", "joy"]), False, False, True, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About wines with great personality, year 2012
    queryText = "grande personalità"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), False, False, True, False, 2012]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About fortified wines with hints of honey
    queryText = "miele"
    parameters = [False, ["review_note"], None, ["24"], None, False, False, True, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    # About 'lambrusco' and 'gnocco fritto': two typical delicacies of Emilia Romagna, Italy
    queryText = "lambrusco e gnocco fritto"
    parameters = [False, ["wine_name", "review_note"], None, None, None, False, False, True, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

    queryText = " > wine_name:lambrusc AND review_note:gnocc AND review_note:fritt"
    parameters = [False, ["wine_name", "review_note"], None, None, None, False, False, True, False, None]
    rObject, results = queryReply(ix, parameters, queryText)
    print (rObject) 

if __name__ == '__main__':

    ix = loadIndex(GUI=False, rebooting=False)
    benchmarksQueries (ix)