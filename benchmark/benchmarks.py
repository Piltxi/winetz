import json
import math
import os
import subprocess
import sys

from query import setBenchmarksQueriesBM25F

sys.path.append('../searcher')
from searcherIO import loadIndex, queryReply, resultFormatter

'''
    code to add search parameters 

    UIMode = False
    UIMode, searchField, priceInterval, wineType, sentimentRequest, algorithm, thesaurusFlag, andFlag, correctionFlag, year = parameters

    searchField = ["wine_name", "review_note", "wine_winery"]
    priceInterval = [(None), (10)]
    wineType = ["1"]
    sentimentRequest = (["M", "joy"])
    algorithm = False
    andFlag = False
    thesaurusFlag = False
    correctionFlag = False
    year = None

    the following lines are examples of parameters specification in code:

    parameters = UIMode searchField                                   priceInterval    wineType     sentimentRequest    algorithm,  thesaurusFlag   andFlag     correctionFlag  year
    parameters = [False, ["wine_name", "review_note", "wine_winery"], [(None), (20)], ["1", "2"],   (["M", "joy"]),     False,      False,          False,       False,           None]
'''

def dcg (scores):
    
    """ Discounted cumulative gain calcula

    Returns:
        gains: list with gains calculated by user-assigned relevances
    """

    gains = [scores[0]]
    dg = [scores[0]]

    for s in range (1, len(scores)):
        dg.append(scores[s] / math.log (1+s, 2))
        gains.append(round(gains[s-1]+dg[s], 3))

    return gains

def ndcg(scores):
    
    """ Normalized discounted cumulative gain calcula

    Returns:
        gains: value calculated from Discounted cumulative gain calcula
    """

    lenght = len(scores)-1
    num = dcg(scores)[lenght]
    
    scores.sort(reverse=True)
    
    return round(num/dcg(scores)[lenght], 3)

def applyRelevance (nlQuery, rObject, results): 

    """ method to set relevance about result obtained with query

        applyRelevance works on a reduce numbers of obtained result
        is normally used to apply the relevance of the results obtained from different search algorithms:
        the number of results is reduced to 10.

    nlQuery: query in natural language
    rObject: query received by search engine module
    results: list of obtained result 

    Returns:
        relevance: list with user-assigned relevances
    """

    print (nlQuery, "\n", rObject)

    resultMod = results [:1] if len(results) > 10 else results

    relevance = []
    for result in resultMod: 
        print (resultFormatter(result))
        relValue = int(input("Insert relevance about this result: "))
        relevance.append((result, relValue))

    return relevance

def getBenchmarks(ix, allQuery): 
    
    """
    getBenchmarks works with queries list 
    - getBenchmarks show results for every query and it allows the user to set related relevance

    ix: index data object loaded
    allQuery: list with queries [defined in setBenchmarksQueries()]

    Returns:
        allBenchmarks: list with all queries and related relevance, DCG, and NDCG of obtained results
    """

    allBenchmarks = []

    for query in allQuery:
        
        nlQuery, queryText, parameters = query
        rObject, results = queryReply(ix, parameters, queryText)
        relevance = applyRelevance(nlQuery, rObject, results)

        DCG_banch = dcg([rel[1] for rel in relevance])
        NDCG_banch = ndcg([rel[1] for rel in relevance])

        allBenchmarks.append([nlQuery, relevance, DCG_banch, NDCG_banch])

        print("DCG values for first 10 documents retrieved:\n", DCG_banch)
        print("Normalized DCG for 10 retrieved documents:\n", NDCG_banch)

    return allBenchmarks

def exportResults (allBenchmarks, name): 

    if not os.path.exists("benchResults/"):
        try:
            os.makedirs("benchResults/")
        except subprocess.CalledProcessError as e:
            print(f"Error in creating the directory: {e}")

    # export measurements obtained with corrispondent queries [.txt]
    fileName = "benchResults/output" + name + ".txt"
    with open(fileName, 'w') as output_file:
        for benchmark in allBenchmarks:
            nlQuery, relevance, DCG_banch, NDCG_banch = benchmark

            output_file.write(f"Query: {nlQuery}\n")
            output_file.write("Relevance:\n")
            for rel in relevance:
                result, rel_score = rel
                output_file.write(f"  {result['review_note']}: {rel_score}\n")

            output_file.write(f"DCG values for first 10 documents retrieved: {DCG_banch}\n")
            output_file.write(f"Normalized DCG for 10 retrieved documents: {NDCG_banch}\n\n")

    # export measurements obtained with corrispondent queries [.json]
    fileName = "benchResults/output" + name + ".json"
    with open(fileName, 'w', encoding='utf-8') as json_file:
        for benchmark in allBenchmarks:
            nlQuery, relevance, DCG_banch, NDCG_banch = benchmark

            benchmark_data = {
                'Query': nlQuery,
                'Relevance': [{'result': result['review_note'], 'score': rel_score} for result, rel_score in relevance],
                'DCG_values': DCG_banch,
                'Normalized_DCG': NDCG_banch
            }

            json.dump(benchmark_data, json_file, indent=2)
            json_file.write('\n')

if __name__ == '__main__':

    ix = loadIndex(GUI=False, rebooting=False)
    
    allQuery = setBenchmarksQueriesBM25F ()
    allBenchmarks = getBenchmarks(ix, allQuery)
    exportResults (allBenchmarks, "BM25F")