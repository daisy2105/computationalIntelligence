import math
import csv
from collections import Counter

def calculate_entropy(labels):
    labels = [lbl for lbl in labels if lbl]
    if not labels: return 0, "0"
    total = len(labels)
    counts = Counter(labels)

    entropy = 0
    formula_parts = []

    for label in counts:
        p = counts[label] / total
        entropy -= p * math.log2(p)
        formula_parts.append(f"({counts[label]}/{total} * log2 {counts[label]}/{total})")

    formula_str = " - ".join(formula_parts)
    if len(counts) > 1:
        formula_str = "- [" + formula_str + "]"
    else:
        formula_str = "- " + formula_str

    return entropy, formula_str

def build_decision_tree(dataset, feature_names, label_name):
    labels = [row[label_name] for row in dataset]
    label_counts = Counter(labels)
    if len(label_counts) == 1:
        return labels[0]

    if not feature_names:
        return label_counts.most_common(1)[0][0]

    total_entropy, _ = calculate_entropy(labels)
    best_gain = -1
    best_feature = None
    best_subsets = {}

    for feature in feature_names:
        distinct_values = set(row[feature] for row in dataset)
        weighted_entropy = 0
        subsets = {}

        for val in distinct_values:
            subset = [row for row in dataset if row[feature] == val]
            subset_labels = [row[label_name] for row in subset]
            subsets[val] = subset
            ent, _ = calculate_entropy(subset_labels)
            weighted_entropy += (len(subset) / len(dataset)) * ent

        gain = total_entropy - weighted_entropy

        if gain > best_gain:
            best_gain = gain
            best_feature = feature
            best_subsets = subsets

    tree = {best_feature: {}}
    remaining_features = [f for f in feature_names if f != best_feature]

    for value, subset in best_subsets.items():
        if not subset:
            tree[best_feature][value] = label_counts.most_common(1)[0][0]
        else:
            subtree = build_decision_tree(subset, remaining_features, label_name)
            tree[best_feature][value] = subtree

    return tree

def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "-> " + str(tree))
        return

    for feature, branches in tree.items():
        print(indent + "[" + feature + "]")
        for value, subtree in branches.items():
            print(indent + "|-- " + str(value))
            print_tree(subtree, indent + "|   ")

def analyze_dataset(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader((line for line in f if line.strip()))
            dataset = []
            for row in reader:
                cleaned_row = {k.strip(): v.strip() for k, v in row.items()}
                dataset.append(cleaned_row)

            if not dataset: return

            all_keys = list(dataset[0].keys())
            feature_names = all_keys[:-1]
            label_name = all_keys[-1]

            parent_labels = [row[label_name] for row in dataset]
            unique_labels = sorted(set(parent_labels))
            initial_entropy, initial_formula = calculate_entropy(parent_labels)

            print(f"\n{'='*20} STEP 1: INITIAL ANALYSIS {'='*20}")
            counts = Counter(parent_labels)
            for lbl in unique_labels:
                print(f"Total {lbl:5}: {counts[lbl]}")
            print(f"Initial Entropy Calculation: {initial_formula}")
            print(f"Initial Total Entropy : {initial_entropy:.4f}")

            gain_results = []
            best_gain = -1
            root_node = ""

            for feature in feature_names:
                print(f"\n>>> ANALYSING FEATURE: {feature.upper()}")

                header = f"{'Value':15}" + "".join([f"{lbl:>10}" for lbl in unique_labels])
                print(header)
                print("-" * len(header))

                distinct_values = sorted(set(row[feature] for row in dataset))
                weighted_entropy = 0
                n = len(dataset)
                subsets = {}

                expansion_parts = []

                for val in distinct_values:
                    subset_labels = [row[label_name] for row in dataset if row[feature] == val]
                    subsets[val] = subset_labels
                    subset_counts = Counter(subset_labels)
                    row_str = f"{val:15}" + "".join([f"{subset_counts[lbl]:>10}" for lbl in unique_labels])
                    print(row_str)

                print("-" * len(header))
                print()

                for val in distinct_values:
                    ent, formula = calculate_entropy(subsets[val])
                    print(f"  * {val:10}: {formula} = {ent:.4f}")

                    weight_fraction = f"({len(subsets[val])}/{n} * {ent:.4f})"
                    expansion_parts.append(weight_fraction)
                    weighted_entropy += (len(subsets[val]) / n) * ent

                print(f"\nWeighted Entropy for {feature}:")
                print(f"  E = {' + '.join(expansion_parts)}")
                print(f"Total Weighted Entropy: {weighted_entropy:.4f}")

                gain = initial_entropy - weighted_entropy
                gain_results.append((feature, gain))

                print(f"Information Gain: {initial_entropy:.4f} - {weighted_entropy:.4f} = {gain:.4f}")

                if gain > best_gain:
                    best_gain = gain
                    root_node = feature

            print(f"\n{'='*20} STEP 3: SUMMARY OF GAINS {'='*20}")
            for feat, g in gain_results:
                print(f"{feat:15} | {g:18.4f}")

            print(f"\nRESULT: THE ROOT NODE IS '{root_node.upper()}'\n")

            print("\n" + "="*20 + " FULL DECISION TREE " + "="*20)
            tree = build_decision_tree(dataset, feature_names, label_name)
            print_tree(tree)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    file_path = input("Enter the path to your CSV file: ").strip()
    analyze_dataset(file_path)


