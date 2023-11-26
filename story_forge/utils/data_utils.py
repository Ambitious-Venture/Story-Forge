import json
from pathlib import Path
from typing import Union
from transformers import Conversation


def save_conversation_as_json(conversation: Conversation, path: Union[str, Path]) -> None:
    conversation_json = list(conversation)
    with open(path):
        json.dump(conversation_json, path)