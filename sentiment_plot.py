#Analyse the Sentiment of the tweet and Plot it Real-time
import datetime
import time
import json
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import pyqtgraph as pg
import numpy as np
import re

name_cand1 = "Donald"
name_cand2 = "Hillary"

#Tags that correspond to each Candidate
tags_cand1 = {"trumpforpresident":None,"lasttimetrumppaidtaxes":None,"trump4president":None,"trumptaxes":None,"trump":None,"donaldtrump":None,"makeamericagreatagain":None,"trumptales":None}
tags_cand2 = {"hillaryclinton":None,"sheswithus":None,"hillaryforpresident":None,"hillary4president":None,"imwithher":None,"hillary":None,"clinton":None}


tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

#Adding stopwords to the pre-existing stopwords
stop = set(stopwords.words('english')+["rt",":","!","-","…","?","url",".","’","\n"])
        
tweetNum_cand1=0
tweetNum_cand2=0

ptweet_cand1=[]
ntweet_cand1=[]
ptweet_cand2=[]
ntweet_cand2=[]

#Load Positive Words
p = {}
with open("positive_words.txt") as f:
    for line in f:
       (key, val) = (line.strip(),1)
       p[key] = val

#Load Negative Words
n = {}
with open("negative_words.txt") as f:
    for line in f:
       (key, val) = (line.strip(),1)
       n[key] = val

# Plot Settings
pg.setConfigOption('background', 'w')
win = pg.GraphicsWindow()
win.setGeometry(5,0,1270,700) 
win.setAntialiasing(True)

plot_cand1 = win.addPlot()

plot_cand1.setDownsampling(mode='peak')
plot_cand1.setYRange(0, 1, padding=0)
plot_cand1.setTitle("<h3><font color='black'>"+name_cand1+"</font></h3>")
plot_cand1.showGrid(x=True,y=True,alpha=0.9)
plot_cand1.setClipToView(True)
plot_cand1_p = plot_cand1.plot(pen=pg.mkPen('g'),antialias=True)
plot_cand1_n = plot_cand1.plot(pen=pg.mkPen('r')) 

win.nextRow()

plot_cand2 = win.addPlot()

plot_cand2.setDownsampling(mode='peak')
plot_cand2.setYRange(0, 1, padding=0)
plot_cand2.setTitle("<h3><font color='black'>"+name_cand2+"</font></h3>")
plot_cand2.showGrid(x=True,y=True,alpha=0.9)
plot_cand2.setClipToView(True)
plot_cand2_p = plot_cand2.plot(pen=pg.mkPen('g'))
plot_cand2_n = plot_cand2.plot(pen=pg.mkPen('r')) 

#Load the tweets file
tweet_file = open('tweets.json', 'r')

while True:
    line = ''
    flag_cand1=False;
    flag_cand2=False;
    flag_trumptales=False;
    
    while len(line) == 0 or line[-1] != '\n':
        tail = tweet_file.readline()
        if tail == '':
            time.sleep(2)
            print(str(datetime.datetime.now().time().replace(microsecond=0))+" - Keep the tweets coming...")
            continue
        line += tail
    
    all_data = json.loads(line)
    
    if "text" in all_data:
        
        pscore = 0
        nscore = 0
        
        tweet = all_data["text"].lower()
        
        #Finding the candidate the tweet is about
        if len([word for word in re.findall(r"[\w']+",tweet) if word in tags_cand1]) > 0:
            flag_cand1 = True
        if len([word for word in re.findall(r"[\w']+",tweet) if word in tags_cand2]) > 0:
            flag_cand2 = True
        
        #Considering tweets that are specific to a single candidate, i.e. if it has both Candidates' name (flag_cand1 is True & flag_cand2 is True), they are discarded
        if (flag_cand1 != flag_cand2):
            #cleaning the tweets
            temp = tknzr.tokenize(tweet)
            tweet = [word for word in temp if word not in stop]
            temp = tweet
            tweet = [word for word in temp if word.isalpha() and len(word) > 0]
            
            #Iterating over words to see if they occur in Positive or Negative lexicon
            for word in tweet:
                if(word in p.keys()):
                    pscore = pscore +1
                if(word in n.keys()):
                    nscore = nscore +1
            
            #Sentiment score = Positive Words - Negative Words
            score = pscore - nscore

            #Considering Positive & Negative Tweets only.
            #Count Tweets for Candidate 1
            if(flag_cand1 == True and score != 0):
                if (score > 0):
                    pscore_cand1 = pscore_cand1 + 1
                if (score < 0):
                    nscore_cand1 = nscore_cand1 + 1
                if (score != 0):
                    tweetNum_cand1 = tweetNum_cand1 + 1
                    ptweet_cand1 = ptweet_cand1 + [pscore_cand1/tweetNum_cand1]
                    ntweet_cand1 = ntweet_cand1 + [nscore_cand1/tweetNum_cand1]
                    plot_cand1_p.setData(np.array(ptweet_cand1))
                    plot_cand1_n.setData(np.array(ntweet_cand1))

            #Count Tweets for Candidate 2
            if(flag_cand2 == True and score != 0):
                if (score > 0):
                    pscore_cand2 = pscore_cand2 + 1
                if (score < 0):
                    nscore_cand2 = nscore_cand2 + 1
                if (score != 0):
                    tweetNum_cand2 = tweetNum_cand2 + 1
                    ptweet_cand2 = ptweet_cand2 + [pscore_cand2/tweetNum_cand2]
                    ntweet_cand2 = ntweet_cand2 + [nscore_cand2/tweetNum_cand2]
                    plot_cand2_p.setData(np.array(ptweet_cand2))
                    plot_cand2_n.setData(np.array(ntweet_cand2))
            
            #Process the plot points, and plot
            pg.QtGui.QApplication.processEvents()