import json
from pathlib import Path
from typing import Optional, Union, List, Dict
from utils import load_jinja_as_string
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
        self.chat_template
        if chat_template is not None:
            chat_template = chat_template \
                if isinstance(chat_template, str) else load_jinja_as_string(chat_template)
            self.tokenizer.chat_template = chat_template
        self.pipe = ConversationalPipeline(model=self.model, tokenizer=self.tokenizer)
        self.conversation = None

    def __str__(self) -> str:
        return str(self.conversation)

    def send_message(self, message: str) -> str:
        if self.conversation is None:
            self.conversation = Conversation(message)
        else:
            self.conversation.add_message({"role": "user", "content": message})
        self.conversation = self.pipe(self.conversation)
        return self.conversation.generated_responses[-1]

    def save_history(self, path: Union[str, Path]) -> None:
        conversation_json = list(self.conversation)
        with open(path):
            json.dump(conversation_json, path)

    def set_conversation(self, conversation: Conversation):
        self.conversation = conversation
    
    def clean_history(self) -> None:
        self.conversation = None

    @staticmethod
    def import_history(self, path: Union[str, Path]) -> List[Dict[str, str]]:
        with open(path) as f:
            conversation_json = json.load(f)
        return conversation_json
