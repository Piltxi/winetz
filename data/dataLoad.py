import pandas as pd
import argparse
import subprocess
import os
import json
from datetime import datetime

"""
wine.csv -> ID, Winery, Name, Year, Style, Rating, Rates count, Type, Price
style.csv -> ID, Region, Description, Nation
reviews.csv -> idRev, Language, idWine, User Rating, Note, CreatedAt

{
    "1" : {
        "47": {
            "Region": "Italia centrale",
            "Description": "Central Italy is a red wine wonderland with an impressive history. Wine cultivation dates all the way back to 8000 BC when Etruscans were settled in the area. It's a land of contrasts. Green hills, craggy coastlines, and mountain peaks all play host to vineyards which produce wines unique to their regions. \n\nCentral Italian reds are often composed of Sangiovese, the most widely planted grape in Italy. Its wines are savory and fruity, with herbal and mineral complexity. It adores sunshine and is sensitive to terroir (the environmental factors that affect the taste of a wine), evolving depending on where it\u2019s planted. \n\nYour Central Italian Red might be made according to a regions' strict rules, or an innovative take on a new technique or blend. It's because this large area is known for both classic flavors and wild experimentation, so have fun exploring both!",
            "Nation": "it",
            "123": {
                "Name": "Petit Verdot",
                "Winery": "Ducato Grazioli",
                "Year": 2021,
                "Rating": 0.0,
                "Rates count": 16,
                "Price": 8.8, 
                "reviews": [{
                    "Language": "it",
                    "Note": "Davvero ottimo questo Petit Verdot, il migliore che abbia mai assaggiato. Pulito ed equilibrato, con note di amarena, visciole e more. ",
                    "CreatedAt": "2016-10-05T20:48:41.000Z"
                  }]
            }
        }
    }
}

1 -> Type
47 -> Style
123 -> ID

merged_df -> idRev,Language,User Rating,Note,CreatedAt,wine_ID,wine_Winery,wine_Name,wine_Year,wine_Rating,wine_Rates count,wine_Type,wine_Price,style_ID,style_Region,style_Description,style_Nation

    STRUTTURA DATAFRAME:
 0   idRev              120 non-null    int64  
 1   Language           120 non-null    object 
 2   User Rating        120 non-null    float64
 3   Note               120 non-null    object 
 4   CreatedAt          120 non-null    object 
 5   wine_ID            120 non-null    int64  
 6   wine_Winery        120 non-null    object 
 7   wine_Name          120 non-null    object 
 8   wine_Year          120 non-null    int64  
 9   wine_Rating        120 non-null    float64
 10  wine_Rates count   120 non-null    int64  
 11  wine_Type          120 non-null    int64  
 12  wine_Price         120 non-null    float64
 13  style_ID           120 non-null    int64  
 14  style_Region       120 non-null    object 
 15  style_Description  90 non-null     object 
 16  style_Nation       120 non-null    object

"""

def valueTypeConverter (input, type):

    if type == "int": 
        try: 
            output = int (input)
        except ValueError: 
            print (f"] reported error: converting \"{input}\" into integer value")
            output = 1

    if type == "float": 
        try: 
            output = float (input)
        except ValueError: 
            print (f"] reported error: converting \"{input}\" into float value")
            output = 1

    return output

def setHierarchy (df):
    
    """
        setHierarchy is used to create the hierarchical data structure to be written to the .json file.
        - df is the pandas dataframe obtained from the csv files created by the web crawler.

        Returns:
            output_json: complex data structure, including dictionaries with all the data:
            typologies, wine styles, wines and reviews.
    """    

    gType = df.groupby('wine_Type')
    lType = []

    for typeName, typeGroup in gType:
        lStyle = []
        gStyle = typeGroup.groupby('style_ID')

        for styleName, styleGroup in gStyle:
            lWines = []

            gWines = styleGroup.groupby('wine_ID')

            for wineName, wineGroup in gWines:
                reviews = []

                for index, row in wineGroup.iterrows():
                    review_data = {
                        "Language": row['Language'],
                        "User_Rating": row['User Rating'],
                        "Note": row['Note'],
                        "CreatedAt": row['CreatedAt']
                    }
                    reviews.append(review_data)

                id = valueTypeConverter(row['wine_ID'], "int")
                year = valueTypeConverter(row['wine_Year'], "int")
                price = valueTypeConverter(row['wine_Price'], "float")

                wine_data = {
                    "wine_ID": id,
                    "wine_Winery": row['wine_Winery'],
                    "wine_Name": row['wine_Name'],
                    "wine_Year": year,
                    "wine_Rating": row['wine_Rating'],
                    "wine_Rates_count": row['wine_Rates count'],
                    "wine_Price": price,
                    "reviews": reviews
                }
                lWines.append(wine_data)

            id = valueTypeConverter(styleName, "int")
            style_data = {
                "style_ID": id,
                "style_Region": wineGroup['style_Region'].iloc[0],
                "style_Description": wineGroup['style_Description'].iloc[0],
                "style_Nation": wineGroup['style_Nation'].iloc[0],
                "wines": lWines
            }
            lStyle.append(style_data)

        id = valueTypeConverter(typeName, "int")
        type_data = {
            "wine_Type": id,
            "styles": lStyle
        }
        lType.append(type_data)

    output_json = {
        "wine_types": lType
    }

    return output_json

