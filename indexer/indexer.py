import os
import subprocess
import argparse
import json
from tqdm import tqdm

from whoosh.fields import *
from whoosh.index import create_in
from whoosh.analysis import LanguageAnalyzer

from sentimentAnalyis import setSentiment, initClassifiers

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

    itAnalyzer = LanguageAnalyzer('it', cachesize=-1)
    # enAnlyzer = LanguageAnalyzer ('en', cachesize=-1)

    classifiers = initClassifiers (args.offline)

    schema = Schema(
        wine_type = NUMERIC(int, stored=True),
        wine_name = TEXT(stored=True, analyzer=itAnalyzer),
        wine_winery = TEXT(stored=True, analyzer=itAnalyzer),
        wine_year = NUMERIC(int, stored=True),
        wine_price = NUMERIC(float, stored=True),
        
        review_note = TEXT(stored=True, analyzer=itAnalyzer),
        sentiment = TEXT(stored=True)
    )

    ix = create_in(indexPath, schema)
    
    ix = create_in(indexPath, schema)
    writer = ix.writer(procs=4, limitmb=64, multisegment=True)

    totDocs = sum(len(wine["reviews"]) for wine_type in datas["wine_types"] for style in wine_type["styles"] for wine in style["wines"])
    with tqdm(total=totDocs, desc="Indexing") as pbar:
        for wine_type in datas["wine_types"]:
            for style in wine_type["styles"]:
                    for wine in style["wines"]:
                            for review in wine["reviews"]:
                                
                                sentiment = setSentiment (review["Note"], review["Language"], classifiers)
                                
                                doc = {
                                    
                                    "wine_type": str(wine_type["wine_Type"]),
                                    "wine_name": wine["wine_Name"],
                                    "wine_price": wine["wine_Price"],
                                    "wine_winery": wine["wine_Winery"],
                                    "wine_year": wine["wine_Year"],
                                   
                                    "sentiment": sentiment,
                                    "review_note": review["Note"],
                                }
                                
                                writer.add_document(**doc)
                                pbar.update(1)

    print("Committing final changes...")
    writer.commit()

    