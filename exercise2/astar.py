class Graph:
   def __init__(self):
      self.nodes=[]
      self.edges=[]
   def addNodes(self, node):
      self.nodes.append(node)
   def deleteNode(self,node):
      self.nodes.remove(node)
      for i in self.edges:
	 if i[0] == node or i[1] == node:
	    self.edges.remove(i)
   def addEdge(self, edge):
      self.edges.append(edge)
   def deleteEdge(self, edge):
      newedge = []
      for e in self.edges:
	 if not (e[0] == edge[0] and e[1] == edge[1] and e[2] == edge[2]):
	    newedge.append(e)
      self.edges = newedge
   def display(self):
      for i in self.nodes:
	 print(i + '->' , end = " ");
	 for j in self.edges:
	    if j[0] == i:
	       print(f"
