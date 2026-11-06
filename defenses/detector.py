"""
Detection defense: scans tool output for common prompt-injection
patterns and redacts or flags them.
"""

import re


# Patterns commonly seen in prompt-injection payloads.
INJECTION_PATTERNS = [
    re.compile(
        r"ignore\s+(all\s+)?(previous|prior|above)\s+"
        r"(instructions|prompts|rules)",
        re.IGNORECASE,
    ),
    re.compile(
        r"you\s+are\s+now\s+instructed\s+to",
        re.IGNORECASE,
    ),
    re.compile(
        r"SYSTEM\s+(NOTICE|OVERRIDE|MESSAGE)",
        re.IGNORECASE,
    ),
    re.compile(
        r"treat\s+these?\s+instructions?\s+as\s+"
        r"higher\s+priority",
        re.IGNORECASE,
    ),
    re.compile(
        r"override\s+the\s+assistant",
        re.IGNORECASE,
    ),
]


class DetectorDefense:
    name = "detector"

    def filter_tool_output(self, tool_name, output_text):
        """
        If suspicious patterns are found, redact the
        matching segments and prepend a warning.
        """
        flagged = False
        cleaned = output_text

        for pattern in INJECTION_PATTERNS:
            if pattern.search(cleaned):
                flagged = True
                cleaned = pattern.sub(
                    "[REDACTED — suspected injection]",
                    cleaned,
                )

        if flagged:
            cleaned = (
                "[WARNING: Potential prompt injection "
                "detected in tool output. Suspicious "
                "segments have been redacted.]\n\n"
                + cleaned
            )

        return cleaned

