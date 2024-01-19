# WineTz Repository

As of today, WineTz provides the following features:
1. Web Scraping from vivino.com
2. Data Representation with dataset.json
3. Indexing Data with Sentiment Analysis
4. Navigate indexed data via graphical interface
5. Conduct search engine benchmarks and calculate DCG and NDCG to obtain a performance measure

### The contents of the folders in more detail:

1. **Web Scraping from vivino.com**
   - The crawler, located in the `/crawler` directory, is responsible for downloading data from *vivino.com*. The details of its functioning are defined in the README.md file within the corresponding directory.
   - After defining the search parameters, the crawler downloads the data into the `out/dataset` folder with corresponding timestamps.

2. **Data Representation with dataset.json**
   - The `/data` folder contains a script named `dataLoad.py`, which works with two directories: `/data/input` and `/data/dataset`.
   - `indexer.py` operates with a file named `dataset.json`, which has a specific structure (example in `jsonStructure.json`).
   - The `dataset.json` file is created by running the `dataLoad.py` script. To create `dataset.json`:
     - Run dataLoad.py:
       ```bash
       python3 dataLoad.py
       ```
     - The script will ask for the input folder path for the .csv files:
       ```bash
       Type path directory of .csv from crawler or other> 
       ```
       Pressing enter without typing the path loads .csv files automatically from the `/data/input` folder.
       For convenience, copy the contents of the data directory from the crawler into the `/data/input` folder.
     - Two files will be created inside `/data/dataset/`: `dataset.json` and `dataset.csv`.
   - `dataLoad.py` creates a folder at the path `/data/dataset/archive` and creates two copies of the dataset: the first inside the archive, the second inside `/data/dataset/`
   - `dataLoad.py` is used to obtain an organized and clean file without redundancies.

3. **Indexing Data with Sentiment Analysis**
   - The `/indexer/indexer.py` script creates the index starting from the `dataset.json` file:
     ```bash
     python3 /indexer/indexer.py
     ```
   - The script accepts a parameter using the `argsparse` library:
     ```bash
     python3 /indexer/indexer.py -o
     ```
     This parameter was used to employ `indexer.py` with offline sentiment analysis models.

4. **Navigate indexed data via graphical interface**
   - The `/searcher/searcher.py` loads GUI with function to navigate into items indexed collection:
     ```bash
     python3 /searcher/searcher.py
     ```
        `/searcher/searcher.py` it is based on the code implemented in the other two files `/searcher/searcherIO.py` and `/searcher/textTools.py`. <br>
    - Automatically, during the startup phase, the GUI tries to load the index at the `/../index` path.
         `/../index` path where by default indexer.py creates the index of the dataset.<br>
    - Via GUI it is possible to flag a set of parameters and values, including different types of wines, price ranges, search fields, etc.

5. **Conduct search engine benchmarks**
    - The `/benchmark/benchmarks.py` it is useful for proposing different queries, specifying the search parameters, and for specifying a relevance value for each query.
    - The value entered will then be used to obtain DCG and NDCG measurements.
     ```bash
     python3 /benchmark/benchmarks.py
     ```
    - Currently, some queries are already described. To change them, please be careful when entering the parameters.


Note: <br>
Currently, the textual procedures are activated, tested and working exclusively for the Italian language.
In the modules, the code is prepared for easy loading of other templates for other languages.
