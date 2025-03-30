from county_graghs import load_inflow_graph
from graph_visualization import visualize_graph

if __name__ == "__main__":
    inflow_graph = load_inflow_graph("shrunk_inflow_data.csv")
    visualize_graph(inflow_graph)