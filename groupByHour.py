'''
Created on Nov 12, 2016

@author: Elliot
'''
import pandas as pd
import matplotlib.pyplot  as plt
def saveHourGraph(fName):
    dfComments = pd.read_csv(fName, parse_dates=['comment_published'],encoding="latin-1")
    print(dfComments.dtypes)
    dfBrief = dfComments[['comment_id', 'comment_published']]
    dfBriefLikes = dfComments[['comment_published', 'comment_likes']]
    dfBrief['comment_published'] = dfBrief['comment_published'].dt.hour
    dfBriefLikes['comment_published'] = dfBriefLikes['comment_published'].dt.hour
    #dfBrief.groupby('comment_published').agg(['count']).plot()
    #dfComments['comment_published'] = dfComments['comment_published'].dt.hour
    #print(dfComments.groupby('comment_published').agg(['count', 'sum']).head())
    #dfComments.groupby('comment_published').agg(['count']).plot()
    #plt.legend().remove()
    dfBriefLikes.groupby('comment_published').agg(['sum']).plot()
    plt.legend().remove()
    plt.title("comments per hour of the day")
    plt.xlabel("comment published per hour of the day")
    plt.ylabel("comments")
    print("saving file")
    plt.savefig('static\commentsByHour.png')
    

