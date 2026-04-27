class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []   # (from, to, cost)

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            print("Node added")
        else:
            print("Node already exists")

    def deleteNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.edges = [e for e in self.edges if e[0] != node and e[1] != node]
            print("Node deleted")
        else:
            print("Node not found")

    def addEdge(self, u, v, cost):
        if u in self.nodes and v in self.nodes:
            self.edges.append((u, v, cost))
            print("Edge added")
        else:
            print("Invalid nodes")

    def deleteEdge(self, u, v):
        new_edges = []
        found = False
        for e in self.edges:
            if e[0] == u and e[1] == v:
                found = True
            else:
                new_edges.append(e)
        self.edges = new_edges
        print("Edge deleted" if found else "Edge not found")

    def display_adjlist(self):
        print("\nAdjacency List:")
        for n in self.nodes:
            print(n, "->", end=" ")
            for e in self.edges:
                if e[0] == n:
                    print(f"{e[1]}(cost={e[2]})", end=" ")
            print()

    def A_Star(self, start, goal):
        heuristic = {}
        print("\nEnter heuristic values:")
        for node in self.nodes:
            heuristic[node] = int(input(f"h({node}) = "))

        open_list = [[start, [start], 0]]
        open_dict = {start: open_list[0]}
        closed_list = set()
        g_score = {start: 0}
	step=0
        while open_list:
	    step+=1
	    print(f"Step : {step}")
            open_list.sort(key=lambda x: x[2] + heuristic[x[0]])
	    print("Open List: ")
	    for item in open_list:
	        f_score = item[2] + heuristic[item[0]]
		print(f"Node: {item[0]}, Path: {item[1]}, g: {item[2]}, h: {heuristic[item[0]]}, f: {f_score}")


	    print(f"Closed List : {closed_list}")

            current, path, g = open_list.pop(0)
            del open_dict[current]

            if current == goal:
                print("\nGoal reached!")
                print("Optimal Path:", path)
                print("Optimal Cost:", g)
                return

            closed_list.add(current)

            for e in self.edges:
                if e[0] == current:
                    neighbor = e[1]
                    cost = e[2]
                    tentative_g = g + cost

                    if neighbor in closed_list:
                        continue

                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        new_path = path + [neighbor]

                        if neighbor in open_dict:
                            for item in open_list:
                                if item[0] == neighbor:
                                    item[1] = new_path
                                    item[2] = tentative_g
                                    break
                        else:
                            open_list.append([neighbor, new_path, tentative_g])
                            open_dict[neighbor] = [neighbor, new_path, tentative_g]

        print("No path found")


if __name__ == '__main__':
    g = Graph()

while True:
    print("\n1. addNode")
    print("2. deleteNode")
    print("3. addEdge")
    print("4. deleteEdge")
    print("5. display_adjlist")
    print("6. A*Search")
    print("7. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        node = input("Enter node: ")
        g.addNode(node)

    elif choice == 2:
        node = input("Enter node to delete: ")
        g.deleteNode(node)

    elif choice == 3:
        u = input("From node: ")
        v = input("To node: ")
        cost = int(input("Cost: "))
        g.addEdge(u, v, cost)

    elif choice == 4:
        u = input("From node: ")
        v = input("To node: ")
        g.deleteEdge(u, v)

    elif choice == 5:
        g.display_adjlist()

    elif choice == 6:
        start = input("Enter the start node: ")
        goal = input("Enter the goal node: ")
        g.A_Star(start, goal)

    elif choice == 7:
        print("Exiting program")
        break

    else:
        print("Invalid choice")

