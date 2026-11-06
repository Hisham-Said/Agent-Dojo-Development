import json

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from .base_provider import BaseProvider
from .response import LLMResponse, ToolCall


class GroqProvider(BaseProvider):

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

        self.model = GROQ_MODEL

    def _convert_messages(self, messages):

        converted_messages = []

        for message in messages:

            converted = dict(message)

            # raw_response is an internal Gemini-only field.
            # Groq/OpenAI-compatible APIs do not support it.
            converted.pop("raw_response", None)

            converted_messages.append(
                converted
            )

        return converted_messages

    def generate(self, messages, tools=None):

        groq_messages = self._convert_messages(
            messages
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=groq_messages,
            tools=tools if tools else None,
            tool_choice="auto" if tools else "none",
        )

        message = response.choices[0].message

        tool_calls = []

        for tool_call in message.tool_calls or []:

            arguments = json.loads(
                tool_call.function.arguments
            )

            tool_calls.append(
                ToolCall(
                    call_id=tool_call.id,
                    name=tool_call.function.name,
                    arguments=arguments,
                )
            )

        return LLMResponse(
            text=message.content,
            tool_calls=tool_calls,
            raw_response=response,
        )