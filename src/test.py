from graph_tool.all import *

g = Graph()
ug = Graph(directed=False)
ug = Graph()
ug.set_directed(False)
assert ug.is_directed() == False
v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)
graph_draw(g, vertex_text=g.vertex_index, output="/logs/two-nodes.pdf")
