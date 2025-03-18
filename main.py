import tweet_parser
import build_map


tweets = tweet_parser.extract_words("Data/cali_tweets2014.txt")

build_map.build_map(tweets)
