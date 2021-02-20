

**Matteo Benzi** — S4376824

# 1st assignment report

The _real network_ I selected for the assignments came from a **peer-to-peer file sharing network**, in particular the [Gnutella peer-to-peer network][1], collected on august 2002.

It's a **directed graph** generated from a snapshot of an unspecified p2p network which use the _Gnutella protocol_. The nodes are the hosts and the edges are the connections the hosts made between each other to send/receive data.

![][img_net]

## Metrics

|Metric|Value|
|---|---|
|Number of nodes|`6301`|
|Number of edges|`20777`|
|Diameter|`20`|
|Average degree|`3.297`|
|Density|`0.0005`|
|Global clustering|`0.021`|
|Average shortest path|`5.426`|
|Giant component size|`6299`|
|Biggest strong connected component size|`2068`|

The _p2p-Gnutella_ is not a small one and it's also well connected, in fact it's almost a unique giant component (only 2 node are outside the giant component) and 1/3 of the network is string connected.

> the 2 node outside are not plotted above, but basically are `X -> Y`: only one is connected to the other.

The number of connection, instead, is not so high. The low density and the global clustering suggests that the network is sparse.

> **NB:** on the site where I got the network, it says that the graph is directed, but the measure was calculated by interpreting it as undirected. So the following measure values do not match the value on the source site.

## Degree distribution

![][img_deg_dist]

This is a very interesting degree distribution, it seems to follow a strong power low but between 10 and 20 there's an "anomalous" peak.

This peak could be explained in 2 way:

1. **It's a normal p2p network behavior**:  
	a p2p network serves mainly to share files or to create sessions between hosts. I didn't found the scope of this one, so could be a mixed one which make really hard to reason on what happens here.
	
	- **file sharing only**: if this is a "file sharing only" p2p, the **degree of a host is directly proportional to the number of files shared and the _request grade_ of the files**. This explain well the general distribution (a lot of hosts have few file with few _request grade_ and few hosts have a lot of file with high _request grade_), but it doesn't easily explain the peak.

		To explain it from a _social_ point of view, I'd tried to separate the hosts in 2 sub category: the **receivers** (who download files) and the **givers** (who share files).
		
		> Of course an host can play both the roles, but keep it simple :)

		Focusing on the **givers**, their degree distribution cold be a _power low_ because a lot of givers share the same few file and a small portion of them share a lot of file or few file with a very high _request grade_.  
		Instead, if we focus on the **receivers**, we may discover that usually they download files that a lot of **givers** have, so maybe on average they make ~15 connections. In terms of distribution this could be a _Gaussian_.

		Putting the **givers** and the **receiver** distribution together we obtain a distribution very like to the real one:

		![][peak_expl]

	- **hosts sessions only**: if it's a "sessions only" network the peak could be explained by two main usage: a lot of sessions by ~2 hosts and session of more hosts which on average is ~15 (imagine an online game with 15 player based on p2p), but is hard or impossible to explain the few hosts with a lot of connections. That's because when `x` hosts start a p2p session from the network point of view this means an `x-clique`, so in our network we should have, for example, a 97-clique which doesn't exists.

	  Also the fact that the previous measures suggest a small number of clusters put in crisis this theory.
	
	- **both**: a mixed p2p network maybe explain better the trend, where the peak is caused by _hosts sessions_ and the power low distribution by _file sharing_.
	
2. **It's caused by the algorithm**:  
	_Gnutella_ is a p2p protocol and depending on how the algorithm is implemented, the peak could be a wanted/unwanted behavior.

Going a bit deeper we can see that **probably the right hypothesis was the file sharing one**.

|                  In-degree                   |                  Out-degree                   |
| :------------------------------------------: | :-------------------------------------------: |
| ![][in_degree_dist] | ![][out_degree_dist] |

In fact **this 2 distribution are very similar to the receivers and the givers** supposed distribution.
What is wrong in the first assumption is that the distribution of givers follows the power-law and the receivers a Gaussian, but in the truth seems to be the contrary.

In fact **the in-degree distribution follows the power-law** and **the out-degree shows us the peak**, which means that the a huge number of givers share files with an average of 10 nodes and the receivers struggle to have more connections.

