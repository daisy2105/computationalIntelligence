class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []   # (from, to, cost)

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return "Node added"
        else:
            return "Node already exists"

    def deleteNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.edges = [e for e in self.edges if e[0] != node and e[1] != node]
            return "Node deleted"
        else:
            return "Node not found"

    def addEdge(self, u, v, cost):
        if u in self.nodes and v in self.nodes:
            self.edges.append((u, v, cost))
            return "Edge added"
        else:
            return "Invalid nodes"

    def deleteEdge(self, u, v):
        new_edges = []
        found = False
        for e in self.edges:
            if e[0] == u and e[1] == v:
                found = True
            else:
                new_edges.append(e)
        self.edges = new_edges
        return "Edge deleted" if found else "Edge not found"

    def display_adjlist(self):
        adj_list = {}
        for n in self.nodes:
            adj_list[n] = []
            for e in self.edges:
                if e[0] == n:
                    adj_list[n].append((e[1], e[2]))
        return adj_list

    def A_Star(self, start, goal, heuristic):
        """
        heuristic: dict with node: heuristic_value (int)
        Returns: (optimal_path(list), optimal_cost(int)) or (None, None) if no path
        Also prints stepwise open and closed lists for tracing.
        """
        open_list = [[start, [start], 0]]
        open_dict = {start: open_list[0]}
        closed_list = set()
        g_score = {start: 0}

        step = 0
        while open_list:
            step += 1
            # Sort by f = g + h
            open_list.sort(key=lambda x: x[2] + heuristic.get(x[0], 0))

            # Debug print of open list and closed list
            print(f"\nStep : {step}")
            print("Open List:")
            for item in open_list:
                f_score = item[2] + heuristic.get(item[0], 0)
                print(f"Node: {item[0]}, Path: {item[1]}, g: {item[2]}, h: {heuristic.get(item[0], 0)}, f: {f_score}")
            print(f"Closed List: {closed_list}")

            current, path, g = open_list.pop(0)
            del open_dict[current]

            if current == goal:
                print("\nGoal reached!")
                print("Optimal Path:", path)
                print("Optimal Cost:", g)
                return path, g

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
        return None, None

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
        g.addNode(input("Enter node: "))

    elif choice == 2:
        g.deleteNode(input("Enter node to delete: "))

    elif choice == 3:
        u = input("From node: ")
        v = input("To node: ")
        c = int(input("Cost: "))
        g.addEdge(u, v, c)

    elif choice == 4:
        g.deleteEdge(input("From node: "), input("To node: "))

    elif choice == 5:
        g.display_adjlist()

    elif choice == 6:
        start = input("Enter the start node: ")
        goal = input("Enter the goal node: ")
        g.A_Star(start, goal)

    elif choice == 7:
        print("Exiting...")
        break



