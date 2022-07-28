

from joblib import dump, load
from keras.models import load_model
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



class PredictAndGroup:

    def __init__(self, model_file, cvectorizer_file):

        #model_file = kwargs["model_file"]
        #cvectorizer_file = kwargs["cvectorizer_file"]
       
        self.model = load_model(model_file)

        self.cvectorizer = load(cvectorizer_file)


    def predict(self, tweet_dataframe, transformed_tweet):

        X_stream = self.cvectorizer.transform([transformed_tweet]).toarray()
        print(X_stream)

        # make predictions
        predict_stream = self.model.predict(X_stream)
        predict_list = predict_stream.round()
        
        predict_list = list(map(lambda x: int(x), list(predict_list[0])))


        tweet_dataframe["sentiment"] = predict_list[0]
        tweet_dataframe["funcionality"]	= predict_list[1]
        tweet_dataframe["client_attention"] = predict_list[2]

        tweet_dataframe["sentiment_code"] = tweet_dataframe["sentiment"].map(str)  + tweet_dataframe["funcionality"].map(str)  + tweet_dataframe["client_attention"].map(str)


        try:
            tweet_dataframe.to_csv("dash_app/data/stream_tweet.csv", sep = ",", mode = "a", index=False, header= False, encoding= "utf-8")
            self._group_dataframe()
            
        except:
            tweet_dataframe.to_csv("dash_app/data/stream_tweet.csv", sep = ",", index=False, header = True, encoding= "utf-8")
            self._group_dataframe()
            

    def _group_dataframe(self):

        tweet_dataframe = pd.read_csv("dash_app/data/stream_tweet.csv", sep = ",", encoding= "latin-1", dtype = {'id_str': str, 'sentiment_code': str})
        print("sentiment code:", tweet_dataframe[["sentiment_code"]].head())
        tweet_dataframe_count = tweet_dataframe.groupby("sentiment_code").count()[["id_str"]]
        tweet_dataframe_count= tweet_dataframe_count.rename({"id_str": "count"}, axis = 1)
        tweet_dataframe_count.reset_index(inplace = True)
        tweet_dataframe_count["sentiment_code"] = tweet_dataframe_count["sentiment_code"].astype(str)

        print("group_dataframe", tweet_dataframe_count)
    
        tweet_dataframe_count.to_csv("dash_app/data/stream_tweet_groupby.csv", sep = ",", index=False, header= True, encoding= "utf-8")





        

        