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


def setBenchmarksQueriesBM25F(): 

    '''
        definition query list and related search filters
        
        Returns:
            allQuery: list with loaded queries
    '''
    
    allQuery = []

    # parameters = UIMode searchField                                   priceInterval    wineType     sentimentRequest    algorithm,  thesaurusFlag   andFlag     correctionFlag  year
    # parameters = [False, ["wine_name", "review_note", "wine_winery"], [(None), (20)], ["1", "2"],   (["M", "joy"]),     False,      False,          False,       False,           None]

    nlQuery = "n1: 'Vino Valpolicella [simple retriving]'"
    queryText = "Valpolicella"
    parameters = [False, ["wine_name"], None, ["1"], (None), False, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])
    
    nlQuery = "n2: 'Vini cantina Valdo [simple retriving]'"
    queryText = "Valdo"
    parameters = [False, ["wine_winery"], None, None, (None), False, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n3: 'Vino Montepulciano, impressione positiva, Prezzo compreso tra 10 e 20€'"
    queryText = "Montepulciano"
    parameters = [False, ["wine_name"], [(10), (20)], ["1"], (["M", "joy"]), False, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n4: 'Vini bianchi adatti sia per la carne che per il pesce, recensioni positive, Prezzo compreso tra 20 e 30€'"
    queryText = "carne e pesce"
    parameters = [False, ["review_note"], [(20), (30)], ["1", "2"], (["M", "joy"]), False, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n5: 'Vini da abbinare a bistecche' [y/n thesaurus] "
    queryText = "bistecca"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), False, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    queryText = "bistecca"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), False, True, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n6: ' Vini economici ma con recensioni tristi'"
    queryText = "economico"
    parameters = [False, ["review_note"], None, None, (["M", "sadness"]), False, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n7: 'Vini per festeggiare, sotto i 20€' [y/n thesaurus] "
    queryText = "festa"
    parameters = [False, ["review_note"], [(None), (20)], None, (["M", "joy"]), False, False, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    queryText = "festa"
    parameters = [False, ["review_note"], [(None), (20)], None, (["M", "joy"]), False, True, False, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n8: 'Vini di grande personalità del 2012'"
    queryText = "grande personalità"
    parameters = [False, ["review_note"], None, None, (["M", "joy"]), False, False, True, False, 2012]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n9: 'Vini Liquorosi con sentori di miele, recensioni positive'"
    queryText = "miele"
    parameters = [False, ["review_note"], None, ["24"], None, False, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    nlQuery = "n10: 'Lambrusco con gnocco fritto'"
    queryText = "lambrusco e gnocco fritto"
    parameters = [False, ["wine_name", "review_note"], None, None, None, False, False, True, False, None]
    allQuery.append([nlQuery, queryText, parameters])

    # Following lines: example of query natural language
    # queryText = " > wine_name:lambrusc AND review_note:gnocc AND review_note:fritt"
    # parameters = [False, ["wine_name", "review_note"], None, None, None, False, False, True, False, None]
    # allQuery.append([nlQuery, queryText, parameters])

    return allQuery
