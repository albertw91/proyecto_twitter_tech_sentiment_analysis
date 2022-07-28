
import nltk
from nltk import * 
import re
import pandas as pd





class ProcessTweet:

    def __init__(self):
        print()


    def procesar(self, tweet) -> str:
            
            file = self._clean_text(tweet)    

            #sentiment_code_dict = {"000":0, "010":1, "001":2, "110":3, "101":4}
            #file["sentiment_code"] = file["sentiment"].map(str)  + file["funcionality"].map(str)  + file["client_attention"].map(str) 
            #file["sentiment_code"] = file["sentiment_code"].apply(lambda x: sentiment_code_dict[x])
            print("tweet_procesado")
            print(file)
            #file.to_csv(namefile, sep=';', encoding='latin-1', index=False)
            return file
    
            
    def _clean_text(self, text):
        pattern_URL="(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})"

        text = text.lower()   
        #text=re.sub("@([A-Za-z0-9_]{1,15})", "@USUARIO", text)
        text=re.sub("@([A-Za-z0-9_]{1,15})", "", text)
        text=re.sub(pattern_URL, "", text)
        
        text= self._remove_emoji(text)
        text = re.sub("(\d+)|(rt)|(RT)", "", text)
        text = re.sub("#\w+", "", text)
        text= self._remove_stopwords(text)
        
        # text=re.sub("\d+", " ", text)
        
        text=re.sub(r" +", " ", re.sub(r"\t", " ", re.sub(r"\n+", "\n", re.sub('(?:[.,\/!$%?¿?!¡\^&\*;:{}=><\-_`~()”“"\'\|])', " ",text))))
        text = text.strip()
        return text

    def _remove_stopwords(self, text):    
        stopwords=set(nltk.corpus.stopwords.words("spanish"))
        for i in stopwords:
            text = re.sub(r"\b%s\b" % i, " ", text)
        return text

    def _remove_emoji(self, text):
        emoji_pattern = re.compile("["
                                "\U0001F600-\U0001F64F"  # emoticons
                                "\U0001F300-\U0001F5FF"  # symbols & pictographs                               
                                "\U0001F680-\U0001F6FF"  # transport & map symbols
                                "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "\U00002702-\U000027B0"
                                "\U000024C2-\U0001F251"
                                "\U0001f926-\U0001f937"
                                "\u200d"
                                "\u2640-\u2642"
                                "\U0001F1F2-\U0001F1F4"  # Macau flag
                                "\U0001F1E6-\U0001F1FF"  # flags
                                "\U0001F600-\U0001F64F"
                                "\U0001F1F2"
                                "\U0001F1F4"
                                "\U0001F620"
                                "]+", flags=re.UNICODE)   
        text = emoji_pattern.sub(r'', text) # no emoji

        return text
    

    def string_tweet_to_dataframe(self, raw_tweet):
        
        tweet_columns = ["id_str", "created_at", "screen_name", "text", "user_followers", "sentiment", "funcionality", "client_attention"]


        tweet_list = raw_tweet.split("|")
        tweet_dict = {}
        for i, v in enumerate(tweet_list):
            tweet_dict[tweet_columns[i]] = [v]
        
        tweet_dataframe = pd.DataFrame(tweet_dict, index = [0])
        print("tweet_dataframe", tweet_dataframe)
        return tweet_dataframe