def activation(yin):
    if activation_type == 1:
        if yin > theta:
            return 1
        else:
            return 0
    elif activation_type == 2:
        if yin > theta:
            return 1
        else:
            return -1

def train():
    global w, b
    max_epochs = 5
    for epoch in range(1, max_epochs + 1):
        print("\n===== Epoch", epoch, "=====")
        print("Inputs\t t\t yin\t y\t weights\t b")
        print("------------------------------------------------------------")
        error = False
        for row in data:
            x = row[:-1]
            t = row[-1]
            yin = b
            for i in range(n):
                yin += x[i] * w[i]
            y = activation(yin)
            print("{:<10} {:<5} {:<8} {:<5} {:<12} {:<5}".format(str(x),t,yin,y,str(w),b))
            if y != t:
                for i in range(n):
                    w[i] = w[i] + alpha * x[i] * t
                b = b + alpha * t
                error = True
        print("------------------------------------------------------------")
        print("Updated weights:", w, "b =", b)
        if not error:
            print("\nConverged at Epoch", epoch)
            return
    print("\nStopped at max epoch (5)")

data = []
with open("data.txt", "r") as f:
    for line in f:
        row = list(map(int, line.split()))
        data.append(row)

n = int(input("Enter number of inputs (n): "))
w = []
print("Enter initial weights:")
for i in range(n):
    w.append(int(input(f"w{i+1}: ")))
b = int(input("Enter bias (b): "))
alpha = int(input("Enter learning rate (alpha): "))

print("\nSelect Activation Function:")
print("1. Binary (0,1)")
print("2. Bipolar (-1,1)")
activation_type = int(input("Enter choice (1 or 2): "))
theta = float(input("Enter threshold value (theta): "))

train()

print("\nFinal Answer:")
print("Weights:", w)
print("Bias:", b)


