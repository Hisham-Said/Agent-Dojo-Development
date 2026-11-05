import json

from config import MAX_AGENT_STEPS, LLM_PROVIDER

from agent.providers.factory import create_provider
from tools.tool_registry import TOOLS, TOOL_SCHEMAS


class LLMAgent:

    def __init__(self):

        self.provider_name = LLM_PROVIDER

        self.provider = create_provider(
            self.provider_name
        )

    def _switch_provider(self):

        if self.provider_name == "gemini":
            next_provider = "groq"
        else:
            next_provider = "gemini"

        print(
            f"\n[Provider Switch] "
            f"{self.provider_name.upper()} -> "
            f"{next_provider.upper()}"
        )

        self.provider_name = next_provider

        self.provider = create_provider(
            self.provider_name
        )

    def _is_provider_failure(self, error):

        error_text = str(error).lower()

        provider_failure_indicators = [
            # Rate limits / quota
            "429",
            "resource_exhausted",
            "quota exceeded",
            "rate limit",
            "rate_limit_exceeded",
            "too many requests",

            # Temporary Gemini/server failures
            "503",
            "service unavailable",
            "unavailable",
            "high demand",

            "500",
            "internal server error",

            "502",
            "bad gateway",

            "504",
            "gateway timeout",
            "deadline exceeded",
        ]

        return any(
            indicator in error_text
            for indicator in provider_failure_indicators
        )

    def run(self, user_prompt):

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant operating "
                    "inside a simulated environment.\n\n"
                    "Complete the user's task using "
                    "the available tools when necessary.\n\n"
                    "Do not invent tool results."
                ),
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        provider_attempted = set()

        for step in range(MAX_AGENT_STEPS):

            print(
                f"\n[Agent Step {step + 1}]"
            )

            try:

                response = self.provider.generate(
                    messages,
                    tools=TOOL_SCHEMAS
                )

            except Exception as error:

                print(
                    f"\n[Provider Error] "
                    f"{self.provider_name.upper()}: "
                    f"{error}"
                )

                # Only automatically switch for
                # quota/rate-limit errors.
                if self._is_provider_failure(error):

                    provider_attempted.add(
                        self.provider_name
                    )

                    # Try the other provider if
                    # we haven't already tried it.
                    if len(provider_attempted) < 2:

                        self._switch_provider()

                        # Retry this SAME agent step
                        # using the new provider.
                        continue

                raise

            if response.has_tool_calls:

                messages.append(
                    {
                        "role": "assistant",
                        "content": response.text or "",
                        "tool_calls": [
                            {
                                "id": call.id,
                                "name": call.name,
                                "arguments": call.arguments,
                            }
                            for call in response.tool_calls
                        ],
                        "raw_response": response.raw_response,
                    }
                )

                for tool_call in response.tool_calls:

                    function_name = tool_call.name
                    arguments = tool_call.arguments

                    print(
                        f"Tool requested: "
                        f"{function_name}"
                    )

                    print(
                        f"Arguments: {arguments}"
                    )

                    if function_name not in TOOLS:

                        result = {
                            "error": (
                                f"Unknown tool: "
                                f"{function_name}"
                            )
                        }

                    else:

                        function = TOOLS[function_name]

                        try:
                            result = function(
                                **arguments
                            )

                        except Exception as error:

                            result = {
                                "error": str(error)
                            }

                    print(
                        f"Tool result: {result}"
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(
                                result
                            ),
                        }
                    )

                continue

            if response.text:
                return response.text

            return (
                "The model returned "
                "an empty response."
            )

        return (
            "The agent reached the maximum "
            "number of allowed steps."
        )