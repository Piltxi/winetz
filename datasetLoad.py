import csv
import argparse
import subprocess
import os

def copyCSV (inputFile, outputFile):
    
    try:
        
        with open(inputFile, 'r', encoding='utf-8') as source_file:
            reader = csv.reader(source_file)
            data = [row for row in reader]

        with open(outputFile, 'w', encoding='utf-8', newline='') as destination_file:
            writer = csv.writer(destination_file)
            writer.writerows(data)
    
    except FileNotFoundError:
        print(f"ERROR] '{inputFile}' -input file not found")
        quit()
    
    except Exception as e:
        print(f"ERROR] '{inputFile}' -during copying {e}")
        quit()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="WineTz v.1")
    parser.add_argument("-r", "--reset", action="store_true", help="reset directory dataset/")

    args = parser.parse_args()

    if (args.reset): 
        
        if os.path.exists("dataset/"):
            try:
                subprocess.run(["rm", "-fr", "dataset"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error in removing the existing directory: {e}")

        print ("reset dataset folder")
        quit()

    #* path directory definition
    directory_name = "dataset/"

    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except subprocess.CalledProcessError as e:
            print(f"Error in creating the directory: {e}")

    inputFile_path = 'crawler/out/out 04.12/dataset 17.56/reviews.csv'
    outputFile_path = 'dataset/reviews.csv'
    copyCSV (inputFile_path, outputFile_path)

    inputFile_path = 'crawler/out/out 04.12/dataset 17.56/wine.csv'
    outputFile_path = 'dataset/wine.csv'
    copyCSV (inputFile_path, outputFile_path)

    inputFile_path = 'crawler/out/out 04.12/dataset 17.56/style.csv'
    outputFile_path = 'dataset/style.csv'
    copyCSV (inputFile_path, outputFile_path)

    print(f"dataset copied successfully")