def loadStructure (path, directory_name, currentTime):  

    """
        loadStructure implements join functionality between the csv files obtained by the crawler to obtain all the data after the merge.
        - path: path of the csv files downloaded by the web crawler
        - directory_name: output dataset path
        - currentTime: time of the current operation, useful for distinguishing more datasets
    """    

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating the directory: {e}")

    subDirectoryArchive = directory_name + "archive/"
    if not os.path.exists(subDirectoryArchive):
        try:
            os.makedirs(subDirectoryArchive)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating the directory: {e}")

    reviews_df = pd.read_csv(f'{path}/reviews.csv')
    wine_df = pd.read_csv(f'{path}/wine.csv')
    style_df = pd.read_csv(f'{path}/style.csv')

    # filling null fields with empty strings
    reviews_df = reviews_df.fillna('')
    wine_df = wine_df.fillna('')
    style_df = style_df.fillna('')

    wine_df = wine_df.add_prefix('wine_')
    style_df = style_df.add_prefix('style_')

    '''print ("Reviews counter: ", len(reviews_df))
    reviews_df = reviews_df.drop_duplicates(subset=['Note', 'idWine'])
    print ("Reviews counter: ", len(reviews_df))
    reviews_df = reviews_df.drop_duplicates(subset=['Note'])
    print ("Reviews counter: ", len(reviews_df))
    quit()'''

    reviews_df = reviews_df.drop_duplicates(subset=['Note', 'idWine'])
    
    reviews_df = reviews_df[reviews_df['Language'] != 'en']

    merged_df = pd.merge(reviews_df, wine_df, left_on='idWine', right_on='wine_ID', how='inner')
    merged_df = pd.merge(merged_df, style_df, left_on='wine_Style', right_on='style_ID', how='inner')
    merged_df.drop(['idWine', 'wine_Style'], axis=1, inplace=True)

    dfJSON = setHierarchy (merged_df)
    
    #* JSON export [archive]
    nameFile = f'dataset {currentTime}.json'
    outPath = subDirectoryArchive + nameFile
    with open(outPath, 'w', encoding='utf-8') as json_file:
        json.dump(dfJSON, json_file, indent=2, ensure_ascii=False)
    print(f"Results [JSON] exported in {outPath}'.")

    #* JSON export [production]
    nameFile = f'dataset.json'
    outPath = directory_name + nameFile
    with open(outPath, 'w', encoding='utf-8') as json_file:
        json.dump(dfJSON, json_file, indent=2, ensure_ascii=False)
    print(f"Results [JSON] exported in {outPath}.")

    #* CSV export
    ''' the following lines are useful for debugging.
        in production you can comment. 
        They are used to generate a standard csv file with the data after performing the merge.  
    '''
    nameFile = f'dataset {currentTime}.csv'
    outPath = subDirectoryArchive + nameFile
    merged_df.to_csv(outPath, index = False)
    print(f"Results [CSV] exported in {outPath}.")

def resetDataset():

    '''
        resetDataset is used to delete the output folder; this is useful for cleaning up the repo directory
    '''

    if os.path.exists("dataset/"):
        try:
            subprocess.run(["rm", "-fr", "dataset"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in removing the existing directory: {e}")

    print("Reset dataset folder successfully.")
    quit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="WineTz v.1")
    parser.add_argument("-r", "--reset", action="store_true", help="reset directory dataset/")
    parser.add_argument("-f", "--file", action="store_true", help="specify output /path/")
    args = parser.parse_args()

    if args.reset:
        resetDataset()

    currentTime = datetime.now().strftime("%H.%M")
    
    inputPath = input("Type path directory of .csv from crawler or other> ")
    inputPath = inputPath if inputPath else "input/"

    directory_name = "dataset/"
    if args.file:
        directory_name = input("Type path directory of the final dataset> ")

    dataframe = loadStructure(inputPath, directory_name, currentTime)