**Matteo Benzi** — S4376824

# 2st assignment report

#### Technical notes:

To avoid a giant complexity in the attack simulation **the algorithm select which node attack and protect only once** (at the beginning), which means that doesn't matter how the network evolves, the nodes convoluted will remain the same.

This approach is not "the best" or "the worst", but is just a way to made an attack or to protect the nodes. It's reasonable imagine a situation in which you have to decide which nodes attack/protect only before, maybe because when the attack starts you cannot stop it and measure again the status of the network.

A different approach could be to _pre-calculate_ the status after each node removal and _pre-chose_ the next one relying on the expected status, but depending on which nodes are protected this strategy could miserably fails.

Like the attack, also **the protection is made preselecting the N nodes to protect**.

## Part 1 (alternative)

Both network have 10000 nodes and the protection is made saving the best 500 (5%) nodes of according to a certain metrics.

### Graph A
> A network with N = 10000 nodes generated with the configuration model (https://en.wikipedia.org/wiki/Configuration_model) and power-law degree distribution with γ = 2.5

![][graph_A]

The network is sparse, in fact there isn't a real giant component but simply a biggest component which is pretty small considering the number of nodes.

|Degree attack|Cluster attack|
|-|-|
|![][graph_A_deg]|![][graph_A_clu]|

For this network the **degree attack** is the most destructive, with few steps the size of the giant component falls down near to 0.
Also **protecting the nodes with high cluster coefficient doesn't help**. This is probably because this network doesn't have any particular cluster, so the clusters are low and the coefficient is meaningless.

Protecting the vertices with highest rank and highest degree had some effects. After ~2000 steps the size decrease linearly but before that the decrease rate is very steep, the fact that  they save more nodes is because the first nodes to be removed are the same that those approach protects.

> We have also to remember that this network is undirected, so the degree and the rank is more related than a directed one.

Anyway **this network is very weak against a degree attack**, also protect it following the same attack doesn't help.

Instead against the **cluster attack** seems to be a bit more strong. What is sure is that, at least for this network, the **cluster protection approach** is useless: after the first 500 steps the trend is the same as the one without protection.

The other 2 protection approaches make the trend, except for some falls, linear. So in general for this network **the most important nodes are those ones with high degree.**

### Graph B
> A network with N = 10000 nodes generated with the hierarchical model (https://en.wikipedia.org/wiki/Hierarchical_network_model). The degree of each node is a random number in the interval [1; 4]

![][graph_B]

Unlike the graph A, this one have a single giant component. The degree distribution is linear, so to generate a strong difference from the previous graph.

|Degree attack|Cluster (random) attack|
|-|-|
|![][graph_B_deg]|![][graph_B_clu]|

Also here the best attack is the **degree** one. Only protecting them the giant component size survives until ~2000 steps. Any other strategy is useless.

> We have to remember that the size of the giant component of this network is much bigger than the previous one (10000 vs ~1200 ), so here the _decrease rate_ is much more steep.

The degree protection is better than the others, but is still basically useless here, so seems that **this kind of network cannot be protected against a degree attack.**

For the clustering attack there is a problem: **this network do not have any cluster**, so basically a cluster attack becomes a random one.

This graph is weak also against a random attack, the cluster protection (which is turned into a random protection) as expected doesn't gives any help. Also protecting the best rank on average is useless, and at this point I can assume that **the rank is not a good metric for this network**.

So with both attack the only strategy that does something is to protect the nods with highest degree, which make this approach the best for this network, but in general is very weak against an attack.

## Part 2

![][graph_real]

Doing the same (protecting the 5% of the nodes) with the real network generate this results:

|Degree attack|Cluster attack|
|-|-|
|![][graph_real_deg]|![][graph_real_clu]|

> The giant component starts form ~2000 because this is a directed graph, so **it's not the giant component but the largest strongly connected component size.**

Again, the degree attack (which is hide under the green graphic) is the best approach against this network, but it's immediately visible that **this network isn't really stronger than the others two**.

**In this network finally the local clustering coefficient gains importance**, but the attack is far from the degree one and the protection is more or less like to not have it.

Like in the graph A, also here the rank and the degree protection strategies seems to be correlated but the degree do a better job also with this one.

**So this network is in general a bit more robust but still not really defensible.**

### Real graph treated as undirected

The real graph doesn't show any particular resistance against the attacks, so I was wandering what would happen if the graph is undirected like the first 2.

|Degree attack|Cluster attack|
|-|-|
|![][graph_real_undirected_deg]|![][graph_real_undirected_clu]|

Here we can see the real strength of this network: **the cluster attack is very weak** and generates a linear trend, with this attack all the protection strategies are more or less equivalent. The fact that against this graph, where the clustering coefficient have more meaning than the other 2, this attack is worthless could be a sing that in general this approach is not a good one neither to attack nor to protect a graph.

The degree attack still remains a strong attack, but nothing compared to the previous ones. An interesting aspect is that the degree protection still remain one of the best approach to defend, but here the best one is the rank strategy.

## Conclusion

To sum up, for all the 3 networks the best attack you can made is to remove the node with the highest degree. The cluster attack in general seems weak and depending on the kindness of the network make a clustering attack is equivalent to make a random one.

From the protection point of view instead there isn't a real winner, but we have a loser: protecting the node with highest local clustering coefficient never does a better job than the other strategies.
Instead both rank and degree protection made a similar job except for the graph B, where the rank is the wrongest choice. **Protecting the node with highest degree seems to be in general a better choice**, but 3/4 networks are too few to make a final conclusion.

[graph_A]: img/graph_A.png
[graph_A_deg]: img/graph_A_deg.png
[graph_A_clu]: img/graph_A_clu.png
[graph_B]: img/graph_B.png
[graph_B_deg]: img/graph_B_deg.png
[graph_B_clu]: img/graph_B_clu.png
[graph_real]: img/graph_real.png
[graph_real_deg]: img/graph_real_deg.png
[graph_real_clu]: img/graph_real_clu.png
[graph_real_undirected_deg]: img/graph_real_undirected_deg.png
[graph_real_undirected_clu]: img/graph_real_undirected_clu.png

