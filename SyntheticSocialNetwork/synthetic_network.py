# synthetic_network.py
# Create a synthetic social network graph using a few algorithms.
# Source: https://towardsdatascience.com/how-to-create-a-synthetic-
#   social-network-using-python-eff6451cab14
# Python 3.7
# Windows/MacOS/Linux


import json
from faker import Faker
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def main():
	# Demonstrate how to generate a synthetic graph in networkx using
	# each of the three models (and see how they look). Note that
	# adjusting the hyperparameters generates drastically different
	# graphs.
	
	# Erdos-Renyi model.
	G1 = nx.erdos_renyi_graph(n=50, p=0.2, seed=42)

	# Watts-Strogatz model.
	G2 = nx.watts_strogatz_graph(n=50, k=5, p=0.4, seed=42)

	# Barabasi-Albert model.
	G3 = nx.barabasi_albert_graph(n=50, m=5, seed=42)

	# Plot the graphs side by side.
	fig, ax = plt.subplots(1, 3, figsize=(15, 5))

	# Add title to each plot.
	ax[0].set_title('Erdos-Renyi')
	ax[1].set_title('Watts-Strogatz')
	ax[2].set_title('Barabasi-Albert')
	nx.draw(G1, ax=ax[0])
	nx.draw(G2, ax=ax[1])
	nx.draw(G3, ax=ax[2])
	# plt.show() # Shows graph in a window.
	plt.savefig('./General_Graphs.png') # Saves graph to file.

	# For a social network, we would like to add node features and node
	# labels. This can be done using faker python library, which 
	# generates fake data such as names.

	# Initialize faker & names list.
	faker = Faker()
	names = []

	# Generate 10 unique names.
	for i in range(10):
		# Generate a random name.
		name = faker.name()
		# Append the name to the list.
		names.append(name)

	# Barabasi-Albert model.
	G = nx.barabasi_albert_graph(n=10, m=5, seed=42)

	# Add the names to the graph.
	mapping = {i: names[i] for i in range(len(names))}
	G = nx.relabel_nodes(G, mapping)

	fig, ax = plt.subplots(figsize=(3, 2), dpi=300)
	nx.draw(G, with_labels=True, node_size=50,width=0.1, font_size=3.5)
	# plt.show() # Shows graph in a window.
	plt.savefig('./Synthetic_Social_Network_Graph.png') # Saves graph to file.

	# The synthetic social network now has labels. Each node represents
	# a person, and their name acts as the node label.
	# It is possible to generate other node attributes like age, sex, 
	# and occupation of each person in the social network and update 
	# the graph.
	# Now we have a fully loaded synthetic social network that can be 
	# used to perform graph analytic tasks.

	# You can also save & load a graph with networkx.
	with open("fake_network.json", "w+") as f:
		json.dump(nx.node_link_data(G), f, indent=4)

	with open("fake_network.json", "r") as r:
		loaded_graph = nx.node_link_graph(
			json.load(r)
		)

	# Compare the loaded graph with the original (compare the JSON
	# serialized data, not the actual raw objects).
	print(f"Loaded and original graphs match: {nx.node_link_data(G) == nx.node_link_data(loaded_graph)}")

	# Exit the program.
	exit(0)


if __name__ == '__main__':
	main()