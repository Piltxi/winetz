<h1 align="center">WineTz</h1>

<div align="center">

[![Work in Progress](https://img.shields.io/badge/status-work_in_progress-yellow.svg)](https://shields.io/)

</div>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## 🍇 About <a name = "about"></a> 

WineTz is a powerful tool that leverages sentiment analysis techniques to provide insights into the emotional tone of wine reviews. 
<br><br>
Whether you're a wine enthusiast, a sommelier, or a data-driven marketer, our engine helps you navigate the rich landscape of wine opinions.

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

### Installing

## 🥂 Usage <a name="usage"></a>

### 📖 CRAWLER Options
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
You can change WineTz search filters by using the ***src/command.py*** **module.** and ***production()*** **function**. 
```
python3 crawler.py -p
```
### ⚖️ Start crawling
When WineTz starts its tasks, it prints the number of matches obtained through requests to the *vivino.com* API.
Afterwards, you will see a progress bar describing the progress of the review retrieval.

WineTz creates an output folder */out*. Inside */out* create a directory for each exported dataset.
Inside the *dataset directory*, WineTz exports three *.csv* files: wines, style and reviews.

*wine.csv* contains information about wines <br> *style.csv* provides information on wine styles <br> *reviews.csv* the reviews of each wine.


## 🚀 Deployment <a name = "deployment"></a>

## ⛏️ Built Using <a name = "built_using"></a>
- [Python](https://docs.python.org/3/) - Main program
- [Pandas](https://pandas.pydata.org/) - Python Data Analysis library
- [Requests](https://pypi.org/project/requests/) - Python HTTP library


## ✍️ Authors <a name = "authors"></a>


