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
    if os.path.exists("../index"):
        try:
            subprocess.run(["rm", "-fr", "../index"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in removing the existing directory: {e}")

    print("Reset index folder")
    quit()

def loadJSON (inputPath):
    
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

    searcher = ix.searcher()
    
    search_field = ["wine_name", "style_description", "review_note", "wine_winery"]
    query_parser = MultifieldParser(search_field, ix.schema)

    query_string = "rosso intenso"
    query = query_parser.parse(query_string)
    results = searcher.search(query)

    print("Risultati della ricerca:")
    for i, result in enumerate(results):
        print(i, "] ",result["wine_name"], "\n\n",result["review_note"], "\n\n", f"sentiment: {result['sentiment']}")

    searcher.close()
