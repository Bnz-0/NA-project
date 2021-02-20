#!/bin/env python3
from utils import *
import random as R, sys
import graph_tool as GT
from graph_tool.draw import graph_draw, graphviz_draw

if len(sys.argv) < 5:
    print("Usage: ./assignment3.py <img_prefix> <#initial_blue_node> <payoff> <network>")
    sys.exit(0)


FILE_NAME, nr, p = sys.argv[1:4]
nr, p = int(nr), float(p)

N = None # number of nodes
g = get_graph(4)
if not g:
	N = 50
	g = GT.generation.price_network(N, gamma=1, directed=False)
else:
	N = g.num_vertices()
	g = GT.topology.extract_largest_component(g, directed=False) # extract only the giant component

# NB: I assume that the payoff is the same for each player (all the nodes)
# so the "second player" is omitted
payoff_matrix = [
	[1, 0],
	[0, p]
]
q = payoff_matrix[1][1] / (payoff_matrix[0][0] + payoff_matrix[1][1])

print(f"Using:\n\tq = {q}\n\t#blue nodes = {nr} ({nr/N*100}%)\n\tgraph {'directed' if g.is_directed() else 'undirected'}")

nodes_adoption = [0]*N # all nodes adopt 0

# graph setup #
plot_color = g.new_vertex_property('vector<double>')
g.vertex_properties['plot_color'] = plot_color

# random blu nodes
for i in R.sample(list(range(N)), nr):
	nodes_adoption[i] = 1

def calc_adoption(node: int):
	p = 0
	neighbors = g.get_in_neighbors(node) if g.is_directed() else  g.get_all_neighbors(node)
	for d in neighbors:
		if nodes_adoption[d] == 0:
			p += 1
	if len(neighbors) == 0:
		return nodes_adoption[node]
	p /= len(neighbors)
	return 0 if p >= q else 1


## start the contagion ##
node_changes = True
step = 1
v_pos = None
while node_changes:
	# print/show the graph
	if FILE_NAME != "!":
		for v in g.vertices():
			plot_color[v] = (1,0,0,1) if nodes_adoption[int(v)] == 0 else (0,0,1,1)
		v_pos = graph_draw(g, pos=v_pos, vertex_fill_color=g.vertex_properties['plot_color'], output=FILE_NAME+"_"+str(step)+".png")
	step += 1

	# calculates the diffusion
	node_changes = False
	for node in g.get_vertices():
		adoption = calc_adoption(node)
		if adoption != nodes_adoption[node]:
			node_changes = True
			nodes_adoption[node] = adoption


red_p = len([0 for x in nodes_adoption if x==0])/N*100
blue_p = 100-red_p
print(f"steps: {step}\nred =\t{100-nr/N*100}% --> {red_p}%\nblue =\t{nr/N*100}% --> {blue_p}%")
