# agent/providers/response.py


class ToolCall:

    def __init__(
        self,
        call_id,
        name,
        arguments
    ):
        self.id = call_id
        self.name = name
        self.arguments = arguments


class LLMResponse:

    def __init__(
        self,
        text=None,
        tool_calls=None,
        raw_response=None
    ):
        self.text = text
        self.tool_calls = tool_calls or []
        self.raw_response = raw_response

    @property
    def has_tool_calls(self):
        return bool(self.tool_calls)