import pandas as pd
import argparse
import subprocess
import os

def resetDataset():
        
    if os.path.exists("dataset/"):
        try:
            subprocess.run(["rm", "-fr", "dataset"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in removing the existing directory: {e}")

    print ("reset dataset folder")
    quit()


parser = argparse.ArgumentParser(description="WineTz v.1")
parser.add_argument("-r", "--reset", action="store_true", help="reset directory dataset/")
parser.add_argument("-f", "--file", action="store_true", help="specify output /path/")

args = parser.parse_args()

if args.reset: 
    resetDataset()

inputPath = input ("Type path directory of .csv from crawler or other> ")

#* path directory definition
directory_name = "dataset/"

if args.file:
    directory_name = input ("Type path directory of final dataset> ")

if not os.path.exists(directory_name):
    try:
        os.makedirs(directory_name)
    except subprocess.CalledProcessError as e:
        print(f"Error in creating the directory: {e}")

reviews_df = pd.read_csv(f'{inputPath}/reviews.csv')
wine_df = pd.read_csv(f'{inputPath}/wine.csv')
style_df = pd.read_csv(f'{inputPath}/style.csv')

merged_df = pd.merge(reviews_df, wine_df, left_on='idWine', right_on='ID', how='inner')
merged_df = pd.merge(merged_df, style_df, left_on='Style', right_on='ID', how='inner')
selected_columns = ['idRev', 'Language', 'Winery', 'Name', 'Year', 'Region', 'Description', 'Nation', 'User Rating', 'Note', 'CreatedAt', 'Rating', 'Rates count', 'Type', 'Price']
result_df = merged_df[selected_columns]

result_df.to_csv(f'{directory_name}/dataset.csv', index=False, encoding='utf-8')

print("Merge and selection completed successfully. Results exported in 'dataset/dataset.csv'.")