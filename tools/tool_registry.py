from .email_tools import get_emails, send_email
from .calendar_tools import get_calendar_events
from .drive_tools import search_files, read_file


TOOLS = {
    "get_emails": get_emails,
    "get_calendar_events": get_calendar_events,
    "search_files": search_files,
    "read_file": read_file,
    "send_email": send_email,
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_emails",
            "description": "Retrieve the user's emails.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_calendar_events",
            "description": "Retrieve the user's calendar events.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search the user's files by name or content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "integer",
                        "description": "The ID of the file.",
                    }
                },
                "required": ["file_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": (
                "Send an email to a recipient."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": (
                            "Recipient email address."
                        ),
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line.",
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body text.",
                    },
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
]
