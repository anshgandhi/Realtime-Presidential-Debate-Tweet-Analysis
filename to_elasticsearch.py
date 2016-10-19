#Loading the tokenized words in to Elasticsearch and use Kibana to find the most used words.
#Top 10 Unique words in all the tweets

from datetime import datetime
from elasticsearch import Elasticsearch
import json
import re
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import time
import datetime

es = Elasticsearch()

#Tags that correspond to each Candidate
tags_cand1 = {"trumpforpresident":None,"lasttimetrumppaidtaxes":None,"trump4president":None,"trumptaxes":None,"trump":None,"donaldtrump":None,"makeamericagreatagain":None,"trumptales":None}
tags_cand2 = {"hillaryclinton":None,"sheswithus":None,"hillaryforpresident":None,"hillary4president":None,"imwithher":None,"hillary":None,"clinton":None}

tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)

#Adding stopwords to the pre-existing stopwords
stop = set(stopwords.words('english')+["rt",":","!","-","…","?","url",".","’","\n","trump","donald","donaldtrump","hillary","clinton","hillaryclinton","https","said","like"])

i=1

tweet_file = open('tweets.json', 'r')

while True:
    line = ''
    flag_cand1=False;
    flag_cand2=False;
    
    while len(line) == 0 or line[-1] != '\n':
        tail = tweet_file.readline()
        if tail == '':
            time.sleep(2)
            print(str(datetime.datetime.now().time().replace(microsecond=0))+" - Keep the tweets coming...")
            continue
        line += tail
    
    all_data = json.loads(line)
    
    if "text" in all_data:
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
            tweet = [word for word in temp if word.isalpha() and len(word) > 2]
            
            #Structuring the words to be put in Elasticsearch
            temp=''
            for word in tweet:
                temp = word+" "+temp
            json_text = '{"text": "'+temp+'"}'
            
            
            res = es.index(index="debate", doc_type='tweet', id=i, body=json.loads(json_text))
            es.indices.refresh(index="debate")
            i += 1
