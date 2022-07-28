from search_or_simulate import SearchOrSimulate

streammer = SearchOrSimulate()
#streammer.simulate_search_streaming("tweets_search.txt", predict = True, model_file = "preprocesing_model/best_keras_network_model.h5", cvectorizer_file = "preprocesing_model/count_vectorizer.joblib")
#streammer.search_streaming(predict = True, model_file = "preprocesing_model/best_keras_network_model.h5", cvectorizer_file = "preprocesing_model/count_vectorizer.joblib")
#streammer.search_30_days_ago(label = "dev", query = "huawei", save_file_name = "tweets_search.txt")
streammer.search_tweets_7_days(query = "huawei", save_file_name = "tweets_search.txt")

#transformed_tweet