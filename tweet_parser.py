from tweet import Tweet


def extract_words(filename):
    all_tweets = []

    with open(filename, "r") as tweets:
        for tweet in tweets:
            parsed = parse_tweet(tweet)
            
            if parsed:
                if parsed["sentimental"] is None:
                    continue
                one_tweet = Tweet(parsed["latitude"], parsed["longitude"], parsed["sentimental"]) 
                all_tweets.append(one_tweet)

    return all_tweets

def parse_tweet(tweet: str):
    parts = tweet.split('_')

    if len(parts) >= 2:

        coordinates = parts[0][1:len(parts[0])-2]  
        latitude, longitude = map(float, coordinates.split(', '))
        
        text = parts[1].strip().split('\t')
        
        return {
            "latitude" : latitude,
            "longitude" : longitude,
            "sentimental" : set_sentimental(text[1])
        }
    return None


def set_sentimental(text, sentiment_file="Data/sorted_sentiments.csv"):
    words = text.split() 
    sentiment_values = []

    for n in range(7, 0, -1):  
        for i in range(len(words) - n + 1):
            phrase = " ".join(words[i:i+n]) 
            sentiment = get_word_sentiment(phrase, sentiment_file) 

            if sentiment is not None:
                sentiment_values.append(sentiment)

    return sum(sentiment_values) / len(sentiment_values) if sentiment_values else None


def get_word_sentiment(word, filename="Data/sorted_sentiments.csv"):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",", 1)  
            if len(parts) == 2 and parts[0] == word:
                return float(parts[1])  
    return None 