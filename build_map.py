import json
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point


def build_map(tweets, file_name="Data/states.json"):
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
    state_sentiments_count = {}

    for tweet in tweets:
        tweet_point = Point(float(tweet.latitude), float(tweet.longitude))
        tweet_sentiment = float(tweet.sentiment)

        found_state = None

        for state, polygons in state_data.items():
            for polygon in polygons:
                polygon_shape = Polygon(flatten_coordinates(polygon))

                if polygon_shape.contains(tweet_point):
                    found_state = state
                    break

            if found_state:
                break

        if found_state:
            state_sentiments[found_state] = state_sentiments.get(found_state, 0) + tweet_sentiment
            state_sentiments_count[found_state] = state_sentiments_count.get(found_state, 0) + 1

    state_avg_sentiments = {
        state: state_sentiments[state] / state_sentiments_count[state]
        for state in state_sentiments
    }
    return state_avg_sentiments


def build_states(state_data, tweets):
    states_sentiments = find_polygon_state(tweets, state_data)

    fig, ax = plt.subplots(figsize=(8, 6))

    for state, polygons in state_data.items():
        state_sentiment = states_sentiments.get(state, None) 

        if state_sentiment is None:
            color = (0.5, 0.5, 0.5) 
        elif state_sentiment > 0:
            color = (1, 1, 0) 
        else:
            color = (0, 0, 1) 
        for polygon in polygons:
            clean_polygon = flatten_coordinates(polygon)

            x = [points[0] for points in clean_polygon]
            y = [points[1] for points in clean_polygon]

            ax.plot(x, y, color="black")  
            ax.fill(x, y, color=color, alpha=0.7)  

        if clean_polygon:
            polygon_shape = Polygon(zip(x, y))
            centroid = polygon_shape.centroid
            ax.text(centroid.x, centroid.y, state, color="black", fontsize=8, ha='center', va='center')

    ax.set_xlabel("Долгота")
    ax.set_ylabel("Ширина")
    ax.set_title("Карта настроений по штатам")

    tweets_points(tweets, ax)
    plt.show()


def tweets_points(tweets, ax):
    for tweet in tweets:
        x = float(tweet.latitude)
        y = float(tweet.longitude)
        sentiment = tweet.sentiment

        if sentiment > 0:
            color = (1, 1, 0) 
        elif sentiment < 0:
            color = (0, 0, 1)  
        else:
            color = (0.5, 0.5, 0.5)  

        ax.scatter(x, y, color=color, edgecolors="black", s=30) 
