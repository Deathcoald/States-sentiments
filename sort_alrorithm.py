def sort_sentiments_file(input_filename, output_filename):
    with open(input_filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    sentiments = []
    for line in lines:
        parts = line.strip().split(",", 1)
        if len(parts) == 2:
            word, value = parts
            sentiments.append((word, value))

    sentiments.sort(key=lambda item: len(item[0].split()), reverse=True)

    with open(output_filename, "w", encoding="utf-8") as file:
        for word, value in sentiments:
            file.write(f"{word},{value}\n")

sort_sentiments_file("Data/sentiments.csv", "Data/sorted_sentiments.csv")
