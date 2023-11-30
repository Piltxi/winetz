import argparse
import requests
import json
import pandas as pd
from tqdm import tqdm
import os
import subprocess
from datetime import datetime
import json

from checkCrawler import resetInfo, checkWineTz

def getWine (wine_id, year, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = f"https://www.vivino.com/api/wines/{wine_id}/reviews?per_page=25&year={year}&page={page}"
    data = requests.get(api_url, headers=headers).json()

    return data

def inputParameters (verbose, specify, development): 

    if development: 
        params = {

        "wine_type_ids[]": "1",
        "country_codes[]":"it",

        "min_rating" : "4.2",
        "price_range_max": "9",
        } 

        languageList = ["it"]

        return params, languageList

    info_requested = ['countries', 'minimum rating', 'maximum price', 'minimum price', 'type']
    wine_info = {}
    languageList = []

    if specify: 
        print ("Enter the following parameters (press Enter to skip):")
        for item in info_requested:
            
            user_input = input(f"Type wine {item}> ").strip()
            wine_info[item] = user_input

        selectedLanguages = input(f"Type the language codes for retrieving reviews> ").strip()
        languageList = selectedLanguages.split()

    #!To do: verify language code

    params = {

        "wine_type_ids[]": wine_info.get('type', '').split() if wine_info.get('type') else "1",
        "country_codes[]": wine_info.get('countries', '').split() if wine_info.get('countries') else "it",

        "min_rating" :  wine_info.get('minimum ratinge') or "1",
        "price_range_min": wine_info.get('minimum price') or "10",
        "price_range_max": wine_info.get('maximum price') or "250",
    }

    checkWineTz (1, [params["price_range_min"], params["price_range_max"]])

    if languageList is None: 
        languageList.append ("en")
        languageList.append ("it")


    if verbose: 
        for key, value in params.items():
            print(f"{key}: {value}")
        print ("Selected Languages: ")
        for item in languageList: 
            print (f"{item} ", end='')
        print ("\n")

    return (params, languageList)
    
def wineCrawler (verbose, wineParameters): 
    
    if verbose: 
        print ("Wine parameters loaded for scraping process:")
        for key, value in wineParameters.items():
            print(f"{key}: {value}")

    # First request (reading number of matches obtained)
    req = requests.get(
            "https://www.vivino.com/api/explore/explore",
            params = wineParameters, 
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
            },
    )

    matches = req.json()['explore_vintage']['records_matched']
    if verbose: 
        print ("Matches obtained: ", matches)

    main_dataframe = pd.DataFrame(columns=["Winery", "Year", "Wine ID", "Wine", "Rating", "Rates count"]) 

    print ("___ START SCRAPING ___")

    for i in range(1, max(1, int(matches / 25)) + 1):
        wineParameters ['page'] = i

        if verbose: 
            print (f"Scraping from {i}")

        rew = requests.get (
            "https://www.vivino.com/api/explore/explore",
            params = wineParameters, 
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
            },
        )

        print (rew.url)

        #!TODO è necessario convertire il tipo di link per ottenere l'informazione sulla gradazione alcolica
        
        """
        html_content = rew.text
        with open("html_content.html", "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
        quit()
        """
        # start_index = html_content.find("window.__PRELOADED_STATE__.vintagePageInformation = ")
        # end_index = html_content.find("};", start_index) + 1
        # json_data = html_content[start_index:end_index]

        # json_data = json_data.replace("//beware of injecting user-generated content into the page here without sanitizing it", "")
        # wine_info = json.loads(json_data)
        # print(wine_info)
        # with open("ciao.json", "w") as json_file:
        #     json.dump(wine_info, json_file, indent=4)

        # quit()

        """"
        Questo code stampa la struttura del json
        all_wines_data = rew.json()["explore_vintage"]["matches"]
        print(json.dumps(all_wines_data[0], indent=4))
        quit()
        """

        results = [
            (
                t["vintage"]["wine"]["winery"]["name"],
                t["vintage"]["year"],
                t["vintage"]["wine"]["id"],
                f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
                t["vintage"]["statistics"]["ratings_average"],
                t["vintage"]["statistics"]["ratings_count"]
            )
            for t in rew.json()["explore_vintage"]["matches"]
        ]

        dataframe = pd.DataFrame(
            results,
            columns=["Winery", "Year", "Wine ID", "Wine", "Rating", "Rates count"],
        )

        main_dataframe = pd.concat([main_dataframe, dataframe], ignore_index=True)
        if verbose: 
            print(f"Size of main dataframe after page {i}: {len(main_dataframe)}")

    main_dataframe = main_dataframe.drop_duplicates(subset="Wine ID")
    
    print ("___ END SCRAPING ___")
    return main_dataframe
    
def reviewsCrawler (verbose, wineDF, selectedLanguages): 
    
    if verbose: 
        print ("Start reviews crawling...\n")


    if not verbose: 
        iteraBar = len (wineDF)
        progress_bar = tqdm(total=iteraBar, desc="reviews", unit="wine", position=0, dynamic_ncols=True)

    ratings = []
    for _, row in wineDF.iterrows():
        page = 1
        while True:
           
            if verbose: 
                print(f'Getting info about wine {row["Wine ID"]}-{row["Year"]} Page {page}')

            d = getWine(row["Wine ID"], row["Year"], page)

            if not d["reviews"]:
                break

            for r in d["reviews"]:
                if r["language"] not in selectedLanguages:
                    continue

                ratings.append(
                    [
                        row["Year"],
                        row["Wine ID"],
                        r["rating"],
                        r["note"],
                        r["created_at"],
                    ]
                )
            page += 1
        
        if not verbose: 
            progress_bar.update(1)

    if not verbose: 
        progress_bar.close()

    ratings = pd.DataFrame(
        ratings, columns=["Year", "Wine ID", "User Rating", "Note", "CreatedAt"]
    )

    df_out = ratings.merge(wineDF)

    return df_out

def exportCSV (data, dataframe): 
    
    #* path directory definition
    directory_name = "../out"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating the directory: {e}")

    currentData = datetime.now().strftime("%d.%m")
    directory_name = f"../out/out {currentData}"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating second directory: {e}")

    currentTime = datetime.now().strftime("%H.%M.%S")
    name = f"../out/{directory_name}/out {data} {currentTime}.csv"

    dataframe.to_csv (name, index=False)

def main (verbose, reset, specify, development): 

    if reset: 
        resetInfo()
    
    (wineParameters, selectedLanguages) = inputParameters(verbose, specify, development)

    wineDF = wineCrawler (verbose, wineParameters)
    
    checkWineTz(2, ["wine", wineDF])
    exportCSV ("wine", wineDF)

    reviewsDF = reviewsCrawler (verbose, wineDF, selectedLanguages)
    checkWineTz(2, ["reviews", reviewsDF])

    exportCSV ("reviews", reviewsDF)

    print ("Dataset exported.")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="WineTz v.1")
    parser.add_argument("-d", "--development", action="store_true", help="debug function for developer")
    parser.add_argument("-s", "--specify", action="store_true", help="specify filter for wine search")
    parser.add_argument("-p", "--production", action="store_true", help="production")
    parser.add_argument("-v", "--verbose", action="store_true", help="additional prints")
    parser.add_argument("-r", "--reset", action="store_true", help="reset directory out/")

    args = parser.parse_args()

    main(args.verbose, args.reset, args.specify, args.development)

    #!TO DO: production option