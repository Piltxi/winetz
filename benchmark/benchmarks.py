import math
import sys

sys.path.append('..')
from searcher.searcherIO import loadIndex, queryReply, printResultsCLI, resultFormatter

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

def queryForBenchmarks ():

    UIMode = False

    searchField = ["wine_name", "style_description", "review_note", "wine_winery"]
    priceInterval = [(None), (10)]
    wineType = ["1"]
    sentimentRequest = (["M", "joy"])
    algorithm = False
    andFlag = False
    thesaurusFlag = False
    correctionFlag = False
    year = None


def benchmarks(ix): 

    queryText = "tanti aromi e profumi"
    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (None), False, False, False, False, None]

    rObject, results = queryReply(ix, parameters, queryText)
    printResultsCLI(rObject, results)
    
    queryText = "spaghetti alle vongole"
    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (None), False, False, False, False, 2021]

    rObject, results = queryReply(ix, parameters, queryText)
    printResultsCLI(rObject, results)

    queryText = "nausea"
    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (None), False, False, False, False, 2021]

    queryText = "festa" # felice
    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (None), False, False, False, False, 2021]

    queryText = "grande personalità" # felice
    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (None), False, False, False, False, 2021]

    queryText = "gongorzola" # felice
    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (None), False, False, False, False, 2021]


if __name__ == '__main__':

    ix = loadIndex(GUI=False)
    benchmarks (ix)