<h1 align="center">WineTz Crawler</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
</div>


<p align="center"> 
Simple web crawling tool to retrieve reviews from <i>vivino.com</i> website. <br><br>
WineTz allows you to specify some parameters to filter the search on the <i>vivino.com</i> environment, retrieves the reviews, and produces the export in <i>.csv dataset.</i>
</p>

## 🍷 Table of Contents

- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)

## 🥣 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Check in **requirements.txt** for prerequisites and any libraries to install. 

```
pip3 install <module>
```

### Installing

Download Repository from GitHub and enter in **src** folder

```
git clone
```

```
cd src
```

## 🥂 Usage <a name="usage"></a>
### 📖 Options
WineTz shows all available features.
```
python3 crawler.py -h
```
WineTz deletes output information and recovered reviews. The */out* directory will be deleted. 
```
python3 crawler.py -r
```
WineTz allows you to specify filtering options for your search. 
```
python3 crawler.py -s
```
WineTz prints additional information while running. **This option is useful and recommended during debugging.**
```
python3 crawler.py -v
```
WineTz acquires filtering parameters in a special way.
**This option must be specialized towards the target of interest.**
```
python3 crawler.py -d
```
### ⚖️ Start crawling
When WineTz starts its tasks, it prints the number of matches obtained through requests to the *vivino.com* API.
Afterwards, you will see a progress bar describing the progress of the review retrieval.

Happy scraping!

## ⛏️ Built Using <a name = "built_using"></a>

- [Python](https://docs.python.org/3/) - Main program
- [Pandas](https://pandas.pydata.org/) - Python Data Analysis library
- [Requests](https://pypi.org/project/requests/) - Python HTTP library

## 👨🏻‍🔬 Authors <a name = "authors"></a>

- [@piltxi](https://github.com/Piltxi/) *excellent singer after some wine* and amateur developer