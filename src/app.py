import graph_tool.all as gt

from TwitterClient import TwitterClient

TEST_USERNAME = 'Luludc17'

tw = TwitterClient()
tw.authenticate()

test_user = tw.get_user(TEST_USERNAME)
test_user.friends = tw.get_user_friends(test_user.name)

print(test_user.friends)
print(f'len : {len(test_user.friends)}')


"""g = gt.Graph()
g.set_directed(False)

user_vertex = g.add_vertex()
friend_vertices = g.add_vertex(len(test_user.friends))
fof_vertices = []
for f in test_user.friends:
    fof_vertices.append(g.add_vertex(len(f.friends)))

v_prop = g.new_vertex_property("string")
v_prop[user_vertex] = TEST_USERNAME

for vertex, index in zip(friend_vertices, range(len(test_user.friends))):
    v_prop[vertex] = test_user.friends[index].name[:4]
    g.add_edge(vertex, user_vertex)

gt.graph_draw(g, vertex_text=v_prop,
              vertex_font_size=10, output="logs/two-nodes.pdf")
"""
