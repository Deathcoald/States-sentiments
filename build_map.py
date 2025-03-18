import json
import matplotlib.pyplot as plt


def build_map(tweets, file_name = "Data/states.json"):
    state_data = extract_state(file_name)
    build_states(state_data, tweets)


def extract_state(file_name):
    with open(file_name, "r", encoding="utf-8") as states:
        return json.load(states)


def build_states(state_data, tweets):
    fig, ax = plt.subplots(figsize=(8, 6))

    for state, polygons in state_data.items():
        for polygon in polygons:
            print(polygon)
            print(state)
            
            x = [points[0] for points in polygon]
            y = [points[1] for points in polygon]
            ax.plot(x, y, label=state if len(ax.lines) == 0 else "", color="black")

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
    
    ax.legend(["Tweet Locations"])
    ax.set_xlabel("Долгота")
    ax.set_ylabel("Ширина")
    ax.set_title("Штаты")

