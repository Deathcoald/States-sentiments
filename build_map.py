import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point


def build_map(tweets, file_name = "Data/states.json"):
    state_data = extract_state(file_name)
    build_states(state_data, tweets)


def extract_state(file_name):
    with open(file_name, "r", encoding="utf-8") as states:
        return json.load(states)


def flatten_coordinates(polygon):
    flat_coords = []
    for points in polygon:
        if isinstance(points, list) and len(points) == 2 and all(isinstance(coord, (int, float)) for coord in points):
            flat_coords.append(points)  
        elif isinstance(points, list):  
            flat_coords.extend(flatten_coordinates(points))
    return flat_coords


def find_polygon_state(tweets, state_data):

    state_sentiments = {}

    for tweet in tweets:
        tweet_point = Point(float(tweet.latitude), float(tweet.longitude))
        tweet_sentiment = float(tweet.sentiment)

        found_state = None

        for state, polygons in state_data.items():
            for polygon in polygons:
                polygon_shape = Polygon(flatten_coordinates(polygon))
                print(polygon_shape.is_valid)

                if polygon_shape.contains(tweet_point):
                    found_state = state
                    break

            if found_state:
                break

        if found_state:
            state_sentiments[found_state] = state_sentiments.get(found_state, 0) + tweet_sentiment

    return state_sentiments
        
def build_states(state_data, tweets):
    print(find_polygon_state(tweets, state_data))

    fig, ax = plt.subplots(figsize=(8, 6))

    for state, polygons in state_data.items():
        state_x = []
        state_y = []

        for polygon in polygons:
            clean_polygon = flatten_coordinates(polygon)

            x = [points[0] for points in clean_polygon]
            y = [points[1] for points in clean_polygon]

            state_x.extend(x)
            state_y.extend(y)

            ax.plot(x, y, label=state if len(ax.lines) == 0 else "", color="black")

        if state_x and state_y:
            polygon_shape = Polygon(zip(state_x, state_y))
            centroid = polygon_shape.centroid

            ax.plot(centroid.x, centroid.y, color="red", marker="o", markersize=5)       

    ax.legend()
    ax.set_xlabel("Долгота")
    ax.set_ylabel("Ширина")
    ax.set_title("Штаты")

    tweets_points(tweets, ax)

    plt.show()

def tweets_points(tweets, ax):
    
    for tweet in tweets:
        x = float(tweet.latitude)
        y = float(tweet.longitude)
        ax.plot(x, y, color="black", marker="o", markersize=5)

