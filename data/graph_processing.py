import json
from pathlib import Path
from typing import Union
import networkx as nx
from networkx.readwrite import json_graph
from functools import cached_property


class DiaologGraph:

    def __init__(self, graph_json_path: Union[str, Path]) -> None:
        self.graph = self.load_graph_from_json(graph_json_path)

    @cached_property
    def start_nodes(self) -> list[str]:
        start_nodes = [n for n, d in self.graph.in_degree() if d == 0]
        return start_nodes
    
    @cached_property
    def last_nodes(self) -> list[str]:
        last_nodes = [n for n, d in self.graph.out_degree() if d == 0]
        return last_nodes

    def passing_through_graph(self, sequences: list[str]) -> list[dict[str, str]]:
        node_id = sequences.pop(0)
        data = self.graph.nodes[node_id]
        if len(sequences) > 0:
            next_node_id = sequences[0]
            edge_data = self.graph.get_edge_data(node_id, next_node_id, default=None)

            if edge_data is None:
                raise RuntimeError(f"{node_id} isn't linked to {next_node_id}!")

            return [
                {"role": "node", "content": data["text"]},
                {"role": "edge", "content": edge_data["text"] or next_node_id},
                *self.passing_through_graph(sequences)
            ]
        return [{"role": "node", "content": data["text"]}]

    def iterate_through_graph(self, start_node: str, last_node: str = None) -> list[dict[str, str]]:
        last_nodes = [last_node] if last_node is not None else self.last_nodes
        for ln in last_nodes:
            for path in nx.all_simple_paths(self.graph, start_node, ln):
                yield self.passing_through_graph(path)
    
    @staticmethod
    def load_graph_from_json(fp: Union[str, Path]) -> nx.DiGraph:
        with open(fp) as f:
            js_graph = json.load(f)
        return json_graph.node_link_graph(js_graph)