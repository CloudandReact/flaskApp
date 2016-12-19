'''
Created on Nov 20, 2016

@author: Elliot
'''
import pandas as pd
import matplotlib.pyplot as plt
import sys

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
def makeTopCommentsGraph(fName):   
    plt.figure()     
    dfStatus = pd.read_csv(fName,parse_dates=['comment_published'])
    print(dfStatus.describe())
    print("head")
    uprint(dfStatus.head())
    dfJustComments = dfStatus.groupby('comment_author')['comment_likes'].agg(['count']) 
    dfJustComments = dfJustComments['count'].sort_values(ascending=False).to_frame()   
    print(type(dfJustComments))                                                   
    uprint(dfJustComments.head(200))
    dfJustComments = dfJustComments.head(100)
    #dfJustComments.head(5).plot(kind='bar')
    gRange = list(range(0, len(dfJustComments.index)))
    print(gRange)
    print("printing comment count")
    uprint(dfJustComments.index)
    print(type(dfJustComments))
    plt.scatter(gRange,dfJustComments['count'],color='red')
    plt.title("Users who comment the most and their number of comments\n")
    plt.xlabel("top users")
    plt.ylabel("number of comments")
    plt.ylim(ymin=0)
    plt.xlim((0,100))
    
    #plt.xticks( dfJustComments['comment_author'].iloc[0:4], rotation='vertical')
    print("right before save file")
    plt.savefig('static\\topCommentators.png')
    print("did we save file")

    
