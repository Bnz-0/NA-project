#!/bin/env python3
from utils import *
import matplotlib.pyplot as plt
import graph_tool.all as GT

if len(sys.argv) < 2:
    print("Usage: ./assignment1.py <path_to_the_graph>")
    sys.exit(0)

TOP=10
g = get_graph()

print(f"--- Graph {'directed' if g.is_directed() else 'undirected'} ---")

N = g.num_vertices()
print(f"N = {N}")
L = g.num_edges()
print(f"L = {L}")

## diameter
d = diameter(g)
print(f"diameter = {d}")

## <k>
avg_degree = L/N if g.is_directed() else 2*L/N
print(f"<k> = {avg_degree}")

## density
p = avg_degree/(N-1)
print(f"p  = {p}")

## global clustering
gc = GT.global_clustering(g)[0]
print(f"gc = {gc}")

## average shortest path
avg_sp = avg_shortest_path(g)
print(f"avg shortest path = {avg_sp}")

## giant component size
gcs = giant_component_size(g)
if g.is_directed(): print(f"biggest strong component size = {gcs}")
else: print(f"giant component size = {gcs}")

##########
# Degree #
##########
degrees = g.get_total_degrees(g.get_vertices())

plt.figure(figsize=(14, 6))
plt.title("Degree distribution")
plt.ylabel('#Nodes')
plt.xlabel('#Connections (in+out)')
plt.plot(distribution(degrees))
plt.savefig(f"img/degree_dist.png", format='png')
plt.close()

print(f"top {TOP} degree nodes: {get_top(degrees, TOP)}")

## in-degree
degrees = g.get_in_degrees(g.get_vertices())

plt.title("In-degree distribution")
plt.ylabel('#Nodes')
plt.xlabel('#Connections')
plt.plot(distribution(degrees))
plt.savefig(f"img/in_degree_dist.png", format='png')
plt.close()

## out-degree
degrees = g.get_out_degrees(g.get_vertices())

plt.title("out-degree distribution")
plt.ylabel('#Nodes')
plt.xlabel('#Connections')
plt.plot(distribution(degrees))
plt.savefig(f"img/out_degree_dist.png", format='png')
plt.close()

del degrees

########
# Rank #
########
rank = GT.pagerank(g).get_array()

plt.title("Rank distribution")
plt.ylabel('#Nodes')
plt.xlabel('Rank')
plt.bar(*float_distribution(rank, 40), width=(max(rank)-min(rank))/50)
plt.savefig(f"img/rank_dist.png", format='png')
plt.close()

print(f"top {TOP} rank nodes: {get_top(rank , TOP)}")
del rank

###############
# Betweenness #
###############
betweenness = GT.betweenness(g)[0].get_array()

plt.title("Betweenness distribution")
plt.ylabel('#Nodes')
plt.xlabel('Betweenness coefficient')
plt.bar(*float_distribution(betweenness, 40), width=(max(betweenness)-min(betweenness))/50)
plt.savefig(f"img/betweenness_dist.png", format='png')
plt.close()

print(f"top {TOP} betweenness nodes: {get_top(betweenness, TOP)}")
del betweenness

#############
# Closeness #
#############
closeness = GT.closeness(GT.extract_largest_component(g), norm=False, harmonic=True).get_array()

plt.title("Closeness distribution")
plt.ylabel('#Nodes')
plt.xlabel('Closeness coefficient')
plt.bar(*float_distribution(closeness, 40), width=(max(closeness)-min(closeness))/50)
plt.savefig(f"img/closeness_dist.png", format='png')
plt.close()

print(f"top {TOP} closeness nodes: {get_top(closeness, TOP)}")
del closeness

##############
# Clustering #
##############
clustering = list(GT.local_clustering(g))

plt.title("Clustering distribution")
plt.ylabel('#Nodes')
plt.xlabel('Local clustering coefficient')
plt.bar(*float_distribution(clustering, 40), width=(max(clustering)-min(clustering))/50)
plt.savefig(f"img/clustering_dist.png", format='png')
plt.close()

print(f"top {TOP} local clustering nodes: {get_top(clustering, TOP)}")
del clustering


draw(g, 'deg', output='network.pdf', vertex_size=5, edge_pen_width=1, output_size=(1000,1000))
