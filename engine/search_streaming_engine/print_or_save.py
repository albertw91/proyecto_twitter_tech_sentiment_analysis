

import tweepy
import json
import re
from process_tweet import ProcessTweet
from predict_and_group import PredictAndGroup


def read_filter_users():
    #file_object = open('filter_users.txt', mode = 'r', encoding="utf-8")
    #filter_users = file_object.read()
    #filter_users = filter_users.split("\n")
    #print(filter_users)

    return ["ho"] #filter_users

class PrintOrSave(tweepy.Stream, ProcessTweet, PredictAndGroup):

    def instance_predict(self, predict, model_file, cvectorizer_file):
        
        #self.filter_users = filter_users
        #self.file_name = file_name
        self.predict = predict
        self.model_file = model_file
        self.cvectorizer_file = cvectorizer_file
    

    def on_data(self, data):

        test_list_origin = []
        test_list = []

        #list_data = extract_tweet_data(data)
        #print(f"Usuario: {list_data[4]}, Mensaje: {list_data[3]}")
        filter_users = read_filter_users()
        self._print_or_save(data, self.predict, filter_users, self.model_file, self.cvectorizer_file)

        

        # funcion de sql para guardar los tweets

        #test_list_origin.append(data)
        #test_list.append(list_data)

        return True

    def on_status(self, status):
        print(status.id)

        
    def _print_or_save(self, data, predict, filter_users, model_file, cvectorizer_file):

        raw_json = json.loads(data)
        print(raw_json.keys())
        is_truncated = raw_json.get("truncated")
        is_retweeted = raw_json.get("retweeted")
        user = raw_json.get("user")["screen_name"]
        text = raw_json.get("text")

        if is_retweeted == True or user in filter_users or bool(re.search("^RT", text)):
            pass
        else:
            if is_truncated:
                text = raw_json.get("extended_tweet")['full_text']
            
            else:
                text = raw_json["text"]

        
            id_str = raw_json["id_str"]
            language = raw_json["lang"]
            timestamp = raw_json["created_at"]
            user = raw_json["user"]["screen_name"]
            user_followers = raw_json["user"]["followers_count"]
            user_friends = raw_json["user"]["friends_count"]
            user_statuses = raw_json["user"]["statuses_count"]
            user_creation = raw_json["user"]["created_at"]

            text = re.sub('[\\n\\t\|;,]', ' ', text)
            text_line = "|".join([id_str, timestamp, user, text, str(user_followers)]) + "\n"
            
            if predict:

                #file_object = open(file_name, mode = 'a', encoding="utf-8")
                # Append 'hello' at the end of file

                proccess_object = ProcessTweet()
                tweet_dataframe = proccess_object.string_tweet_to_dataframe(text_line) 
                transformed_tweet =  proccess_object.procesar(tweet_dataframe["text"][0])
                
                model_predict = PredictAndGroup(model_file, cvectorizer_file)
                model_predict.predict(tweet_dataframe, transformed_tweet)
                print("linea: ", text_line)

            else:
                print("linea: ", text_line)