The out-degree suggests also that **under this trend could be an algorithm behavior**, because from 10 to 11 the number of nodes with this connections drop down form more than 1500 to near 0. So it appears that the algorithm/protocol put a sort of limit of out connections a host can made.

## Top nodes by metrics
|Node id|degree coefficient|Node id|rank|Node id|betweenness coefficient|Node id|Local cluster coefficient|Node id|Closeness coefficient|
|-:|:-|-:|-:|-:|:-|--|--|--|--|
|**123**|97|**367**|0.0024|**1317**|0.019|**506**|1.0|**5831**|0.202|
|**127**|95|**249**|0.0022|**3**|0.017|**702**|1.0|**2614**|0.192|
|**367**|94|**145**|0.0021|**146**|0.015|**3589**|1.0|**1382**|0.188|
|**424**|92|***264***|0.0020|**390**|0.014|**4223**|1.0|**5202**|0.186|
|**251**|91|  **266** | 0.0020 |**175**|0.014|**4278**|1.0|**2852**|0.185|
|***264***|91|  **123** | 0.0019 |**559**|0.012|**4321**|1.0|**1534**|0.184|
|**2646**|91|**127**|0.0019|**1534**|0.012|**5060**|1.0|**1675**|0.184|
|**427**|91|**122**|0.0019|**250**|0.012|**6287**|1.0|**4533**|0.183|
|**145**|90|**1317**|0.0018|**700**|0.010|**4022**|0.666|**786**|0.182|
|**249**|90|**5**|0.0018|***264***|0.010|**137**|0.333|**2718**|0.181|

> NB 1: the degrees are the sum of in and out degree
> 
> NB 2: the closeness coefficient were calculated using only the giant component and the harmonic formula

In the top 10 for various centrality measures there is nothing special, there are some common nodes sorting by degree and rank and the other metrics select mostly different nodes. If we have to chose a winner the node that appears most is the **264**: it have both good rank and high number of edges and appears in the top 10 of the betweenness.

Below I reported the distributions of the various coefficients. More or less also these follow a power-law distribution, except for the closeness:

| ![][rank_dist]      | ![][betweenness_dist] |
| -------------------------------------------- | ---------------------------------------------- |
| ![][closeness_dist] | ![][clustering_dist]  |

The interesting part is that the closeness distribution made a "bump" between 300 and 400 but have the great majority (more than 4000 nodes) with a very low coefficient (~0).
This "bump" deserves attention because the other distributions don't show anything related to the degree distribution's peak.

**The only distribution that not follows a power-law one is the out-degree and the closeness, are they related somehow?**

Remembering that "*Closeness measures the mean distance from a vertex to the other vertices*"  the "bump" in the closeness distribution make sense:
in the network there are a quite high number of node with a high out-degree, and those nodes can reach the other nodes in an easier way in respect to the others.

**But why the other distribution doesn't have this peak?**

The short answer is: **because the network is directed.**

Let's take the rank distribution as example where to reason about it:
the rank measure "_the probability to reach that node after x random jump_", and because we are in a directed graph the out-degree doesn't matter so much, so it's understandable that it follows the same distribution as the in-degree one.

The same reasoning is applicable to the betweenness and the clustering is quite "distant" from the degree distribution, it simply says that there are few and small clusters around the network. I don't see any meaningful relation between cluster and degree distribution in this network.

### Other considerations

However, knowing the nature of the graph, the fact that there are few cluster is somehow unexpected. In a p2p file sharing network the nodes make connections to shares a file, so I would have expected that "around" that file the partial owners (I mean a node that have only part of a file, so it must still download the missing parts but can already shares with other nodes) will generates a cluster between them, but this measure confirm that my assumption was wrong, or maybe this happens but for a very few nodes or for a small amount of time. Anyway in general seems that in this network the separation of the roles (givers and receivers) is remarkable, so a node tent to only shares or only get, and not made a 50-50.



[1]: https://snap.stanford.edu/data/p2p-Gnutella08.html
[img_net]: img/network.png
[img_deg_dist]: img/degree_dist.png
[peak_expl]: img/peak_explanation.png
[rank_dist]: img/rank_dist.png
[betweenness_dist]: img/betweenness_dist.png
[closeness_dist]: img/closeness_dist.png
[clustering_dist]: img/clustering_dist.png
[in_degree_dist]: img/in_degree_dist.png
[out_degree_dist]: img/out_degree_dist.png
