

from ctypes.wintypes import _LARGE_INTEGER
from operator import truediv
#from keys_twitter import consumer_key, consumer_secret, access_token, access_token_secret
import tweepy
#from tweepy import OAuthHandler, Stream, StreamListener
import json
import sys
import time
import regex as re 
import nltk
from nltk import *
import pandas as pd

from predict_and_group import PredictAndGroup
from process_tweet import ProcessTweet
from print_or_save import PrintOrSave



def configurations():

    f = open("configurations.json", "r")
    return json.load(f)


def save_twitter_data_cursor(data, filter_users, file_name):

    raw_json = data

    is_truncated = raw_json.get("truncated")
    is_retweeted = raw_json.get("retweeted")
    user = raw_json.get("user")["screen_name"]


    if is_truncated:
        if raw_json.get("extended_tweet") is None:
            text = raw_json.get("full_text")

        else:
            text = raw_json.get("extended_tweet")['full_text']
    else:
        text = raw_json.get("text")

        if text is None:
            text = raw_json.get("full_text")

    print(text)

    if is_retweeted == True or user in filter_users or bool(re.search("^RT", text)):
        pass
    else:

        id_str = raw_json["id_str"]
        language = raw_json["lang"]
        timestamp = raw_json["created_at"]
        
        user = raw_json["user"]["screen_name"]
        user_followers = raw_json["user"]["followers_count"]
        user_friends = raw_json["user"]["friends_count"]
        user_statuses = raw_json["user"]["statuses_count"]
        user_creation = raw_json["user"]["created_at"]
        

        file_object = open(file_name, mode = 'a', encoding="utf-8")
        # Append 'hello' at the end of file

        text = re.sub('[\\n\\t\|]', ' ', text)

        tweet_string = "|".join([id_str, timestamp, user, text, str(user_followers)]) + "\n"
        
        print("linea: ", tweet_string)

        file_object.write(tweet_string)
        # Close the file
        file_object.close()

        return tweet_string



class SearchOrSimulate(PredictAndGroup, ProcessTweet):

    def __init__(self):

        # lista para ver como estructuramos los datos
        
        # Initialize instance of the subclass
        #printer = IDPrinter(
        #consumer_key, consumer_secret,
        #access_token, access_token_secret,
        #chunk_size = 1024
        #)

        # Filter realtime Tweets by keyword languages = ["es"]
        #printer.filter(track=["huawei"], languages = ["es"])

        twitter_keys = configurations()

        self.consumer_key = twitter_keys.get("consumer_key")
        self.consumer_secret = twitter_keys.get("consumer_secret")
        self.access_token = twitter_keys.get("access_token")
        self.access_token_secret = twitter_keys.get("access_token_secret")

    

    def search_30_days_ago(self,  label, query, save_file_name):
        self.label = label
        self.query = query
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth)

        
        for resp in api.search_30_day(label = self.label, query = self.query):
            
            resp = resp._json
            filter_users = configurations()

            save_twitter_data_cursor(resp, filter_users, save_file_name)
            print(resp)
            break

    def search_tweets_7_days(self, query, save_file_name):
        self.query = query
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth)

        
        for resp in api.search_tweets(q = self.query, lang = "es", tweet_mode='extended'):
            
            resp = resp._json
            filter_users = configurations()
            print(resp)

            save_twitter_data_cursor(resp, filter_users, save_file_name)
            
        
            


    def search_streaming(self, predict, model_file, cvectorizer_file):
        
        twitter_keys = configurations()

        consumer_key = twitter_keys.get("consumer_key")
        consumer_secret = twitter_keys.get("consumer_secret")
        access_token = twitter_keys.get("access_token")
        access_token_secret = twitter_keys.get("access_token_secret")

        printer = PrintOrSave(
            consumer_key, consumer_secret,
            access_token, access_token_secret,
            chunk_size = 1024
        )

     
        printer.instance_predict(predict, model_file, cvectorizer_file)

        # Filter realtime Tweets by keyword languages = ["es"]
        printer.filter(track=["huawei"], languages = ["es"])

        
    

    def simulate_search_streaming(self, file_name, predict, model_file, cvectorizer_file):
        with open(file_name, mode = "r", encoding = "utf-8") as f:
        
            for i in f:
                time.sleep(10)
                text_line = f.readline()
                print(text_line)

                if predict:
                    proccess_object = ProcessTweet()
                    tweet_dataframe = proccess_object.string_tweet_to_dataframe(text_line) 
                    transformed_tweet =  proccess_object.procesar(tweet_dataframe["text"][0])
                    
                    model_predict = PredictAndGroup(model_file, cvectorizer_file)
                    model_predict.predict(tweet_dataframe, transformed_tweet)
                    
                else:
                    print(text_line)

    

       



