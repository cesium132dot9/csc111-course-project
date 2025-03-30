from __future__ import annotations
import csv
from typing import Set
import networkx as nx

class InflowCountyVertex:
    """A vertex representing a county in the migration graph.

        Instance Attributes:
        - id: Unique county ID
        - county_name: Name of the county
        - state_name: Name of the state
        - edges: A set of tuples representing connections to other counties and the number of people moved
    """
    id: int
    county_name: str
    state_name: str
    edges: Set[tuple[InflowCountyVertex, int]]

    def __init__(self, county_id: int, county_name: str, state_name: str) -> None:
        self.id = county_id
        self.county_name = county_name
        self.state_name = state_name
        self.edges = set()


class InflowCountyGraph:
    """A graph of counties representing inflow migration."""
    vertices: dict[int, InflowCountyVertex]

    def __init__(self) -> None:
        self.vertices = {}

    def add_vertex(self, county_id: int, county_name: str, state_name: str) -> InflowCountyVertex:
        """Add a vertex to the graph."""

        if county_id not in self.vertices:
            self.vertices[county_id] = InflowCountyVertex(county_id, county_name, state_name)
        return self.vertices[county_id]

    def add_edge(self, source_id: int, source_name: str, source_state: str, dest_id: int, dest_name: str,
                 dest_state: str, amount: int) -> None:
        """Add an inflow edge: someone moved from source to des"""

        source_vertex = self.add_vertex(source_id, source_name, source_state)
        dest_vertex = self.add_vertex(dest_id, dest_name, dest_state)
        dest_vertex.edges.add((source_vertex, amount))

    def get_top_sources(self, county_id: int, n: int) -> list[tuple[InflowCountyVertex, int]]:
        """return the top nth counties where people come from
        Preconditions:
            - n >= 0
        """

        if county_id not in self.vertices:
            return []
        target_county = self.vertices[county_id]
        inflows = list(target_county.edges)
        sorted_inflows = sorted(inflows, key=lambda x: x[1], reverse=True)
        return sorted_inflows[:n]

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """"""
        graph_nx = nx.Graph()
        for v in self.vertices.values():
            v_names = (v.state_name, v.county_name)
            graph_nx.add_node(v_names)

            for u, amount in v.edges:
                u_names = (u.state_name, u.county_name)
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u_names)

                if u_names in graph_nx.nodes:
                    graph_nx.add_edge(v_names, u_names, weight = amount)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx


def load_inflow_graph(filename: str) -> InflowCountyGraph:
    """read the given CSV file and build InflowCountyGraph"""
    graph = InflowCountyGraph()
    with open(filename, encoding='latin-1') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            source_id = int(row[3])
            source_name = row[4]
            source_state = row[5]
            dest_id = int(row[0])
            dest_name = row[1]
            dest_state = row[2]
            amount = int(float(row[6]))
            graph.add_edge(source_id, source_name, source_state, dest_id, dest_name, dest_state, amount)
    return graph


class OutflowCountyVertex:
    """A vertex representing a county in the migration graph.

        Instance Attributes:
        - id: Unique county ID
        - county_name: Name of the county
        - state_name: Name of the state
        - edges: A set of tuples representing connections to other counties and the number of people moved
    """
    id: int
    county_name: str
    state_name: str
    edges: Set[tuple[OutflowCountyVertex, int]]

    def __init__(self, county_id: int, county_name: str, state_name: str) -> None:
        self.id = county_id
        self.county_name = county_name
        self.state_name = state_name
        self.edges = set()


class OutflowCountyGraph:
    """A graph of counties representing inflow migration."""
    vertices: dict[int, OutflowCountyVertex]

    def __init__(self) -> None:
        self.vertices = {}

    def add_vertex(self, county_id: int, county_name: str, state_name: str) -> OutflowCountyVertex:
        """Add a vertex to the graph.
        Preconditions:
        - county_id not in self._vertices
        """
        if county_id not in self.vertices:
            self.vertices[county_id] = OutflowCountyVertex(county_id, county_name, state_name)
        return self.vertices[county_id]

    def add_edge(self, source_id: int, source_name: str, source_state: str, dest_id: int, dest_name: str,
                 dest_state: str, amount: int) -> None:
        """Add an Outflow edge: someone moved from source to des"""
        source_vertex = self.add_vertex(source_id, source_name, source_state)
        dest_vertex = self.add_vertex(dest_id, dest_name, dest_state)
        source_vertex.edges.add((dest_vertex, amount))

    def get_top_destinations(self, county_id: int, n: int) -> list[tuple[OutflowCountyVertex, int]]:
        """return the top nth counties where people travel to"""
        if county_id not in self.vertices:
            return []
        target_county = self.vertices[county_id]
        outflows = list(target_county.edges)
        sorted_outflows = sorted(outflows, key=lambda x: x[1], reverse=True)
        return sorted_outflows[:n]


def load_outflow_graph(filename: str) -> OutflowCountyGraph:
    """read the given CSV file and build OutflowCountyGraph"""
    graph = OutflowCountyGraph()
    with open(filename, encoding='latin-1') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            source_id = int(row[3])
            source_name = row[4]
            source_state = row[5]
            dest_id = int(row[0])
            dest_name = row[1]
            dest_state = row[2]
            amount = int(float(row[6]))
            graph.add_edge(source_id, source_name, source_state, dest_id, dest_name, dest_state, amount)
    return graph


def name_to_id_map(graph) -> dict[tuple[str, str], int]:
    """Create a mapping from (county_name, state_name) to county_id."""
    dict_so_far = {}
    for i in graph.vertices.values():
        key = (i.county_name, i.state_name)
        dict_so_far[key] = i.id
    return dict_so_far
