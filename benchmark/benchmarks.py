import sys
sys.path.append('..')

# Ora puoi fare l'import relativo
from searcher.searcherIO import loadIndex, queryReply, printResultsCLI


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

    parameters = UIMode, searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year
    rObject, results = queryReply(ix, parameters, queryText)
    printResultsCLI(rObject, results)

    


if __name__ == '__main__':

    ix = loadIndex(GUI=False)
    benchmarks (ix)

    

