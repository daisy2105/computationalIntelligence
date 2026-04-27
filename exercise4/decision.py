import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def entropy(y):
    value_counts = y.value_counts(normalize=True)
    entropy_value = -np.sum(value_counts * np.log2(value_counts + 1e-9))
    print(f"Total Entropy: H(Y) = {entropy_value:.4f}\n")
    return entropy_value

def information_gain(X, y, feature):
    total_entropy = entropy(y)
    weighted_entropy = 0

    values = X[feature].unique()
    for value in values:
        subset = y[X[feature] == value]
        subset_entropy = entropy(subset)
        weighted_entropy += (len(subset) / len(y)) * subset_entropy
        print(f"Weighted Entropy for {value}: (|Subset| / |Total|) * H(Subset) = ({len(subset)} / {len(y)}) * {subset_entropy:.4f}")

    gain = total_entropy - weighted_entropy
    print(f"Information Gain for '{feature}': IG = H(Y) - Weighted Entropy")
    print(f"{total_entropy:.4f} - {weighted_entropy:.4f} = {gain:.4f}\n")
    return gain

def build_tree(X, y, features):
    # If all labels are the same, return that label
    if len(y.unique()) == 1:
        return y.iloc[0]

    # If no features left, return majority class
    if len(features) == 0:
        return y.mode()[0]

    # Calculate gains for all features
    gains = [information_gain(X, y, feature) for feature in features]
    best_feature = features[np.argmax(gains)]

    tree = {best_feature: {}}

    for value in X[best_feature].unique():
        subset_X = X[X[best_feature] == value]
        subset_y = y[X[best_feature] == value]
        subtree = build_tree(subset_X, subset_y, [f for f in features if f != best_feature])
        tree[best_feature][value] = subtree

    return tree

def display_tree(tree, depth=0, dict=None):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print("\t" * depth + str(key))
            display_tree(value, depth + 1)
    else:
        print("\t" * depth + "--> " + str(tree))

def main():
    Tk().withdraw()
    filename = askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])

    if not filename:
        print("No file selected. Exiting.")
        return

    data = pd.read_csv(filename)
    print("Dataset loaded successfully!")
    print(data.head())
    print()

    # Drop the target column; last column assumed to be target
    target_col = data.columns[-1]
    X = data.drop(columns=[target_col])
    y = data[target_col]
    features = list(X.columns)

    print("Calculating Entropy:")
    P_yes = (y == y.unique()[0]).sum() / len(y)
    P_no = 1 - P_yes
    print(f"P(yes) = {P_yes:.4f}")
    print(f"Contribution to Entropy for yes: -P(yes) * log2(P(yes)) = {-P_yes * np.log2(P_yes + 1e-9):.4f}")
    print(f"P(no) = {P_no:.4f}")
    print(f"Contribution to Entropy for no: -P(no) * log2(P(no)) = {-P_no * np.log2(P_no + 1e-9):.4f}")
    H = -P_yes * np.log2(P_yes + 1e-9) - P_no * np.log2(P_no + 1e-9)
    print(f"Total Entropy: H(Y) = {H:.4f}\n")

    # Find root node
    gains = {feature: information_gain(X, y, feature) for feature in features}
    root_node = max(gains, key=gains.get)
    print(f"Root Node: '{root_node}' (Highest Information Gain: {gains[root_node]:.4f})\n")

    proceed = input("Do you want to see the entire tree? (yes/no): ").lower()
    if proceed == 'yes':
        tree = build_tree(X, y, features)
        display_tree(tree)
    else:
        print("Tree display stopped.")

if __name__ == "__main__":
    main()




