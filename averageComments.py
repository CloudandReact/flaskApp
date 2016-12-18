'''
Analyze find all users see how many comments each one made
Created on Oct 30, 2016

@author: Elliot
'''
import pandas as pd
import collections
import sys
import matplotlib.pyplot  as plt

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
def getTopLikes(topLikes):
    for i in topLikes:
        pass
        
def getAverageLikes(fComments,fPosts):   
    dfComments = pd.read_csv(fComments,encoding="latin-1")
    #print(dfComments['comment_published'])
    print("df comments length", len(dfComments.index))
    dfStatus = pd.read_csv(fPosts,encoding="UTF-8")
    print(dfStatus['status_published'])
    print("df status length", len(dfStatus.index))
    dfMerged = pd.merge(dfComments, dfStatus, on='status_id')
    print("df merged count", len(dfMerged.index))
    users = set(dfMerged['comment_author'])  # get the list of users 
    dictUserComments = {}
    print("printing merged columns ")
    print(dfMerged.columns)
    for i in users:
        dictUserComments[i] = 0
    
    # iterate over headers apparently
    # for df in dfMerged:
        # print(df)
        # name = df[5] #authro
        # print(name)
        # dictUserComments[name]= dictUserComments[name]+1
    for index, df in dfMerged.iterrows():
        try:
            name = df['comment_author']
            dictUserComments[name] = dictUserComments[name] + 1
        except:
            pass
    dfMostCommon = collections.Counter(dictUserComments)
    top20 = dfMostCommon.most_common(500)
    uprint(top20)
    print(max(dictUserComments.values()))
    maxKey =top20[0][0] #to get top 1
    print("df merged head see if both rows are there")
    uprint(dfMerged.head(5))
    dfTop= dfMerged[dfMerged['comment_author']==maxKey]
    uprint(dfMerged[dfMerged['comment_author']==maxKey])
    
    listAverage=[]
    for i in top20:
        k = i[0]
        dfTopI = dfMerged[ dfMerged['comment_author']==k]
        meanLikes = dfTopI['comment_likes'].mean()
        listAverage.append(meanLikes)
    #rangeComments = df.index.tolist()..
    rangeComments = range(0,len(listAverage))
    plt.scatter(rangeComments,listAverage,s=2,color="green")
    plt.xlabel("top commententators from most to least comments")
    plt.ylabel("number of likes per comment (average)")
    plt.title("Top commentators  vs average likes per comment\n")
    plt.ylim(ymin=0)
    plt.xlim((0,500))
    plt.savefig("static\\aComments.png")
   
    
