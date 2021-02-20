#!/bin/env python3
from utils import *
import graph_tool as GT
from graph_tool.draw import graph_draw, graphviz_draw
from graph_tool.generation import random_graph, price_network
from graph_tool.clustering import local_clustering, global_clustering
from graph_tool.centrality import betweenness, pagerank
import random as R
import math
import matplotlib.pyplot as plt
import time

if len(sys.argv) < 4:
    print("Usage: ./assignment2.py <#nodes> <protect%> <path_to_the_graph>")
    sys.exit(0)

class NodeProtected(Exception): pass

def std_rand_deg(N, p):
	"Chose the degree for each of `N` vertex based on a probability `p`"
	def f():
		n=0
		for _ in range(N):
			n += 1 if R.random() < p else 0
		return n
	return f


def pow_low(gamma):
	# "the number of node having k edges follow a power-low dist."
	# so to select the degree of each node just sample the points using the inverse function
	# NB: this sample in [0,1) because, by definition, k start from 1 (i.e. there isn't node with k = 0)
	return lambda: R.random()**(-1/gamma)


def hierarchical_graph(N, deg_sampler) -> GT.Graph:
	#NB: it have cluster coefficient always 0
	g = GT.Graph(directed=False)
	vertices = [g.add_vertex()] ; N-=1
	while(N > 0 and len(vertices) > 0):
		v = vertices.pop()
		deg = round(deg_sampler())
		for _ in range(deg):
			new_v = g.add_vertex() ; N-=1
			g.add_edge(v, new_v)
			vertices.insert(0, new_v)
			if N <= 0: break
	return g

class Sim:
	## WARN ##
	# for performance reasons, this methods uses a "static approach" to select the next vertex to remove,
	# which means that the measurements will be calculate only once (on the initial graph)
	# instead re-calculating it every time.
	## WARN 2 ##
	# Due to graph_tool's data structure (which didn't preserve the vertices id)
	# this methods works only if the function remove_vertex() use the "fast" flag set to True
	# (https://graph-tool.skewed.de/static/doc/graph_tool.html?highlight=remove#graph_tool.Graph.remove_vertex)

	n_protected = 0

	@staticmethod
	def attack(g: GT.Graph, attack_strategy, protection_strategy = lambda g, nodes, n_protected: set()):
		nodes = attack_strategy(g)
		protected = protection_strategy(g, nodes, Sim.n_protected)
		giant_component_history = [giant_component_size(g)]

		while giant_component_history[-1] > 1:
			try:
				g.remove_vertex(Sim.get_best(nodes, protected), fast=True)
				giant_component_history.append(giant_component_size(g))
			except NodeProtected: # the node is protected, the giant component size remains the same
				giant_component_history.append(giant_component_history[-1])
			except IndexError:
				break # no more removable vertex
			print(f"{g.num_vertices()} nodes remain ", end='\r')
		
		print('')
		return giant_component_history
	
	@staticmethod
	def get_best(nodes, protected = set()):
		# Get the best value in nodes and removes it following the remove_vertex TODO
		i_max = i_of_max(nodes)
		if nodes.id_of(i_max) in protected:
			nodes[i_max] = -1
			raise IndexError() if all((-1 == n for n in nodes)) else NodeProtected()
		nodes.remove(i_max)
		return i_max

	#NB: this should work because the id of the nodes is always the index in the array. Doesn't matter which function you use to get those
	
	@staticmethod
	def deg_attack(g: GT.Graph):
		return IdNodes(g.get_total_degrees(g.get_vertices()))

	@staticmethod
	def clu_attack(g: GT.Graph):
		lc = IdNodes(list(local_clustering(g)))
		if all(c == 0.0 for c in lc):
			for i in range(len(lc)):
				lc[i] = R.random()
			print("!!! clu_attack randomized !!!")
		return lc

	@staticmethod
	def deg_protection(g: GT.Graph, nodes, n_protected):
		return {nodes.id_of(n) for n in i_of_bests(Sim.deg_attack(g), n_protected)}
	
	@staticmethod
	def clu_protection(g: GT.Graph, nodes, n_protected):
		lc = list(local_clustering(g))
		if all(n == 0.0 for n in lc):
			print("!!! clu_protection randomized !!!")
			return set(R.sample(range(len(lc)), n_protected))
		return {nodes.id_of(n) for n in i_of_bests(lc, n_protected)}

	@staticmethod
	def rank_protection(g: GT.Graph, nodes, n_protected):
		return {nodes.id_of(n) for n in i_of_bests(IdNodes(list(pagerank(g))), n_protected)}


N = int(sys.argv[1]) # number of nodes

print("n_prot", Sim.n_protected)

legend = ["No protection", "Degree protection", "Cluster protection", "Rank protection"]

for name, gg in ( # lazy graphs tuple
	("graph_A", lambda: random_graph(N, pow_low(2.5), model="configuration", random=True, directed=False)),
	("graph_B", lambda: hierarchical_graph(N, lambda: R.randint(1,4))),
	[("graph_real_undirected", lambda: get_graph(3))]
):
	print(f"---------- {name} ----------")
	t = time.time()
	g = gg()
	Sim.n_protected = int(g.num_vertices()*float(sys.argv[2]))
	print("protected nodes: ", Sim.n_protected)
	print(f"Drawing {name}")
	graph_draw(g, output=f"img/{name}.png", output_size=(1000,1000))

	#################
	# Degree attack #
	#################

	plt.title("Network under degree attack")
	plt.ylabel('Giant component size')
	plt.xlabel('#Iterations')

	print("Degree attack simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.deg_attack))

	print("Degree attack with degree protection simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.deg_attack, Sim.deg_protection))
	
	print("Degree attack with cluster protection simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.deg_attack, Sim.clu_protection))
	
	print("Degree attack with rank protection simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.deg_attack, Sim.rank_protection))

	plt.legend(legend)
	plt.savefig(f"img/{name}_deg.png", format='png')

	plt.close()

	##################
	# Cluster attack #
	##################

	plt.title("Network under cluster attack")
	plt.ylabel('Giant component size')
	plt.xlabel('#Iterations')

	print("Cluster attack simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.clu_attack))

	print("Cluster attack with degree protection simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.clu_attack, Sim.deg_protection))
	
	print("Cluster attack with cluster protection simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.clu_attack, Sim.clu_protection))

	print("Cluster attack with rank protection simulation...")
	plt.plot(Sim.attack(g.copy(), Sim.clu_attack, Sim.rank_protection))

	plt.legend(legend)
	plt.savefig(f"img/{name}_clu.png", format='png')
	plt.close()

	print("  --> Time elapsed: {:.3f}s".format(time.time()-t))
