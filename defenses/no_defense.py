"""
No-op defense: passes all tool outputs through unmodified.

Used as the baseline in experiments.
"""


class NoDefense:
    name = "no_defense"

    def filter_tool_output(self, tool_name, output_text):
        """Return the tool output unchanged."""
        return output_text

