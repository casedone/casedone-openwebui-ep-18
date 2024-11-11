"""
title: Token Count
author: Pisek
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional
import tiktoken
from open_webui.utils.misc import get_last_user_message_item, get_last_assistant_message
import time


global token_msg


class Filter:
    class Valves(BaseModel):
        encoding_name: str = Field(default="cl100k_base", description="encoding name")

    # class UserValves(BaseModel):
    #     max_turns: int = Field(
    #         default=4, description="Maximum allowable conversation turns for a user."
    #     )
    #     pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def count_tokens(self, text: str, encoding_name: str) -> int:
        """
        Counts the number of tokens in a given text using the specified encoding.

        Parameters:
            text (str): The text to count tokens in.
            encoding_name (str): The encoding model name to use. Default is 'cl100k_base'.

        Returns:
            int: The number of tokens in the text.
        """
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(text)
        return len(tokens)

    async def inlet(
        self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None
    ) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")
        
        

        # if __user__.get("role", "admin") in ["user", "admin"]:
        messages = body.get("messages", [])
        message = get_last_user_message_item(messages)
        count = self.count_tokens(message["content"], self.valves.encoding_name)
        _token_msg = f"Input tokens: {count}"
        global token_msg
        token_msg = _token_msg
        
        time.sleep(3)
        
        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": token_msg, "done": True},
            }
        )
        
        

        return body

    async def outlet(
        self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None
    ) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        messages = body.get("messages", [])
        message = get_last_assistant_message(messages)
        count = self.count_tokens(message, self.valves.encoding_name)
        _token_msg = f"Output tokens: {count}"
        global token_msg
        token_msg += ", " + _token_msg
        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": token_msg, "done": True},
            }
        )
        return body
