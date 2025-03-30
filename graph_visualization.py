import matplotlib.pyplot as plt
import networkx as nx
from fa2_modified import ForceAtlas2
import numpy as np

def visualize_migration_graph(graph, max_vertices=3000, title="County Migration Network"):
    """
    Visualize the migration graph with NetworkX.
    
    Args:
        graph: An InflowCountyGraph or OutflowCountyGraph instance
        max_vertices: Maximum number of vertices to include
        title: Title for the visualization
    """
    graph_nx = graph.to_networkx(max_vertices=max_vertices)
    
    degrees = dict(graph_nx.degree())
    
    max_edge_weight = max([graph_nx[u][v]['weight'] for u, v in graph_nx.edges()])
    edge_weights = [graph_nx[u][v]['weight']*20 / max_edge_weight for u, v in graph_nx.edges()]
    
    plt.figure(figsize=(40, 40))

    forceatlas2 = ForceAtlas2(
                        outboundAttractionDistribution=False,  # Dissuade hubs
                        linLogMode=False,  # NOT IMPLEMENTED
                        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
                        edgeWeightInfluence=1,

                        # Performance
                        jitterTolerance=0.1,  # Tolerance
                        barnesHutOptimize=True,
                        barnesHutTheta=2.0,
                        multiThreaded=False,  # NOT IMPLEMENTED

                        # Tuning
                        scalingRatio=1.0,
                        strongGravityMode=True,
                        gravity=0.1,

                        # Log
                        verbose=True)
    
    pos = forceatlas2.forceatlas2_networkx_layout(graph_nx, pos=None, iterations=1000)
    
    states = sorted(set(node[0] for node in graph_nx.nodes()))
    state_to_idx = {state: i for i, state in enumerate(states)}
    
    cmap = plt.cm.get_cmap('YlGnBu', len(states))
    
    for state in states:
        state_nodes = [node for node in graph_nx.nodes() if node[0] == state]
        node_subset_sizes = [degrees[node] * 20 for node in state_nodes]
        color_idx = state_to_idx[state]
        nx.draw_networkx_nodes(graph_nx, pos, nodelist=state_nodes, 
                              node_size=node_subset_sizes, 
                              edgecolors="black",
                              node_color=[cmap(color_idx)] * len(state_nodes), 
                              alpha=1.0, label=state)
    
    # nx.draw_networkx_edges(graph_nx, pos, width=edge_weights,arrows=True, connectionstyle="arc3,rad=0.2", alpha=0.5, 
    #                       edge_color='black')
    for u, v in graph_nx.edges():
        source_state = u[0] 
        color_idx = state_to_idx[source_state]
        edge_color = cmap(color_idx)
        
        nx.draw_networkx_edges(graph_nx, pos, edgelist=[(u, v)], 
                              width=edge_weights,
                              arrows=True, 
                              connectionstyle="arc3,rad=0.2", 
                              alpha=0.5, 
                              edge_color=[edge_color])
    
    node_labels = {node: f"{node[1]},\n {node[0]}" for node in graph_nx.nodes()}

    nx.draw_networkx_labels(graph_nx, pos, labels=node_labels, font_size= 2, font_weight="bold")
    
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    
    
    return plt