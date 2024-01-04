from whoosh.analysis import LanguageAnalyzer
from nltk.corpus import wordnet
from langdetect import detect

def searchFromThesaurus (sentence): 
    words = sentence.split()
    synonyms = []

    for word in words:
        synonyms = [lemma.name() for syn in wordnet.synsets(word, lang='ita') for lemma in syn.lemmas('ita')]
        synonyms.extend(synonyms)

    synonyms = list(set(synonyms))

    return synonyms

'''def langAnalysis (analyzers, sentence): 

    lanC = langDetection (sentence)
    itAnalyzer, enAnalyzer = analyzers

    match lanC:
        case 'it': 
            tokens = [token.text for token in itAnalyzer(sentence)]
            return tokens
        case 'en': 
            tokens = [token.text for token in enAnalyzer(sentence)]
            return tokens

    print (f"] ERRROR unknow language for {sentence}")
    quit()'''

def langAnalysis (analyzers, sentence): 

    itAnalyzer, enAnalyzer = analyzers

    tokens = [token.text for token in itAnalyzer(sentence)]
    return tokens

def initAnalyzer ():
    
    itAnalyzer = LanguageAnalyzer('it', cachesize=-1)
    enAnlyzer = LanguageAnalyzer ('en', cachesize=-1)

    return [itAnalyzer, enAnlyzer]

def langDetection (content): 

    lang = detect(content)
    print(f"Language detected: {lang}")

    return lang

if __name__ == "__main__":
    raise ImportError("This is not an executable program: run searcher.py")