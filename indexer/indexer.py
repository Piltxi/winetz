import os
import subprocess
import argparse
import json

from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import MultifieldParser
from whoosh.qparser import QueryParser

from sentimentAnalyis import setSentiment, initClassifier

def resetIndex():

    '''
        resetIndex is used to delete the output folder; this is useful for cleaning up the repo directory
    '''

    if os.path.exists("../index"):
        try:
            subprocess.run(["rm", "-fr", "../index"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in removing the existing directory: {e}")

    print("Reset index folder successfully.")
    quit()

def loadJSON (inputPath):
    
    '''
        loadJSON is used to load data from the dataset.json file.
        It was initially a method of the class.
        The specific function would not be necessary, but it is found here for possible debugging operations.
        - inputPath: path of inputh dataset.json
    '''

    with open(inputPath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="WineTz - Indexer v.1")
    parser.add_argument("-r", "--reset", action="store_true", help="reset directory dataset/")
    parser.add_argument("-o", "--offline", action="store_true", help="load offline models")
    args = parser.parse_args()

    if args.reset:
        resetIndex()

    inputPath = "../data/dataset/dataset.json"
    indexPath = "../index"

    if not os.path.exists(indexPath):
            try:
                os.makedirs(indexPath)
            except subprocess.CalledProcessError as e:
                print(f"Error in creating the directory: {e}")

    datas = loadJSON (inputPath)

    '''
        args.offline parameter is useful for performing sentiment analysis with pre-downloaded models.
        This works if the models have been downloaded to the /models directory and match those specified in the sentimentAnalysis.py module. 
        
        initClassifier initializes the methods to perform sentiment analysis.
        sentiment analysis is implemented in English and Italian.

        sentiment analysis is implemented on a separate 
        module so you can change the specific implementation without changing the indexer
    '''

    classifierIT, classifierEN = initClassifier (args.offline)

    schema = Schema(
        wine_type=TEXT(stored=True),
        style_description=TEXT(stored=True),
        wine_name=TEXT(stored=True),
        user_rating=NUMERIC(float, stored=True),
        review_note=TEXT(stored=True),
        created_at=TEXT(stored=True),
        wine_winery=TEXT(stored=True),
        wine_year=NUMERIC(int, stored=True),
        wine_rating_count=NUMERIC(int, stored=True),
        sentiment=TEXT(stored=True)
    )

    ix = create_in(indexPath, schema)
    writer = ix.writer()

    for wine_type in datas["wine_types"]:
        for style in wine_type["styles"]:
            for wine in style["wines"]:
                for review in wine["reviews"]:
                    
                    sentiment = setSentiment (review["Note"], review["Language"], classifierIT, classifierEN)
                    
                    doc = {
                        "wine_type": str(wine_type["wine_Type"]),
                        "style_description": style["style_Description"],
                        "wine_name": wine["wine_Name"],
                        "user_rating": float(review["User_Rating"]),
                        "review_note": review["Note"],
                        "created_at": review["CreatedAt"],
                        "wine_winery": wine["wine_Winery"],
                        "wine_year": wine["wine_Year"],
                        "wine_rating_count": wine["wine_Rates_count"],
                        "sentiment": sentiment
                    }
                    
                    writer.add_document(**doc)
    
    writer.commit()

    '''
        The following lines represent an example of how to formulate a query to the search engine. 
        In this way, the query is formulated on multiple fields (MultifieldParser).
        This represents example and debug code only.
    '''

    searcher = ix.searcher()
    
    search_field = ["wine_name", "style_description", "review_note", "wine_winery"]
    query_parser = MultifieldParser(search_field, ix.schema)

    query_string = "rosso intenso"
    query = query_parser.parse(query_string)
    results = searcher.search(query)

    print("Search results:")
    for i, result in enumerate(results):
        print(i, "] ",result["wine_name"], "\n\n",result["review_note"], "\n\n", f"sentiment: {result['sentiment']}")

    searcher.close()
