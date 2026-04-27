import csv
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from collections import Counter

def entropy(y):
    total = len(y)
    counts = Counter(y)
    entropy_value = 0.0
    for count in counts.values():
        p = count / total
        entropy_value -= p * np.log2(p + 1e-9)
    print(f"Total Entropy: H(Y) = {entropy_value:.4f}\n")
    return entropy_value

def information_gain(X, y, feature_index):
    total_entropy = entropy(y)
    weighted_entropy = 0
    values = set(row[feature_index] for row in X)

    for value in values:
        subset_y = [y[i] for i in range(len(y)) if X[i][feature_index] == value]
        subset_entropy = entropy(subset_y)
        weighted_entropy += (len(subset_y) / len(y)) * subset_entropy
        print(f"Weighted Entropy for {value}: (|Subset| / |Total|) * H(Subset) = ({len(subset_y)} / {len(y)}) * {subset_entropy:.4f}")

    gain = total_entropy - weighted_entropy
    print(f"Information Gain for feature index {feature_index}: IG = H(Y) - Weighted Entropy")
    print(f"{total_entropy:.4f} - {weighted_entropy:.4f} = {gain:.4f}\n")
    return gain

def build_tree(X, y, features):
    # If all labels are the same, return that label
    if len(set(y)) == 1:
        return y[0]

    # If no features left, return majority class
    if len(features) == 0:
        return Counter(y).most_common(1)[0][0]

    gains = [information_gain(X, y, f) for f in features]
    best_feature = features[np.argmax(gains)]

    tree = {best_feature: {}}

    values = set(row[best_feature] for row in X)
    for value in values:
        subset_X = [X[i] for i in range(len(X)) if X[i][best_feature] == value]
        subset_y = [y[i] for i in range(len(y)) if X[i][best_feature] == value]
        subtree = build_tree(subset_X, subset_y, [f for f in features if f != best_feature])
        tree[best_feature][value] = subtree

    return tree

def display_tree(tree, depth=0):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print("\t" * depth + f"Feature {key}")
            display_tree(value, depth + 1)
    else:
        print("\t" * depth + "--&gt; " + str(tree))

def main():
    Tk().withdraw()
    filename = askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])

    if not filename:
        print("No file selected. Exiting.")
        return

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    header = data[0]
    data = data[1:]

    # Separate features and target
    X = [row[:-1] for row in data]
    y = [row[-1] for row in data]

    features = list(range(len(header) - 1))  # feature indexes

    print("Dataset loaded successfully!")
    print(f"Columns: {header}")
    print(f"Sample data (first 5 rows):")
    for row in data[:5]:
        print(row)
    print()

    # Calculate entropy for target
    total = len(y)
    counts = Counter(y)
    for label in counts:
        p = counts[label] / total
        print(f"P({label}) = {p:.4f}")
        print(f"Contribution to Entropy for {label}: -P({label}) * log2(P({label})) = {-p * np.log2(p + 1e-9):.4f}")
    H = entropy(y)

    # Find root node
    gains = {f: information_gain(X, y, f) for f in features}
    root_node = max(gains, key=gains.get)
    print(f"Root Node: Feature '{header[root_node]}' (Index: {root_node}) with Highest Information Gain: {gains[root_node]:.4f}\n")

    proceed = input("Do you want to see the entire tree? (yes/no): ").lower()
    if proceed == 'yes':
        tree = build_tree(X, y, features)
        display_tree(tree)
    else:
        print("Tree display stopped.")

if __name__ == "__main__":
    main()



