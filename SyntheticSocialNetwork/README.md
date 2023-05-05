# Syntheic Social Networks

Description: Create a synthetic social network (graph) in python.


### Notes

 - The quickest way to find a graph for dataset evaluation is through synthetic graphs. The alternative is to collect/scrape actual graph datasets which takes time and can run into issues with usage, sharing, and privacy policies.
 - Benefits to synthetic graphs:
     - Convenience
     - No issues around privacy/data restrictions
     - Control graph size & data format
 - Synthetic graphs are constructed with graph generative models. Three of the more well know models are as follows:
     - Erdös-Rényi model
         - Start with a predefined set of nodes, say, N. Add the edges between nodes using a probability to generate a graph. The probability is fixed, and it is the same for all pairs of nodes in the graph. Hence, a higher probability makes a dense graph and a lower probability a sparse one. This is a simple model and does not come close to a real-world graph.
     - Watts-Strogatz model
         - This is a way of generating graphs with a small-world property. In this context, a small-world is defined as something that has a small path length and a high clustering coefficient.
             - Path length: The measure of distance between two nodes in a graph. The shorter the path length, the closer the nodes are to each other.
             - Clustering coefficient: It measures how tightly a node’s neighbors are connected to each other.
         - Start with a regular grid-like structure with a fixed number of nodes. Connect the edges from a node to its nearest neighbors. It uses a rewiring probability which means that some edges are randomly removed from a place and added elsewhere.
         - It is used to model real-world networks, which are instances of small-world like social networks and transportation networks.
     - Barabasi-Albert model
         - This graph generative model follows the “rich get richer” principle. The model connects new nodes to existing nodes that already have more connections. It causes the development of a few highly connected nodes and several poorly connected nodes in the graph. It is used in modeling scale-free networks like the internet and social networks.
 - The networkx library in python has the above generative models implemented, making it ideal for generating synthetic network graphs quickly.


### References

 - Main [Medium article](https://towardsdatascience.com/how-to-create-a-synthetic-social-network-using-python-eff6451cab14)
 - Supplimental [Medium article](https://medium.com/pragmatic-programmers/generate-synthetic-networks-f19186673ec6)
 - Faker [Pypi](https://pypi.org/project/Faker/)
 - Faker [GitHub](https://github.com/joke2k/faker)
 - Faker [Documentation](https://faker.readthedocs.io/en/master/)
 - Networkx [Documentation](https://networkx.org/documentation/stable/reference/index.html)
     - [Graph FileIO](https://networkx.org/documentation/stable/reference/readwrite/index.html)
     - [Erdös-Rényi](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.erdos_renyi_graph.html)
     - [Watts-Strogatz](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.watts_strogatz_graph.html)
     - [Barabasi-Albert](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.barabasi_albert_graph.html)
     - [Relabel Nodes](https://networkx.org/documentation/stable/reference/relabel.html)