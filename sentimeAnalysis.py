'''
Created on Nov 13, 2016

@author: Elliot
'''
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
def parseFile(fName,levelSentiment):
    dfComments = pd.read_csv(fName,encoding="latin-1")  # ParseDatesTests
    commentPolarity = []
    commentSubjectivity = []
    commentPos = []
    commentNeg = []
    tb = Blobber(analyzer=NaiveBayesAnalyzer())
    tp = Blobber()
    
    for index, df in dfComments.iterrows():
        comment = df['comment_message']
        txtP = tp(comment)
        txtB = tb(comment)
        commentPolarity.append(txtP.sentiment.polarity)
        commentSubjectivity.append(txtP.sentiment.subjectivity)
        #print(txtP.sentiment)
        commentPos.append(txtB.sentiment.p_pos)
        commentNeg.append(txtB.sentiment.p_neg)
        #print(txtB.sentiment)
    dfComments['comment_polarity'] = commentPolarity
    dfComments['comment_subjectivity'] = commentSubjectivity
    dfComments['comment_pos'] = commentPos
    dfComments['comment_neg'] = commentNeg
    print("finished analyzing all comments now filtering and saving comments based on level of sentiment")
    #dfPros = dfComments[dfComments['comment_polarity'] > 0.8]
    #dfPros = dfPros[dfPros['comment_pos'] >0.65]
    #(dfComments['comment_subjectivity'] > 0.6)
    #dfPros.to_csv("pros2.csv", index=False)
    #dfCons = dfComments [dfComments['comment_polarity'] < -0.8]
    #   (dfComments['comment_subjectivity'] < -0.6)
    #dfCons = dfCons[ dfCons['comment_neg'] <0.35]
    #dfCons.to_csv("cons2.csv", index=False)
    if levelSentiment== "Somewhat Negative":
        dfCons = dfComments[dfComments['comment_polarity'] <-0.45]
        dfCons = dfCons[dfCons['comment_pos'] <0.37]
        uprint(dfCons.to_string())
        dfCons.to_csv("somewhatCons.csv",index=False,encoding="latin-1")
        print("writing somewhat negative file")
    elif levelSentiment == "Very Negative":
        dfCons = dfComments[dfComments['comment_polarity'] <-0.7]
        dfCons = dfCons[dfCons['comment_pos'] <0.25]
        uprint(dfCons.to_string())
        dfCons.to_csv("veryCons.csv", index=False,encoding="latin-1")
        print("writing to very negative file")        
    elif levelSentiment== "Somewhat Positive":
        dfPros= dfComments[dfComments['comment_polarity']>0.45]
        dfPros= dfPros[dfPros['comment_pos']>0.63]
        uprint(dfPros.to_string())
        dfPros.to_csv("somewhatPros.csv",index=False,encoding="latin-1")
    elif levelSentiment=="Very Positive":
        dfPros= dfComments[dfComments['comment_polarity']>0.7]
        dfPros= dfPros[dfPros['comment_pos']>0.75]
        uprint(dfPros.to_string())
        dfPros.to_csv("veryPros.csv",index=False,encoding="latin-1")
    else:
        print("wrong positivity type not writing to a file please enter one of the 4 from the form")
        
        
