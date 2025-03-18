class Tweet:
    def __init__(self, latitude: str, longitude: str, sentiment):
        self.sentiment = sentiment

        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self):
        return f"Tweet({self.latitude}, {self.longitude}, Sentiment: {self.sentiment})"
    
    def __repr__(self):
        return self.__str__()  
    
