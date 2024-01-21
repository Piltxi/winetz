import json
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

def applyRelevance (nlQuery, rObject, results): 

    print (nlQuery, "\n", rObject)

    resultMod = results [:100] if len(results) > 100 else results

    relevance = []
    for result in resultMod: 
        print (resultFormatter(result))
        relevance.append(int(input("Insert relevance about this result: ")))

    return relevance

def getBenchmarks (ix, allQuery): 

    allBenchmarks = []

    for query in allQuery:
        
        nlQuery, queryText, parameters = query
        rObject, results = queryReply(ix, parameters, queryText)
        relevance = applyRelevance (nlQuery, rObject, results)

        DCG_banch = dcg(relevance)
        NDCG_banch = ndcg(relevance)

        allBenchmarks.append ([nlQuery, relevance, DCG_banch, NDCG_banch])

        print("DCG values for first 10 document retrieved:\n", DCG_banch)
        print("Normalized DCG for 10 retrieved documents:\n", NDCG_banch)

    return allBenchmarks

def setBenchmarksQueries(): 

    allQuery = []

    nlQuery = "Query n1: 'Vino Valpolicella'"
    queryText = "Valpolicella"
    parameters = [False, ["wine_name"], None, ["1"], (None), True, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])
    
    nlQuery = "Query n2: 'Vini cantina Valdo'"
    queryText = "Valdo"
    parameters = [False, ["wine_winery"], None, None, (None), True, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n3: 'Vino Montepulciano, impressione positiva, Prezzo compreso tra 10 e 20€'"
    queryText = "Montepulciano"
    parameters = [False, ["wine_name"], [(10), (20)], ["1"], (["M", "joy"]), True, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n4: 'Vini bianchi adatti sia per la carne che per il pesce, recensioni positive, Prezzo compreso tra 20 e 30€'"
    queryText = "carne e pesce"
    parameters = [False, ["review_note"], [(20), (30)], ["1", "2"], (["M", "joy"]), True, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n5: 'Vini da abbinare a bistecche [con e senza thesaurus]'"
    queryText = "bistecca"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), True, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    queryText = "bistecca"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), True, True, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n6: ' Vini economici ma con recensioni tristi'"
    queryText = "economico"
    parameters = [False, ["review_note"], None, None, (["M", "sadness"]), True, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n7: 'Vini per festeggiare, sotto i 20€'"
    queryText = "festa"
    parameters = [False, ["review_note"], [(None), (20)], None, (["M", "joy"]), True, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    queryText = "festa"
    parameters = [False, ["review_note"], [(None), (20)], None, (["M", "joy"]), True, True, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n8: 'Vini di grande personalità del 2012'"
    queryText = "grande personalità"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), True, False, True, False, 2012]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n9: 'Vini Liquorosi con sentori di miele, recensioni positive'"
    queryText = "miele"
    parameters = [False, ["review_note"], None, ["24"], None, True, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "Query n10: 'Lambrusco con gnocco fritto'"
    queryText = "lambrusco e gnocco fritto"
    parameters = [False, ["wine_name", "review_note"], None, None, None, True, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    queryText = " > wine_name:lambrusc AND review_note:gnocc AND review_note:fritt"
    parameters = [False, ["wine_name", "review_note"], None, None, None, True, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    return allQuery

if __name__ == '__main__':

    ix = loadIndex(GUI=False, rebooting=False)
    
    allQuery = setBenchmarksQueries ()
    allBenchmarks = getBenchmarks(ix, allQuery)
    
    with open('benchmarks_data25.json', 'w') as json_file:
        json.dump(allBenchmarks, json_file, indent=2)