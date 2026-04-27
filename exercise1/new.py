class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNode(self, node):
        self.nodes.append(node)

    def deleteNode(self, node):
        self.nodes.remove(node)
        for i in list(self.edges):
            if i[0] == node or i[1] == node:
                self.edges.remove(i)

    def addEdge(self, edge):
        start, goal, cost = edge
        self.edges.append([start, goal, int(cost)])

    def deleteEdge(self, edge):
        for i in list(self.edges):
            if i[0] == edge[0] and i[1] == edge[1]:
                self.edges.remove(i)

    def display(self):
        for i in self.nodes:
            print(str(i), end=" ")
            for edge in self.edges:
                if edge[0] == i:
                    print(f"{edge[1]} (cost={edge[2]})", end=" ")
            print()

    # ---------------- BFS ----------------
    def bfs(self, start, goal):
        visited = []
        fringe = [start]
        print("Initial fringe:", fringe)

        while fringe:
            curr = fringe.pop(0)
            print(curr)
            if curr == goal:
                print("Goal node found!")
                print("Visited nodes:", visited + [curr])
                return
            if curr not in visited:
                visited.append(curr)
                for edge in self.edges:
                    if edge[0] == curr and edge[1] not in visited and edge[1] not in fringe:
                        fringe.append(edge[1])
            print("Fringe after processing node", curr, ":", fringe)

        print("Goal node NOT found!")
        print("Visited nodes:", visited)

    # ---------------- DFS ----------------
    def dfs(self, start, goal):
        visited = []
        stack = [start]
        fringe = [start]
        print("Initial fringe:", fringe)

        while stack:
            current = stack.pop()
            print(current)
            if current == goal:
                print("Goal node found!")
                print("Visited nodes:", visited + [current])
                return
            if current not in visited:
                visited.append(current)
                children = [edge[1] for edge in self.edges
                            if edge[0] == current and edge[1] not in visited and edge[1] not in stack]
                for child in reversed(children):
                    stack.append(child)
                    fringe.append(child)
            print("Fringe after processing node", current, ":", fringe)

        print("Goal node NOT found!")
        print("Visited nodes:", visited)

    # ---------------- UCS ----------------
    def ucs(self, start, goal):
        visited = []
        queue = [(start, 0, [start])]
        fringe = [start]
        print("Initial fringe:", fringe)

        while queue:
            # find node with minimum cost
            min_index = 0
            for i in range(len(queue)):
                if queue[i][1] < queue[min_index][1]:
                    min_index = i
            current, cost, path = queue.pop(min_index)
            print(current)
            if current == goal:
                print("Goal node found!")
                print("Visited nodes:", visited + [current])
                print("Final path:", path)
                print("Total cost:", cost)
                return
            if current not in visited:
                visited.append(current)
                for edge in self.edges:
                    if edge[0] == current and edge[1] not in visited:
                        queue.append((edge[1], cost + edge[2], path + [edge[1]]))
                        fringe.append(edge[1])
            # show fringe like BFS/DFS (nodes only)
            print("Fringe after processing node", current, ":", fringe)

        print("Goal node NOT found!")
        print("Visited nodes:", visited)


# ---------------- Menu-driven program ----------------
if __name__ == '__main__':
    graph = Graph()
    print("1.addnode\n2.deletenode\n3.addedge\n4.deleteedge\n5.display\n6.bfs\n7.dfs\n8.ucs\n")
    while True:
        n = int(input("Enter choice: "))
        if n == 1:
            node = input("Enter node to insert: ")
            graph.addNode(node)
        elif n == 2:
            node = input("Enter node to delete: ")
            graph.deleteNode(node)
        elif n == 3:
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            cost = input("Enter cost: ")
            graph.addEdge([start, goal, cost])
        elif n == 4:
            start = input("Enter start node: ")
            goal = input("Enter the goal node: ")
            graph.deleteEdge([start, goal])
        elif n == 5:
            graph.display()
        elif n == 6:
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.bfs(start, goal)
        elif n == 7:
            start = input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.dfs(start, goal)
        elif n == 8:
            start =input("Enter start node: ")
            goal = input("Enter goal node: ")
            graph.ucs(start, goal)


