import graph_tool.all as gt

g = gt.Graph().set_directed(False)
assert g.is_directed() == False

g.add_vertext()
