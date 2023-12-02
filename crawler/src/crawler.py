import argparse
import requests
import json
import pandas as pd
from tqdm import tqdm
import os
import subprocess
from datetime import datetime
import json

import command
from checkCrawler import resetInfo, checkWineTz

def getWine (wine_id, year, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    api_url = f"https://www.vivino.com/api/wines/{wine_id}/reviews?per_page=25&year={year}&page={page}"
    data = requests.get(api_url, headers=headers).json()

    return data

def inputParameters (verbose, specify, development, production): 

    if production: 
        return command.production()

    if development: 
        return command.development()

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

    try: 
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
    
        print ("]Matches obtained: ", matches)
        checkWineTz(3, [matches,wineParameters])

        wineStyleID = set ()
    
        mainwine_dataframe = pd.DataFrame(columns=["ID", "Winery", "Name", "Year", "Style", "Rating", "Rates count", "Type", "Price"]) 
        mainstyle_dataframe = pd.DataFrame(columns=["ID", "Region", "Description", "Nation"]) 

        if verbose: 
            print ("___ START SCRAPING ___")

        if not verbose: 
            iteraBar = matches
            progress_bar = tqdm(total=iteraBar, desc="]drinking", unit="wine", position=0, dynamic_ncols=True)


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

            #!TODO getting alchol gradation

            """"
            #Questo code stampa la struttura del json
            all_wines_data = rew.json()["explore_vintage"]["matches"]
            print (json.dumps(all_wines_data[0], indent=4))
            #for i in range (len(all_wines_data)): 
                #print(json.dumps(all_wines_data[i], indent=4))
            
            quit()
            """
            
            """
            results = [
                (
                    Winery -> t["vintage"]["wine"]["winery"]["name"],
                    Year -> t["vintage"]["year"],
                    ID -> t["vintage"]["wine"]["id"],
                    WINE -> f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
                    RATING -> t["vintage"]["statistics"]["ratings_average"],
                    RATE COUNT -> t["vintage"]["statistics"]["ratings_count"]
                )
                for t in rew.json()["explore_vintage"]["matches"]
            ]
            """

            for t in rew.json()["explore_vintage"]["matches"]: 
                
                styleID = t["vintage"]["wine"]["style"]["id"]

                if styleID not in wineStyleID: 
                    wineStyleID.add(styleID)

                    styleData = [(
                        t["vintage"]["wine"]["style"]["id"],
                        t["vintage"]["wine"]["style"]["regional_name"],
                        t["vintage"]["wine"]["style"]["description"],
                        t["vintage"]["wine"]["style"]["country"]["code"]
                        )
                    ]

                    styleDataframe = pd.DataFrame(
                        styleData,
                        columns=["ID", "Region", "Description", "Nation"]
                    ) 
                    mainstyle_dataframe = pd.concat([mainstyle_dataframe, styleDataframe], ignore_index=True)

                wineData = [ (
                        t["vintage"]["wine"]["id"],
                        t["vintage"]["wine"]["winery"]["name"],
                        t["vintage"]["wine"]["name"],
                        t["vintage"]["year"],
                        t["vintage"]["wine"]["style"]["id"],
                        t["vintage"]["statistics"]["ratings_average"],
                        t["vintage"]["statistics"]["ratings_count"],
                        t["vintage"]["wine"]["type_id"],
                        t["price"]["amount"]
                        # alchol gradation)
                        )
                ]

                wineData = pd.DataFrame(
                    wineData,
                    columns=["ID", "Winery", "Name", "Year", "Style", "Rating", "Rates count", "Type", "Price"],
                )


                if not mainwine_dataframe.empty:
                    mainwine_dataframe = pd.concat([mainwine_dataframe, wineData], ignore_index=True)
                else:
                    mainwine_dataframe = wineData.copy()
        
                if verbose: 
                    print(f"Size of main dataframe after page {i}: {len(mainwine_dataframe)}")

                if not verbose: 
                    progress_bar.update(1)

        if not verbose: 
            progress_bar.close()

        mainwine_dataframe = mainwine_dataframe.drop_duplicates(subset="ID")
        
        if verbose:
            print ("___ END SCRAPING ___")

    except KeyboardInterrupt: 
        
        if not verbose: 
            progress_bar.close()

        timing = datetime.now().strftime("%H.%M")
        message = "recovered" + " " + timing
        exportCSV ("wine", mainwine_dataframe, message)
        exportCSV ("style", mainstyle_dataframe, message)
        checkWineTz(4, message)
    
    return mainwine_dataframe, mainstyle_dataframe
    
def reviewsCrawler (verbose, wineDF, selectedLanguages): 
    
    if verbose: 
        print ("Start reviews crawling...\n")
    
    mainratings_dataframe = pd.DataFrame(columns=["Year", "ID", "User Rating", "Note", "CreatedAt"])

    if not verbose: 
        iteraBar = len (wineDF) #{desc}{percentage:3.0%}{bar} {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]
        progress_bar = tqdm(total=iteraBar, desc="]singing: ", unit="wine", position=0, dynamic_ncols=True, bar_format="{desc}{percentage:3.0f}%|{bar}  {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {postfix}]")
    try: 
        for _, row in wineDF.iterrows():
            page = 1
            while True:
            
                if verbose: 
                    print(f'Getting info about wine {row["ID"]}-{row["Year"]} Page {page}')

                d = getWine(row["ID"], row["Year"], page)

                if not d["reviews"]:
                    progress_bar.set_description(f"]singing") 
                    break

                for r in d["reviews"]:
                    if r["language"] not in selectedLanguages:
                        continue

                    reviewsData = [
                        (
                            row["Year"],
                            row["ID"],
                            r["rating"],
                            r["note"],
                            r["created_at"],
                        )
                    ]
                    
                    reviewsData = pd.DataFrame(
                        reviewsData, 
                        columns=["Year", "ID", "User Rating", "Note", "CreatedAt"]
                    )

                    if not mainratings_dataframe.empty:
                        mainratings_dataframe = pd.concat([mainratings_dataframe, reviewsData], ignore_index=True)
                    else:
                        mainratings_dataframe = reviewsData.copy()
                page += 1
            
            if not verbose: 
                progress_bar.update(1)
                progress_bar.set_postfix(rev = len(mainratings_dataframe), refresh=True)

        if not verbose: 
            progress_bar.close()
    
    except KeyboardInterrupt:

        if not verbose: 
            progress_bar.close()
        
        timing = datetime.now().strftime("%H.%M")
        message = "recovered" + " " + timing
        exportCSV ("reviews", mainratings_dataframe, message)
        checkWineTz(4, message)

    return mainratings_dataframe

def exportCSV (data, dataframe, message): 

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

    directory_name = f"../out/out {currentData}/dataset {message}"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating second directory: {e}")

    name = f"../out/{directory_name}/{data}.csv"

    dataframe.to_csv (name, index=False)

def main (verbose, reset, specify, development, production): 

    if reset: 
        resetInfo()
    
    currentTime = datetime.now().strftime("%H.%M")
    
    (wineParameters, selectedLanguages) = inputParameters (verbose, specify, development, production)

    wineDF, styleDF = wineCrawler (verbose, wineParameters)

    checkWineTz(2, ["wine", wineDF])
    exportCSV ("wine", wineDF, currentTime)
    
    checkWineTz(2, ["style", styleDF])
    exportCSV ("style", styleDF, currentTime)

    reviewsDF = reviewsCrawler (verbose, wineDF, selectedLanguages)
    checkWineTz(2, ["reviews", reviewsDF])

    exportCSV ("reviews", reviewsDF, currentTime)

    print ("]datasets exported successfully")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="WineTz v.1")
    parser.add_argument("-d", "--development", action="store_true", help="debug function for developer")
    parser.add_argument("-s", "--specify", action="store_true", help="specify filter for wine search")
    parser.add_argument("-p", "--production", action="store_true", help="production")
    parser.add_argument("-v", "--verbose", action="store_true", help="additional prints")
    parser.add_argument("-r", "--reset", action="store_true", help="reset directory out/")

    args = parser.parse_args()

    if not (args.development or args.specify or args.production or args.reset):
        parser.print_help()
        checkWineTz(0, "options")

    main(args.verbose, args.reset, args.specify, args.development, args.production)