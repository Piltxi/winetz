"""
FEEL-IT: Emotion and Sentiment Classification for the Italian Language

Reference:
@inproceedings{bianchi2021feel,
    title = {{"FEEL-IT: Emotion and Sentiment Classification for the Italian Language"}},
    author = "Bianchi, Federico and Nozza, Debora and Hovy, Dirk",
    booktitle = "Proceedings of the 11th Workshop on Computational Approaches to Subjectivity, Sentiment and Social Media Analysis",
    year = "2021",
    publisher = "Association for Computational Linguistics",
}
"""

"""
Twitter-roBERTa-base for Sentiment Analysis - UPDATED (2022)
@inproceedings{loureiro-etal-2022-timelms,
    title = "{T}ime{LM}s: Diachronic Language Models from {T}witter",
    author = "Loureiro, Daniel  and
      Barbieri, Francesco  and
      Neves, Leonardo  and
      Espinosa Anke, Luis  and
      Camacho-collados, Jose",
    booktitle = "Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics: System Demonstrations",
    month = may,
    year = "2022",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.acl-demo.25",
    doi = "10.18653/v1/2022.acl-demo.25",
    pages = "251--260"
}
"""

from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
from transformers import pipeline

def setSentiment (content, language, classifiers): 

    '''
        setSentiment returns the various scores of the sentiment analysis. 
        the method is implemented separately in order to correctly handle the library output.
    '''
    classifierIT, classifierEN = classifiers

    if language == 'it':
        result = classifierIT (content)

        # print ("result: ", result)

        return result [0]['label']

    if language == 'en':
        result = classifierEN (content)

        # print ("result: ", result)

        return result [0]['label']

    print (f"An error occurred during the sentiment analysis process: language detected: {language}")
    quit()

def initClassifiers (offlineFlag): 

    '''
        initClassifier is used to specify the classifiers to perform sentiment analysis
        - offlineFlag:  useful when loading downloaded modules.
    '''

    if offlineFlag: 

        #* Loading IT classifier
        pathModel = "../models/feel-it-italian-emotion"
        model = AutoModelForSequenceClassification.from_pretrained(pathModel)
        tokenizer = AutoTokenizer.from_pretrained(pathModel, use_fast=False)
        classifierIT = TextClassificationPipeline(model=model, tokenizer=tokenizer, task="text-classification")

        '''#* Loading EN classifier
        pathModel = "../models/twitter-roberta-base-sentiment-latest"
        model = AutoModelForSequenceClassification.from_pretrained(pathModel)
        tokenizer = AutoTokenizer.from_pretrained(pathModel, use_fast=False)
        classifierEN = TextClassificationPipeline(model=model, tokenizer=tokenizer, task="text-classification")'''

        print ("Models loaded locally.")

    else: 
        
        #* Loading IT classifier
        classifierIT = pipeline ("text-classification", model = 'MilaNLProc/feel-it-italian-emotion', top_k=2)
    
        #* Loading EN classifier
        # classifierEN = pipeline ("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest")

        print("Models downloaded from internet.")

    # return [classifierIT, classifierEN]
    return [classifierIT, classifierIT]