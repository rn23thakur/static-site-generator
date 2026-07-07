from enum import Enum

class BlockType(str, Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    return [block.strip() for block in raw_blocks if block.strip() != ""]

def block_to_block_type(block: str) -> BlockType:
    if not block:
        return BlockType.PARAGRAPH

    # Route based on initial indicators, but validate fully inside helpers
    if block.startswith('#'):
        return is_heading(block)
    if block.startswith('>'):
        return is_quote(block)
    if block.startswith('- '):
        return is_unordered_list(block)
    if block.startswith('```'):
        return is_code(block)
    if block[0].isdigit():
        return is_ordered_list(block)
        
    return BlockType.PARAGRAPH

def is_heading(block: str) -> BlockType:
    # Split into maximum 2 parts to find the prefix safely
    parts = block.split(maxsplit=1)
    prefix = parts[0]
    
    # Must be 1-6 '#' characters, and there must be text after the space
    if 1 <= len(prefix) <= 6 and all(char == '#' for char in prefix):
        if len(parts) > 1:
            return BlockType.HEADING
            
    return BlockType.PARAGRAPH

def is_quote(block: str) -> BlockType:
    lines = block.split("\n")
    for line in lines:
        # Every line must start with '>'
        if not line.startswith('>'):
            return BlockType.PARAGRAPH
    return BlockType.QUOTE

def is_unordered_list(block: str) -> BlockType:
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("- "):
            return BlockType.PARAGRAPH
    return BlockType.UNORDERED_LIST

def is_ordered_list(block: str) -> BlockType:
    lines = block.split("\n")
    for i, line in enumerate(lines):
        expected_num = i + 1
        prefix = f"{expected_num}. "
        if not line.startswith(prefix):
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST

def is_code(block: str) -> BlockType:
    # Must start with triple backticks and a newline, and end with triple backticks
    if block.startswith("```\n") and block.endswith("```"):
        # Make sure it's not just "```\n```" without content if requirements dictate
        return BlockType.CODE
    return BlockType.PARAGRAPH
