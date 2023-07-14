import igraph as ig
import matplotlib.pyplot as plt

def graph_maker():
#read from the node-attributes file to create nodes and store the data to a list
    node_file=open("node-attributes.csv", "r")
    nodes=[]
    for line in node_file:
        column_data=line.split(',')
        if column_data[0]!="id" and column_data[1]!="team":
            nodes.append((int(column_data[0]), column_data[1][:-1]))
#read from the network file that specifies the connections between nodes
    network_file=open("network-2.csv", "r")
    network=[]
    for line in network_file:
        column_data=line.split(',')
        if column_data[0]!="nodeID1" and column_data[1]!="nodeID2":
            network.append((int(column_data[0]), int(column_data[1][:-1])))
            
    node_file.close()
    network_file.close()
    
    n_vertices=len(nodes)
    # Construct a graph with some required vertices
    g = ig.Graph(n_vertices, network)
    g["title"] = "Small Social Network"
    #for i in range(0, len(g.vs)):
        #g.vs[i]["nodeID"]=str(i+1)
    # Plot in matplotlib
    fig, ax = plt.subplots(figsize=(5,5))
    ig.plot(
        g,
        target=ax,
        vertex_size=0.4,
        vertex_color="red",
        vertex_frame_width=1.0,
        vertex_frame_color="white",
        #vertex_label=g.vs["nodeID"],
        vertex_label_size=5.0,
        edge_width=1,
        edge_color="black"
    )

    plt.show()
    
graph_maker()