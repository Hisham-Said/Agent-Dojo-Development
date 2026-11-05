# agent/providers/gemini_provider.py

import json

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL

from .base_provider import BaseProvider
from .response import LLMResponse, ToolCall


class GeminiProvider(BaseProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = GEMINI_MODEL

    # =========================================================
    # Tool conversion
    # =========================================================

    def _convert_tools(self, tools):

        if not tools:
            return None

        function_declarations = []

        for tool in tools:

            function = tool["function"]

            function_declarations.append(
                types.FunctionDeclaration(
                    name=function["name"],
                    description=function.get(
                        "description",
                        ""
                    ),
                    parameters=function.get(
                        "parameters"
                    ),
                )
            )

        return [
            types.Tool(
                function_declarations=function_declarations
            )
        ]

    # =========================================================
    # Convert messages
    # =========================================================

    def _convert_messages(self, messages):

        contents = []
        system_instruction = None

        for message in messages:

            role = message["role"]

            # -------------------------------------------------
            # SYSTEM
            # -------------------------------------------------

            if role == "system":

                system_instruction = message["content"]

                continue

            # -------------------------------------------------
            # USER
            # -------------------------------------------------

            if role == "user":

                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=message["content"]
                            )
                        ],
                    )
                )

            # -------------------------------------------------
            # ASSISTANT
            # -------------------------------------------------

            elif role == "assistant":

                # IMPORTANT:
                #
                # If this message contains the original Gemini
                # response, use its original Content object.
                #
                # This preserves thought_signature.

                raw_response = message.get(
                    "raw_response"
                )

                if raw_response is not None:

                    candidates = (
                        raw_response.candidates
                        or []
                    )

                    if candidates:

                        original_content = (
                            candidates[0].content
                        )

                        if original_content:

                            contents.append(
                                original_content
                            )

                            continue

                # Fallback for normal text assistant messages

                parts = []

                if message.get("content"):

                    parts.append(
                        types.Part.from_text(
                            text=message["content"]
                        )
                    )

                if parts:

                    contents.append(
                        types.Content(
                            role="model",
                            parts=parts,
                        )
                    )

            # -------------------------------------------------
            # TOOL RESULT
            # -------------------------------------------------

            elif role == "tool":

                tool_name = message["name"]

                try:

                    result = json.loads(
                        message["content"]
                    )

                except Exception:

                    result = message["content"]

                # Gemini requires FunctionResponse.response
                # to be a dictionary.

                if not isinstance(result, dict):

                    result = {
                        "result": result
                    }

                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_function_response(
                                name=tool_name,
                                response=result,
                            )
                        ],
                    )
                )

        return contents, system_instruction

    # =========================================================
    # Generate
    # =========================================================

    def generate(self, messages, tools=None):

        contents, system_instruction = (
            self._convert_messages(messages)
        )

        gemini_tools = self._convert_tools(tools)

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=gemini_tools,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        # =====================================================
        # Parse response
        # =====================================================

        text_parts = []
        tool_calls = []

        candidates = response.candidates or []

        if candidates:

            parts = (
                candidates[0]
                .content
                .parts
                or []
            )

            for index, part in enumerate(parts):

                # ---------------------------------------------
                # Text
                # ---------------------------------------------

                if getattr(part, "text", None):

                    text_parts.append(
                        part.text
                    )

                # ---------------------------------------------
                # Function call
                # ---------------------------------------------

                function_call = getattr(
                    part,
                    "function_call",
                    None
                )

                if function_call:

                    tool_calls.append(
                        ToolCall(
                            call_id=(
                                f"gemini_call_{index}"
                            ),
                            name=function_call.name,
                            arguments=(
                                dict(
                                    function_call.args
                                )
                                if function_call.args
                                else {}
                            ),
                        )
                    )

        text = "\n".join(
            text_parts
        ).strip()

        if not text:

            text = None

        return LLMResponse(
            text=text,
            tool_calls=tool_calls,
            raw_response=response,
        )