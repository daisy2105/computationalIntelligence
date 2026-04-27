import math

def read_data(filename):
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n")
    headers = lines[0].split(",")
    data = [line.split(",") for line in lines[1:]]
    return headers, data

def entropy_calc(values):
    total = len(values)
    if total == 0: return 0, "0"

    unique_counts = {}
    for v in values:
        unique_counts[v] = unique_counts.get(v, 0) + 1

    ent = 0
    steps = []
    for val, count in unique_counts.items():
        p = count / total
        ent -= p * math.log2(p)
        steps.append(f"({count}/{total})log2({count}/{total})")

    step_str = "-[" + " + ".join(steps) + "]"
    return ent, step_str

def information_gain(data, attr_index, target_index, total_entropy, attr_name):
    print(f"\nAttribute: {attr_name}")
    print("-" * 60)

    values = sorted(list(set(row[attr_index] for row in data)))
    total_records = len(data)

    # 1. Print Frequency Table first
    print(f"{'Value':<15} | {'Pass':<8} | {'Fail':<8}")
    print("-" * 35)

    subsets_info = []
    for val in values:
        subset = [row[target_index] for row in data if row[attr_index] == val]
        p_count = subset.count("Pass")
        f_count = subset.count("Fail")
        print(f"{val:<15} | {p_count:<8} | {f_count:<8}")

        ent_val, ent_step = entropy_calc(subset)
        subsets_info.append({
            'val': val,
            'ent': ent_val,
            'step': ent_step,
            'size': len(subset)
        })

    # 2. Print Calculation Steps below the table
    print("\n--- Entropy Calculations ---")
    weighted_parts = []
    weighted_entropy = 0

    for info in subsets_info:
        print(f"Entropy({info['val']}) = {info['step']} = {round(info['ent'], 4)}")
        weight = info['size'] / total_records
        weighted_entropy += weight * info['ent']
        weighted_parts.append(f"({info['size']}/{total_records} * {round(info['ent'], 4)})")

    print(f"\nWeighted Entropy (E_avg):")
    print(f"E_avg = {' + '.join(weighted_parts)}")
    print(f"E_avg = {round(weighted_entropy, 4)}")

    gain = total_entropy - weighted_entropy
    print(f"\nInformation Gain:")
    print(f"Gain = Total Entropy - E_avg")
    print(f"Gain = {round(total_entropy, 4)} - {round(weighted_entropy, 4)} = {round(gain, 4)}")

    return gain

def find_root_node(filename):
    headers, data = read_data(filename)
    target_index = len(headers) - 1
    target_values = [row[target_index] for row in data]

    total_ent, total_ent_step = entropy_calc(target_values)

    print("=" * 60)
    print(f"Target Attribute: {headers[target_index]}")
    print(f"Total System Entropy = {total_ent_step} = {round(total_ent, 4)}")
    print("=" * 60)

    gains = {}
    for i in range(target_index):
        gain = information_gain(data, i, target_index, total_ent, headers[i])
        gains[headers[i]] = gain

    print("\n" + "=" * 60)
    print(f"{'Summary of Information Gain':^60}")
    print("-" * 60)

    for attr, g in gains.items():
        print(f"{attr:<20}: {round(g, 4)}")

    root = max(gains, key=gains.get)
    print("-" * 60)
    print(f"Root Node: {root} (Max Gain: {round(gains[root], 4)})")
    print("=" * 60)

# Run the function
if __name__ == "__main__":
    # Ensure data.txt exists in the same directory
    find_root_node("data.txt")


