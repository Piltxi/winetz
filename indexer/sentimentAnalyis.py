from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
from transformers import pipeline

def setSentiment (content, language, classifierIT, classifierEN): 

    '''
        setSentiment returns the various scores of the sentiment analysis. 
        the method is implemented separately in order to correctly handle the library output.
    '''

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

def initClassifier (offlineFlag): 

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

        ''' #* Loading EN classifier
        pathModel = "../models/twitter-roberta-base-sentiment-latest"
        model = AutoModelForSequenceClassification.from_pretrained(pathModel)
        tokenizer = AutoTokenizer.from_pretrained(pathModel, use_fast=False)
        classifierEN = TextClassificationPipeline(model=model, tokenizer=tokenizer, task="text-classification")'''

        print ("Models loaded locally.")

    else: 
        
        #* Loading IT classifier
        classifierIT = pipeline ("text-classification", model = 'MilaNLProc/feel-it-italian-emotion', top_k=2)
    
        #* Loading EN classifier
        classifierEN = pipeline ("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest")

        print("Models downloaded from internet.")

    return classifierIT, classifierIT