import graph_tool as GT, sys
from collections import OrderedDict
from graph_tool.draw import graph_draw, sfdp_layout
import matplotlib, re
import copy

INF_INT=2147483647

def frange(start, stop, step):
	while start < stop:
		yield start
		start += step

def i_of_max(l):
	return max(range(len(l)), key=l.__getitem__)

def i_of_bests(l, n):
	cl = copy.deepcopy(l)
	bests = []
	for _ in range(n):
		bests.append(i_of_max(cl))
		cl[bests[-1]] = -1
	return bests

def get_graph(arg_n = 1):
	file = sys.argv[arg_n] if len(sys.argv) > arg_n else None
	if file is None:
		return False
	elif file.split('.')[-1] == 'txt':
		directed = sys.argv[arg_n+1].lower() == "d"
		return load_graph_from_raw(file, directed)
	else:
		return GT.load_graph(file)

def load_graph_from_raw(path: str, directed) -> GT.Graph:
	# it's read an "adjacency graph" representation
	g = GT.Graph(directed=directed)
	with open(path, 'r') as f:
		for edge in (re.split(r"\s", l.strip('\n')) for l in f.readlines() if l[0] != '#'):
			g.add_edge(source=int(edge[0]), target=int(edge[1]), add_missing=True)
	return g

def distribution(x):
	_min, _max = min(x), max(x)
	dist = [0]*int(1+_max-_min)
	for d in x: dist[d-_min]+=1
	return dist

def float_distribution(x, n_ranges):
	highest, lowest = max(x), min(x)
	dist = OrderedDict({r: 0 for r in frange(lowest, highest, (highest-lowest)/n_ranges)})
	ranges = list(dist.keys())
	for d in x:
		i = ranges[-1]
		for r in ranges:
			if r > d:
				i = r
				break
		dist[i] += 1
	return zip(*dist.items())

def get_top(data, top):
	"returns a list of tuple (index, value) of the top `top` (i.e. max) value in `data`"
	if len(data) == 0: return []
	top_data = [(0,data[0])]
	for i,v in enumerate(data):
		if top_data[-1][1] < v:
			top_data.append((i,v))
			top_data.sort(key=lambda x: x[1], reverse=True)
			if len(top_data) > top:
				top_data.pop()
	return top_data

def diameter(g: GT.Graph):
	d=0
	if g.num_vertices() < 10_000:
		d = GT.topology.shortest_distance(g) #NB: allocate memory, isn't an iterator!
		d = max((max(_d, key=lambda x: x if x!=INF_INT else -1) for _d in d))
	else:
		d = GT.topology.pseudo_diameter(g)[0]
	return d

def avg_shortest_path(g: GT.Graph):
	if g.num_vertices() < 10_000:
		d = GT.topology.shortest_distance(g) #NB: allocate memory, isn't an iterator!
		return sum((max(_d, key=lambda x: x if x!=INF_INT else -1) for _d in d))/(g.num_vertices())
	else:
		return None #TODO

def giant_component_size(g: GT.Graph):
	return GT.topology.extract_largest_component(g).num_vertices()

def draw(g: GT.Graph, color_mode=None, **kwargs):
	if color_mode is None:
		graph_draw(g)
	else:
		vc=None
		if color_mode == 'deg':
			vc = g.degree_property_map('total')
		graph_draw(g, vertex_fill_color=vc, vcmap=matplotlib.cm.gist_heat_r, **kwargs)

class IdNodes:
	def __init__(self, nodes):
		self.nodes = list(zip(nodes, range(len(nodes))))

	def id_of(self, i):
		return self.nodes[i][1]

	def remove(self, i):
		"removes the i-th node following the remove_vertex() behavior"
		self.nodes[i] = self.nodes[-1]
		del self.nodes[-1]

	def __getitem__(self, i):
		return self.nodes[i][0]

	def __setitem__(self, i, v):
		self.nodes[i] = (v, self.id_of(i))

	def __len__(self):
		return len(self.nodes)
