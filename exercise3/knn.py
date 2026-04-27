import csv
import math
import random


def distance(a, b, r):
    return sum(abs(x - y) ** r for x, y in zip(a, b)) ** (1 / r)


def load(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                features = list(map(float, row[:4]))
                label = row[4]
                data.append((features, label))
    return data


def majorvote(neighbors):
    freq = {}

    for _, _, label in neighbors:
        freq[label] = freq.get(label, 0) + 1

    max_count = max(freq.values())
    max_classes = [cls for cls, cnt in freq.items() if cnt == max_count]

   
    if len(max_classes) == 1:
        predicted = max_classes[0]
    else:
        predicted = neighbors[0][2]

    return predicted, freq

def main():
    print("KNN Classification using Iris Dataset")


    random.seed(42)
    data = load("iris.data")

    
    selected = random.sample(data, 15)

    print("\n--- 15 Randomly Selected Records ---")
    for i, (features, label) in enumerate(selected, 1):
        print(f"{i:2}. {features} -> {label}")

    
    training = selected[:10]
    testing = selected[10:]

    
    test_features, test_label = random.choice(testing)

    print("\n--- Selected Test Record ---")
    print("Features:", test_features)
    print("Actual Class:", test_label)

    
    print("\nDistance Metric:")
    print("1. Euclidean (r = 2)")
    print("2. Manhattan (r = 1)")
    choice = input("Enter choice: ")

    r = 2 if choice == "1" else 1

    
    distance_table = []
    for features, label in training:
        d = distance(features, test_features, r)
        distance_table.append((features, d, label))

    distance_table.sort(key=lambda x: x[1])

    
    print("\n--- Distance Table ---")
    print(f"{'Rank':<5} | {'Training Record':<35} | {'Distance':<10} | Class")
    print("-" * 80)

    for i, (features, dist, label) in enumerate(distance_table, 1):
        print(f"{i:<5} | {str(features):<35} | {dist:.4f}     | {label}")

    k = int(input("\nEnter K value: "))

    neighbors = distance_table[:k]

    print(f"\n--- Top {k} Nearest Neighbors ---")
    print(f"{'Rank':<5} | {'Distance':<10} | Class")
    print("-" * 40)

    for i, (_, dist, label) in enumerate(neighbors, 1):
        print(f"{i:<5} | {dist:.4f}     | {label}")

    
    predicted_class, vote_count = majorvote(neighbors)

    print("\nClass Frequency:", vote_count)

    if list(vote_count.values()).count(max(vote_count.values())) > 1:
        print("Tie detected → Selected class of nearest neighbor")

    print("\nFinal Predicted Class:", predicted_class)
    print("Actual Class:", test_label)

if __name__ == "__main__":
    main()



