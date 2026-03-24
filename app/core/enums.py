from enum import Enum

class MarkdownFormat(str, Enum):
    COMMONMARK = "commonmark"
    GFM = "gfm"
    MARKDOWN = "markdown"
