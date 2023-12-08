from typing import List, Callable
from chatbot import ChatBotSession
from transformers import Conversation


def history2conversation(history: List[List[str]]) -> Conversation:
    conversation_history = []
    for user, bot in history:
        conversation_history.append({
            "role": "user",
            "content": user
        })
        conversation_history.append({
            "role": "assistant",
            "content": bot
        })
    return Conversation(conversation_history)


def gradio_chatbot_func_generator(chatbot: ChatBotSession, streaming: bool = True) -> Callable:
    def generate_response(user_input: str, history: List[List[str]]) -> str:
        conversation = history2conversation(history)
        chatbot.set_conversation(conversation)
        response = chatbot.send_message(user_input)
        return response

    def streaming_generate_response(user_input: str, history: List[List[str]]) -> str:
        conversation = history2conversation(history)
        chatbot.set_conversation(conversation)
        generated_text = ""
        for new_text in chatbot.stream_generate(user_input):
            generated_text += new_text
            yield generated_text
    
    return streaming_generate_response if streaming else generate_response
