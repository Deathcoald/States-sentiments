import json
import matplotlib.pyplot as plt


def built_map(file_name = "Data/states.json"):
    state_data = extract_state(file_name)
    build_states(state_data)


def extract_state(file_name):
    with open(file_name, "r", encoding="utf-8") as states:
        return json.load(states)


def build_states(state_data):
    fig, ax = plt.subplots(figsize=(8, 6))

    for state, polygons in state_data.items():
        for polygon in polygons:
            print(polygon)
            print(state)
            x = [points[0] for points in polygon]
            y = [points[1] for points in polygon]
            ax.plot(x, y, label=state if len(ax.lines) == 0 else "")

    ax.legend()
    ax.set_xlabel("Долгота")
    ax.set_ylabel("Ширина")
    ax.set_title("Штаты")
    plt.show(block=True)


built_map()


