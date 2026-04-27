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
                # Assuming class label is in column 2 and features from columns 3-6
                # Adjusting for 0-based indexing: class label is index 1, features are indices 2-5
                features = list(map(float, row[2:6])) # Extract features from column 3 to 6
                label = row[1] # Class label is in column 2
                data.append((features, label))
    return data

def min_max_normalize(data):
    features_only = [item[0] for item in data]
    num_features = len(features_only[0])
    min_vals = [min(features_only[i][j] for i in range(len(features_only))) for j in range(num_features)]
    max_vals = [max(features_only[i][j] for i in range(len(features_only))) for j in range(num_features)]

    normalized_data = []
    for features, label in data:
        normalized_features = []
        for j in range(num_features):
            if (max_vals[j] - min_vals[j]) != 0:
                normalized_value = (features[j] - min_vals[j]) / (max_vals[j] - min_vals[j])
            else:
                normalized_value = 0
            normalized_features.append(normalized_value)
        normalized_data.append((normalized_features, label))
    return normalized_data

def majorvote(neighbors, is_weighted=False):
    freq = {}
    for features, metric_value, label, _ in neighbors: # Unpack original_d but not used in vote calculation
        if is_weighted:
            # If weighted, metric_value is already 1/d^2. Handle inf case.
            weight = metric_value if metric_value != float('inf') else 1000000 # Assign a very large weight for inf
        else:
            # If unweighted, metric_value was 'd', but for voting, we just count as 1
            weight = 1
        freq[label] = freq.get(label, 0) + weight

    if not freq:
        return None, {}

    max_count = max(freq.values())
    max_classes = [cls for cls, cnt in freq.items() if cnt == max_count]

    if len(max_classes) == 1:
        predicted = max_classes[0]
    else:
        # Tie-breaking: choose the class of the 'nearest' neighbor.
        # Since neighbors are sorted by the metric_value, the first one is the "best".
        predicted = neighbors[0][2] 
    return predicted, freq

def main():
    print("KNN Classification using Breast cancer Dataset")
    random.seed(42)
    # Using 'wdbc.data' as specified
    data = load("wdbc.data")

    needs_normalization = False
    for features, _ in data:
        if any(f > 10 for f in features):
            needs_normalization = True
            break

    if needs_normalization:
        print("\n--- Performing Min-Max Normalization ---")
        data = min_max_normalize(data)

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
    
    # Menu for weighted/unweighted voting
    print("\nSelect Voting Method:")
    print("1. Unweighted Voting")
    print("2. Weighted Voting (1/d^2)")
    vote_choice = input("Enter choice: ")
    is_weighted_voting = (vote_choice == "2")

    distance_table = []
    for features, label in training:
        d = distance(features, test_features, r)
        
        # Store the appropriate metric in the distance_table based on voting choice
        if is_weighted_voting:
            # Store 1/d^2 for weighted. If d is 0, make it a very large number for sorting.
            metric_for_table = (1 / (d ** 2)) if d != 0 else float('inf') 
        else:
            metric_for_table = d # Store d for unweighted

        distance_table.append((features, metric_for_table, label, d)) # Always store original 'd' for potential display

    # Sort the distance table based on the metric_for_table
    # If unweighted, sort by 'd' (ascending). If weighted, sort by '1/d^2' (descending - highest weight first).
    distance_table.sort(key=lambda x: x[1] if not is_weighted_voting else -x[1])


    print("\n--- Distance Table ---")
    # Display the appropriate 'Distance' based on the voting method chosen
    distance_header = "Distance (1/d^2)" if is_weighted_voting else "Distance"
    # Use a fixed width for the distance column
    print(f"{'Rank':<5} | {'Training Record':<35} | {distance_header:<16} | Class")
    print("-" * 85) # Adjusted line length
    for i, (features, metric_val, label, original_d) in enumerate(distance_table, 1):
        display_dist = metric_val if is_weighted_voting else original_d
        # Format display_dist with a fixed width, handling 'inf' gracefully
        if display_dist == float('inf'):
            formatted_dist = "inf".ljust(16)
        else:
            formatted_dist = f"{display_dist:.4f}".ljust(16)
        print(f"{i:<5} | {str(features):<35} | {formatted_dist} | {label}")
    
    k = int(input("\nEnter K value: "))
    neighbors = distance_table[:k] # Select top K neighbors based on the sorted metric_for_table
    
    print(f"\n--- Top {k} Nearest Neighbors ---")
    print(f"{'Rank':<5} | {distance_header:<16} | Class") # Display the appropriate 'Distance' header
    print("-" * 45) # Adjusted line length
    for i, (_, metric_val, label, original_d) in enumerate(neighbors, 1):
        display_dist = metric_val if is_weighted_voting else original_d
        # Format display_dist with a fixed width, handling 'inf' gracefully
        if display_dist == float('inf'):
            formatted_dist = "inf".ljust(16)
        else:
            formatted_dist = f"{display_dist:.4f}".ljust(16)
        print(f"{i:<5} | {formatted_dist} | {label}")
    
    predicted_class, vote_count = majorvote(neighbors, is_weighted=is_weighted_voting) # Pass is_weighted to majorvote
    
    print("\nClass Frequency:", vote_count)

    if predicted_class is None:
        print("No neighbors selected, cannot predict class.")
    else:
        # Check for tie in majorvote results
        max_votes = max(vote_count.values())
        tied_classes = [cls for cls, votes in vote_count.items() if votes == max_votes]
        if len(tied_classes) > 1:
            print("Tie detected → Selected class of nearest neighbor")

    print("\nFinal Predicted Class:", predicted_class)
    print("Actual Class:", test_label)

if __name__ == "__main__":
    main()


