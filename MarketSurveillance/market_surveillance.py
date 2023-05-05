# market_surveillance.py
# Create a synethic social network graph using a few algorithms.
# Source: https://medium.com/@adityagandhi.7/network-analysis-and-
#   community-structure-for-market-surveillance-using-python-networkx-
#   65413e7b7fee
# Python 3.7
# Windows/MacOS/Linux


from collections import Counter
import community
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import pandas as pd
import networkx as nx


def main():
	# Introduction
	# Market Surveillance is an area within financial institutions 
	# which involves monitoring for market manipulation practices. 
	# Traditionally, a lot of work in this area used to monitor either 
	# trading or e-communications (chats/voice calls) in silos. This 
	# led to a huge amount of false alerts, leading to wastage of a 
	# large number of man-hours. Recently, compliance functions are 
	# catching up and attempting to analyze multiple variables 
	# simultaneously - this is due to the fact that with the influx of 
	# data science tools and increase in computing power, it is easier 
	# to derive insights from big data. So instead of monitoring either 
	# just trade data or just e-communication data in silos, the trend 
	# is slowly moving towards monitoring trade and e-communications 
	# both.
	# One of the roles of a data scientist is to look for use cases 
	# (moonshots) in different industries and try simulating the 
	# concept for finance. During a moonshot sessions, the article
	# authors came across an excellent article on Bloomberg related to 
	# surveillance expertise, conceptualized and implemented by 
	# Palantir Technologies for JP Morgan Chase. Palantir had developed
	# capabilities to scan through emails, browsing histories, GPS 
	# location using company owned smart phones, transcripts of phone 
	# conversations and employee badge timings.
	# (https://www.bloomberg.com/features/2018-palantir-peter-thiel). 
	# Reading through this article inspired the authors to attempt a 
	# moonshot and implement a proof-of-concept visualization/model to 
	# carry out holistic surveillance and identify network 
	# structure/communities in the data.


	# Background
	# Network Analysis and Graph Theory is already a known concept in 
	# areas of social networking, communication, organizational change 
	# management and recently in area of market surveillance. Network 
	# Analysis helps in visualizing multiple data points and drawing 
	# insights from a complex set of connections.
	# A quick background about the market surveillance space — Market 
	# Surveillance is a department within banks with an onus to curb 
	# market manipulation practices by the firm’s traders/clients. 
	# Old-school surveillance techniques always used variables such as 
	# threshold and the horizon period. This technique implied 
	# surveillance of financial transactions within a fixed time 
	# horizon and only for transaction amounts that were more than a 
	# certain threshold. This led to a large amount of false alerts and
	# traditionally compliance departments have spent a lot of 
	# man-hours in tackling false alerts. In addition, the false alert 
	# ratio used to be an input to the increasing/decreasing threshold 
	# of transactions to be monitored. With the advent of data science, 
	# there lies an opportunity to make this space more efficient. 
	# Keeping this aim in mind, the authors have attempted to not 
	# analyze trading or e-communication space separately, but to 
	# combine trading with chat data, and to perform this analysis, by 
	# combining multiple sources.
	# Insights can be drawn in either quantitative measures like 
	# centrality (degree, closeness or eigenvector) or network density,
	# community formation et al. via visual mapping.


	# Data Overview
	# The authors created an example of chat data which contains the 
	# information such as Inviter (person sending the chat), Invitee/s 
	# (person(s) receiving the chat), and also the Message Count 
	# (number of messages sent in the the conversation). Their data had
	# 130 participants, with 91 conversations. This is shown in the 
	# image below (along with the supporting Python code in next block):
	# Figure Dimensions
	value_height=9
	value_width=16
	matplotlib.rcParams['figure.figsize']=[12, 8]

	# Reading in the data for the Inviters and Invitees from the the Bloomberg Chat Data
	df = pd.read_excel('dataset.xlsx')

	# Creating a graph from a pandas dataframe
	G = nx.from_pandas_edgelist(df, 'Inviter', 'Invitee', 'MsgCount')
	for index, row in df.iterrows():
		G.add_edge(row['Inviter'], row['Invitee'])
		
	# Position nodes using Fruchterman-Reingold force-directed algorithm
	pos = nx.spring_layout(G)

	# Drawing the graph
	nx.draw_networkx_nodes(
		G, pos, with_labels=True, node_size=50, font_size=7,
		node_color='green', label='Participants'
	)
	nx.draw_networkx_edges(
		G, pos, with_labels=False, width=2.0, 
		label='Number of Messages'
	)
	plt.title(
		'Node Graph for Communications Data', fontsize=22, 
		fontname='Arial'
	)
	plt.box(on=None)
	plt.axis('off')
	plt.legend(bbox_to_anchor=(1, 0), loc='best', ncol=1)
	plt.savefig('base.png', dpi=400)

	# Additional metrics
	print("Total number of Edges=", len(G.edges()))
	print("Total number of Nodes=", len(G.nodes()))


	# Quantitative Metrics for Network Analysis
	# Centrality: A measure used to identify which nodes/traders are 
	# the biggest influencers of the network. The different types of 
	# centrality in analyzing the network are given as follows 
	# (Reference: https://sctr7.com/2013/06/17/adopting-analytics-
	# culture-6-what-information-is-gained-from-social-network-
	# analysis-6-of-7/):
	# -> Degree: Measures number of incoming connections
	# -> Closeness: Measures how quickly (minimum number of steps) can 
	#	one trader connect to others in the network
	# -> Eigenvector: Measures a trader’s connection to those who are 
	#	highly connected. A person with a high score will be someone 
	#	who is influencing multiple players (who in turn are highly 
	#	connected) and is exercising control behind the scenes.

	# Centrality Metrics

	# Calculating Centrality metrics for the Graph
	dict_degree_centrality = nx.degree_centrality(G)
	dict_closeness_centrality = nx.closeness_centrality(G)
	dict_eigenvector_centrality = nx.eigenvector_centrality(G)

	# Top 10 nodes with the largest values of degree centrality in 
	# descending order
	dict(Counter(dict_degree_centrality).most_common(10))

	# Top 10 nodes with the largest values of closeness centrality in 
	# descending order
	dict(Counter(dict_closeness_centrality).most_common(10))

	# Top 10 nodes with the largest values of eigenvector centrality in
	# descending order
	dict(Counter(dict_eigenvector_centrality).most_common(10))

	# Function to plot the graphs for each centrality metric
	matplotlib.rcParams['figure.figsize']= [24, 8]
	def draw(G, pos, lista, listb, measure_name):
		nodes=nx.draw_networkx_nodes(
			G, pos, node_size=100, cmap=plt.cm.viridis, 
			node_color=lista, nodelist=listb
		)
		nodes.set_norm(
			mcolors.SymLogNorm(linthresh=0.01, linscale=1)
		)
		edges=nx.draw_networkx_edges(G, pos)
		plt.title(measure_name, fontsize=22, fontname='Arial')
		plt.colorbar(nodes)
		plt.axis('off')

	plt.subplot(1,3,1)
	list_pos_values = []
	for i in nx.degree_centrality(G).values():
		list_pos_values.append(i)
		list_pos_keys=[]
	for i in nx.degree_centrality(G).keys():
		list_pos_keys.append(i)
	draw(G, pos, list_pos_values, list_pos_keys, 'Degree Centrality')

	# Based on the graphs above, the authors observe that some of the 
	# most influential participants are P1, P12, P16, P29, P44 and P63.


	# Algorithms for Community Detection for the Data
	# The article has concentrated on the visual representation of a 
	# community using different algorithms. Whilst quantitative 
	# measures have its own importance, a visual representation is 
	# strongly recommended in such areas as work can be easily 
	# integrated into popular charting tools available across banks. 
	# Visualization is very commonly used within the trading community 
	# to analyze trading patterns for a particular asset class and its 
	# comparison to benchmarks. The combined visualization of trade 
	# with chat data makes the exercise far more meticulous.
	# Imagine a scenario where a score to the number of chat messages 
	# which has been exchanged between two traders (nodes) and repeat 
	# this exercise for the complete network landscape. This score is 
	# referred to as modularity. If we try to form communities based on
	# connectivity and modularity and run the exercise for the 
	# landscape, we can oversee communities~ which essentially 
	# represent group of traders (nodes), whose exchange of messages 
	# among themselves is far more as compared to the community’s 
	# exchange with rest of the world. The purpose here is to find 
	# tightly knit communities of nodes which have rarer friendship 
	# ties between different communities.
	# Community detection algorithms can be of multiple types with 
	# varying levels of success. The authors have used three popular 
	# types of community detection algorithms to better understand the 
	# network:

	# Louvain Algorithm for Community Detection:
	# This algorithm works on the principle of partitioning a network 
	# into mutually exclusive communities such that the number of 
	# edges across different communities is significantly less than 
	# expectation, whereas the number of edges within each community is
	# significantly greater than expectation. The Louvain algortihm is
	# one of the most widely used for identifying communities due its
	# speed and high modularity. Modularity values can span from -1 to
	# 1, and the higher the value, the better the community structure 
	# that is formed.
	# The authors performed the Louvain algorithm on this dataset, and 
	# the results are given below. They show that there are 46 
	# communities, and a modularity of 0.953, which is a pretty good 
	# solution. Also we see a few communities that have more than 3 
	# members and some of the most influential people are in those 
	# communities. For example, P1, P12, P16 and P44 are all in 
	# community 2. These are some of the higher influential 
	# participants. The following code block also shows the code used 
	# for this purpose:
	# Starting with an initial partition of the graph and running the 
	# Louvain algorithm for Community Detection
	partition=community.best_partition(G, weight='MsgCount')
	print('Completed Louvain algorithm .. . . ' )
	values = [partition.get(node) for node in G.nodes()]
	list_com = partition.values()

	# Creating a dictionary like {community_number:list_of_participants}
	dict_nodes = {}

	# Populating the dictionary with items
	for each_item in partition.items():
		community_num = each_item[1]
		community_node = each_item[0]
		if community_num in dict_nodes:
			value = dict_nodes.get(community_num) + ' | ' + str(community_node)
			dict_nodes.update({community_num:value})
		else:
			dict_nodes.update({community_num:community_node})

	# Creating a dataframe from the diet, and getting the output into 
	# excel
	community_df=pd.DataFrame.from_dict(
		dict_nodes, orient='index', columns=['Members']
	)
	community_df.index.rename('Community_Num' , inplace=True)
	community_df.to_csv('Community_List_snippet.csv')

	# Creating a new graph to represent the communities created by the 
	# Louvain algorithm
	matplotlib.rcParams['figure.figsize'] = [12, 8]
	G_comm = nx.Graph()

	# Populating the data from the node dictionary created earlier
	G_comm.add_nodes_from(dict_nodes)

	# Calculating modularity and the total number of communities
	mod=community.modularity(partition,G)
	print("Modularity: ", mod)
	print("Total number of Communities=", len(G_comm.nodes()))

	# Creating the Graph and also calculating Modularity
	matplotlib.rcParams['figure.figsize'] = [12, 8]
	pos_louvain = nx.spring_layout(G_comm)
	nx.draw_networkx(
		G_comm, pos_louvain, with_labels=True, node_size=160, 
		font_size=11,label='Modularity =' + str(round(mod,3)) +
			', Communities=' + str(len(G_comm.nodes()))
	)
	plt.suptitle(
		'Community structure (Louvain Algorithm)', fontsize=22, 
		fontname='Arial'
	)
	plt.box(on=None)
	plt.axis('off')
	plt.legend(bbox_to_anchor=(0,1), loc='best', ncol=1)
	plt.savefig('louvain.png', dpi=400, bbox_inches='tight')

	# If we were to visualize all the non-overlapping communities in 
	# different colors, we would get the following image. As we can see
	# in the first two examples, we see the cases where there are 
	# members from different communities that converse with each other.
	# In Example 1, we see six people that are in two communities, 9 
	# and 38., and they have some inter-community and intra-community 
	# communication. The same conclusion holds true for communities 18 
	# and 39.


	# Girvan-Newman Algorithm:
	# This has four steps and can be given as follows:
	# a. The betweenness of all existing edges in the network is 
	#	calculated first.
	# b. The edge with highest betweenness is removed.
	# c. The betweenness of all edges affected by the removal is 
	#	recalculated.
	# d. Steps b. and c. are repeated until no edges remain.
	# The Girvan-Newman algorithm gives a very similar solution, that 
	# is slightly inferior to the Louvain algorithm, but also does a 
	# little worse in terms of performance. The modularity is a little 
	# lesser, and around 0.94 for this algorithm. The code block for 
	# the Girvan-Newman algorithm is quite similar to that for the 
	# Louvain algorithm, and can be found at the Github link given at 
	# the beginning of the article. The next figure shows the community
	# structure for the Girvan-Newman Algorithm.


	# Maximal Clique Calculation:
	# Cliques are sub-graphs in which every node is connected to every 
	# other node. A node can be a member of more than one 
	# clique/community hence there is a sense of overlapping structure.
	# As per the Maximal Cliques approach, we find cliques which are 
	# not sub-graphs of any other clique. The Bron-Kerbosch algorithm 
	# is famous in this aspect, the authors pick maximal cliques bigger
	# than minimum size (number of nodes).
	# When run on this data, 79 cliques were formed, and the following 
	# figure shows the top 15 communities (overlapping) found using 
	# maximal cliques. We can see some communities have multiple 
	# influential people in them, such as cliques 40, 41 and 43. We can
	# also see the interconnectedness between cliques, as we see 11 
	# nodes all being a part of 8 overlapping cliques. This can be used
	# to identify a sub-section of communities that are more closely 
	# connected than other sets of nodes.
	# Now, if would like to view the interconnectedness between cliques
	# for the complete network/dataset, we can see the image below, and 
	# also the supporting Python code:
	# Finding the Maximal Cliques associated with teh graph
	a = nx.find_cliques(G)
	i = 0

	# For each clique, print the members and also print the total 
	# number of communities
	for clique in a:
		print(clique)
		i += 1
	total_comm_max_cl = i
	print('Total number of communities: ', total_comm_max_cl)

	# Remove "len(clique)>1" if you're interested in maxcliques with 2 
	# or more edges
	cliques = [clique for clique in nx.find_cliques(G) if len(clique)>1]


	# Test Exercise: Real World/Large Scale Data
	# In addition to the metrics and algorithms used above, the authors
	# also looked at scenarios with large-scale simulated data. This is
	# to give the user a better understanding of how these scenarios 
	# work, and how the complexity increases when the data is scaled 
	# up. The increase of the density in connections and differences in
	# the quality of solutions becomes evident.
	# For clique calculation, with a highly dense and clustered graph, 
	# filtering for cliques that are greater than a certain threshold 
	# is helpful. This allows for formation of only the most connected 
	# communities, and can assist in filtering out nodes. 


	# Conclusion
	# With the world increasingly networked, community detection and 
	# relationships across different nodes will be an interesting space
	# to watch. Benchmarking across different algorithms of community 
	# detection namely the Louvian algorithm, Girvan-Newman algorithm 
	# and Clique based algorithms clearly depicts that the first one is
	# far more efficient — specially with respect to focus towards 
	# finding ‘like’ minded nodes. However, usage/efficiency might 
	# differ from one domain to another depending on the use cases. 
	# Market Surveillance has been a space where false alerts lead to 
	# significant wastage of time — hence innovative technology 
	# advances/research are very handy to reduce false alert ratio. The
	# authors' intent is to continue trying out new ideas to make 
	# market surveillance more robust and efficient.


	# Exit the program.
	exit(0)


if __name__ == '__main__':
	main()