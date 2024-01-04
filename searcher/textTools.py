from whoosh.analysis import LanguageAnalyzer
from nltk.corpus import wordnet
from langdetect import detect

def searchFromThesaurus (sentence): 

    """
        NOW ONLY SUITABLE FOR ITALIAN LANGUAGE
        extension of a sentence with a list of synonyms, useful for implementing query expansion in the search engine
        
    Returns:
        synonyms: list with synonyms
    """

    words = sentence.split()
    synonyms = []

    for word in words:
        synonyms = [lemma.name() for syn in wordnet.synsets(word, lang='ita') for lemma in syn.lemmas('ita')]
        synonyms.extend(synonyms)

    synonyms = list(set(synonyms))

    return synonyms

def langAnalysis (analyzers, sentence): 

    """
        CODE CURRENTLY NOT USED.
        language identification and analyze the text with whoosh tools
    
    Returns:
        analyzers: list with init analyzers 
        sentence: text to analyze
    """

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
    quit()

def initAnalyzer ():

    """
        CODE CURRENTLY NOT USED.
        
        function designed to initialize 
        lexical analyzers that can be used in the search engine

    Returns:
        list: list with init analyzers 
    """

    itAnalyzer = LanguageAnalyzer('it', cachesize=-1)
    enAnlyzer = LanguageAnalyzer ('en', cachesize=-1)

    return [itAnalyzer, enAnlyzer]

def langDetection (content): 

    """
        CODE CURRENTLY NOT USED.
        language identification
    
    Returns:
        content: string of text
    """

    lang = detect(content)
    print(f"Language detected: {lang}")

    return lang

if __name__ == "__main__":
    raise ImportError("This is not an executable program: run searcher.py")