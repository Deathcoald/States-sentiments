class Tweet:
    def __init__(self,longitude: str , latitude: str, sentiment):
        self.sentiment = sentiment

        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self):
        return f"Tweet({self.longitude}, {self.latitude}, Sentiment: {self.sentiment})"
    
    def __repr__(self):
        return self.__str__()  
    
