# WineTz Repository

Ad oggi, WineTZ offre le seguenti funzionalità:
1. web scraping da *vivino.com* 
2. rappresentazione dei dati scaricati mediante *dataset.json*
3. indicizzazione dei dati con le stime ottenute da librerie di sentiment analysis

WineTz, attualmente elabora recensioni in lingua italiana e in lingua inglese. 

# /crawler

Il crawler serve per scaricare i dati da *vivino.com*. 
Il funzionamento del crawler è definito nel README.md all'interno della directory corrispondente. 
<br>
[il funzionamento è rimasto quello definito all'inizio]

Definiti i parametri di ricerca, il crawler scarica i dati nella cartella *out/dataset* con i corrispondenti riferimenti temporali. 

# /data
La cartella */data* contiene uno script *dataLoad.py* . 
Lo script lavora con due directory: */data/input* e */data/dataset*. 

*indexer.py* lavora con un file, denominato *dataset.json*. 
*dataset.json* ha una struttura specifica (esempio in *jsonStructure.json*)

Il file *dataset.json* viene creato dallo script *dataLoad.py* . 
Per creare *dataset.json*:
- Avviare dataLoad.py 
`python3 dataLoad.py`
- Lo script chiederà la cartella di input dei file *.csv*
`Type path directory of .csv from crawler or other> `
Premendo il pulsante *enter* senza digitare il path, lo script carica automaticamente i file *.csv* dalla cartella */data/input*. 
Per comodità, una volta scaricati i dati dal crawler, copiare il contenuto della directory con i dati all'interno della cartella */data/input*. 
- All'interno di */data/dataset/* verranno creati due file: *dataset.json* e *dataset.csv*. 

Una volta ottenuto il dataset desiderato, è necessario **rinominare** il file *.json*.
*indexer.py* si aspetta un file  `dataset.json`; è necessario rimuovere l'ultima parte del nome del file con il riferimento temporale. 

`dataLoad.py` serve esclusivamente ad ottenere un file ordinato e pulito dalle ridondanze.

# /indexer

*/indexer/indexer.py* crea l'indice partendo dal file *dataset.json*

    python3 /indexer/indexer.py

Lo script accetta un parametro tramite la libreria *argsparse*:

    python3 /indexer/indexer.py -o
   Questo parametro è servito a me per utilizzare indexer.py con dei modelli di *sentiment analysis* offline.

Dopo aver creato l'indice, lo script esegue una query di prova, che serve soltanto a verificare l'effettiva presenza dell'indice. 
