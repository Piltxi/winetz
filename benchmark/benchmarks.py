import math
import sys

sys.path.append('..')
from searcher.searcherIO import loadIndex, queryReply, printResultsCLI, resultFormatter

def dcg(scores):
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

def benchmarks (ix): 
    
    UIMode = False

    searchField = ["wine_name", "style_description", "review_note", "wine_winery"]
    priceInterval = [(None), (None)]
    wineType = ["1"]
    sentimentRequest = (["M", "joy"])
    algorithm = False
    andFlag = False
    thesaurusFlag = False
    correctionFlag = False
    year = None

    queryText = "petit"

    parameters = [False, ["wine_name", "style_description", "review_note", "wine_winery"], [(None), (20)], ["1"], (["M", "joy"]), False, False, False, False, 2021]
    
    # parameters = UIMode, searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year
    rObject, results = queryReply(ix, parameters, queryText)
    # printResultsCLI(rObject, results)

    relevance = applyRelevance (rObject, results)

    if relevance: 
        print (f"DCG values: {dcg(relevance)}")
        print (f"\nNDCG values: {ndcg(relevance)}")


if __name__ == '__main__':

    ix = loadIndex(GUI=False)
    
    benchmarks (ix)

    

