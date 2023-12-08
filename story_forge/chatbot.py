import os
import json
from pathlib import Path
from typing import Optional, Union, List, Dict
from transformers import (
    AutoModel, AutoTokenizer,
    ConversationalPipeline, Conversation,
    GenerationConfig, TextIteratorStreamer
)
from itertools import chain
from utils import load_jinja_as_string, save_conversation_as_json
from utils import ThreadWithReturnValue


class ChatBotSession:
    def __init__(
            self,
            model: AutoModel, 
            tokenizer: AutoTokenizer, 
            chat_template: Optional[Union[str, Path]] = None, 
            ) -> None:
        self.model = model
        self.tokenizer = tokenizer
        if chat_template is not None:
            chat_template = chat_template \
                if not os.path.exists(chat_template) else load_jinja_as_string(chat_template)
            self.tokenizer.chat_template = chat_template
        self.streamer = TextIteratorStreamer(tokenizer=tokenizer)
        self.pipe = ConversationalPipeline(
            model=self.model, tokenizer=self.tokenizer, streamer=self.streamer)
        self.conversation = Conversation()

    def __str__(self) -> str:
        return str(self.conversation)

    def generate(self, message: str, generation_cfg: Union[dict, GenerationConfig] = dict()) -> str:
        self.conversation.add_message({"role": "user", "content": message})
        self.conversation = self.pipe(self.conversation, **generation_cfg)
        return self.conversation.generated_responses[-1]

    def stream_generate(
            self, message: str, 
            generation_cfg: Union[dict, GenerationConfig] = dict()
            ) -> str:
        self.conversation.add_message({"role": "user", "content": message})
        thread = ThreadWithReturnValue(
            target=self.pipe, kwargs={"conversations": self.conversation, **generation_cfg})
        thread.start()
        streamer_iter = iter(self.streamer)
        for new_text in chain(streamer_iter, [None]):
            if "[/INST]" in new_text:
                continue
            if new_text is None:
                self.conversation = thread.join()
                return None
            yield new_text
        
    def is_conversation_exist(self) -> bool:
        return len(self.conversation) > 0

    def set_conversation(self, conversation: Conversation):
        self.conversation = conversation
    
    def clean_conversation(self) -> None:
        self.conversation = Conversation()
        
    def save_conversation(self, path: Union[str, Path]) -> None:
        if self.is_conversation_exist():
            raise RuntimeError("Conversation doesn't exist for saving!")
        save_conversation_as_json(self.conversation)

    @staticmethod
    def import_conversation(path: Union[str, Path]) -> List[Dict[str, str]]:
        with open(path) as f:
            conversation_json = json.load(f)
        return conversation_json
