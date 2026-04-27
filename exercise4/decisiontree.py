import math

def read_dataset(filename):
    file = open(filename, 'r')
    lines = file.read().strip().split('\n')
    file.close()

    headers = lines[0].split(',')
    data = []

    for line in lines[1:]:
        data.append(line.split(','))

    return headers, data

def entropy(values):
    total = len(values)
    ent = 0.0
    unique_values = []

    for v in values:
        if v not in unique_values:
            unique_values.append(v)

    for v in unique_values:
        count = 0
        for val in values:
            if val == v:
                count += 1

        p = count / total
        ent -= p * math.log2(p)

    return ent

def information_gain(data, attr_index, target_index, total_entropy, attr_name):
    values = []

    for row in data:
        if row[attr_index] not in values:
            values.append(row[attr_index])

    print("\nAttribute:", attr_name)
    print("-" * 40)

    weighted_entropy = 0.0
    total = len(data)

    for val in values:
        subset_targets = []

        for row in data:
            if row[attr_index] == val:
                subset_targets.append(row[target_index])

        ent = entropy(subset_targets)
        weight = len(subset_targets) / total
        weighted_entropy += weight * ent

        labels = []
        for t in subset_targets:
            if t not in labels:
                labels.append(t)

        count_str = ""
        for l in labels:
            count = 0
            for t in subset_targets:
                if t == l:
                    count += 1
            count_str += f"{l}={count} "

        print(
            f"Value = {val:10} | "
            f"{count_str:15} | "
            f"Entropy = {ent:.4f}"
        )

    gain = total_entropy - weighted_entropy

    print(f"Entropy after split ({attr_name}) = {weighted_entropy:.4f}")
    print(f"Information Gain ({attr_name}) = {gain:.4f}")

    return gain

def find_root_node(filename):
    headers, data = read_dataset(filename)

    target_index = len(headers) - 1
    target_name = headers[target_index]

    target_values = []
    for row in data:
        target_values.append(row[target_index])

    total_entropy = entropy(target_values)

    print("\nTarget Attribute:", target_name)
    print("Total Entropy =", round(total_entropy, 4))

    gains = {}

    print("\n========== Intermediate Entropy Calculations ==========")

    for i in range(target_index):
        gain = information_gain(
            data, i, target_index, total_entropy, headers[i]
        )
        gains[headers[i]] = gain

    print("\n========== Information Gain Table ==========")
    print("-" * 45)
    print("Attribute        Information Gain")
    print("-" * 45)

    for attr in gains:
        print(f"{attr:15} {gains[attr]:.4f}")

    # Find root node
    root = None
    max_gain = -1

    for attr in gains:
        if gains[attr] > max_gain:
            max_gain = gains[attr]
            root = attr

    print("\nRoot Node (Maximum Information Gain):", root)
    print("Gain =", round(max_gain, 4))

find_root_node("data.txt")




