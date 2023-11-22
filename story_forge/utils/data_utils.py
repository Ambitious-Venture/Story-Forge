import json
from pathlib import Path
from typing import Union
import networkx as nx
from networkx.readwrite import json_graph
from transformers import Conversation


def load_graph_from_json(fp: Union[str, Path]) -> nx.Graph:
    with open(fp) as f:
        js_graph = json.load(f)
    return json_graph.node_link_graph(js_graph)


def graph2conversations():
    ...


def save_conversation_as_json(conversation: Conversation, path: Union[str, Path]) -> None:
    conversation_json = list(conversation)
    with open(path):
        json.dump(conversation_json, path)