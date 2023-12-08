import os
import json
from pathlib import Path
from typing import Optional, Union, List, Dict
from utils import load_jinja_as_string, save_conversation_as_json
from transformers import (
    AutoModel, AutoTokenizer, 
    ConversationalPipeline, Conversation, 
    GenerationConfig
)


class ChatBotSession:
    def __init__(
            self,
            model: AutoModel, 
            tokenizer: AutoTokenizer, 
            chat_template: Optional[Union[str, Path]] = None, 
            generation_cfg: Optional[GenerationConfig] = None
            ) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.generation_cfg = generation_cfg
        if chat_template is not None:
            chat_template = chat_template \
                if not os.path.exists(chat_template) else load_jinja_as_string(chat_template)
            self.tokenizer.chat_template = chat_template
        self.pipe = ConversationalPipeline(model=self.model, tokenizer=self.tokenizer)
        self.conversation = Conversation()

    def __str__(self) -> str:
        return str(self.conversation)

    def send_message(self, message: str) -> str:
        self.conversation.add_message({"role": "user", "content": message})
        self.conversation = self.pipe(self.conversation)
        return self.conversation.generated_responses[-1]
    
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
