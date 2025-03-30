from county_graghs import load_inflow_graph
from graph_visualization import visualize_migration_graph

if __name__ == "__main__":
    inflow_graph = load_inflow_graph("shrunk_inflow_data.csv")
    plt = visualize_migration_graph(inflow_graph, title="County Migration Inflow Network")
    plt.savefig('migration_visualization.png', dpi=300) 
    # plt.show() 