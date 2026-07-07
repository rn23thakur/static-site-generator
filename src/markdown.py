from parentnode import ParentNode
from blocks import markdown_to_blocks, block_to_block_type, BlockType
from splitnode import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block, block_to_block_type(block)) for block in blocks]
    return ParentNode(tag="div", children=children)


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
    raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph_text = " ".join(lines)  # soft line breaks -> spaces, per CommonMark
    paragraph_text_refined = " ".join(paragraph_text.split())
    return ParentNode(tag="p", children=text_to_children(paragraph_text_refined))


def heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level + 1:]  # skip the space after the #'s
    return ParentNode(tag=f"h{level}", children=text_to_children(text))


def code_to_html_node(block):
    # 1. Strip the leading backticks and the first newline
    text = block[3:].lstrip("\n") 
    
    # 2. Slice off the trailing backticks precisely without stripping the final \n
    if text.endswith("```"):
        text = text[:-3] 
    code_text_node = TextNode(text=text, text_type=TextType.CODE)
    code_leaf_node = text_node_to_html_node(code_text_node)
    return ParentNode(tag="pre", children=[code_leaf_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = [line.lstrip(">").strip() for line in lines]
    text = " ".join(stripped_lines)
    return ParentNode(tag="blockquote", children=text_to_children(text))


def unordered_list_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for item in items:
        text = item[2:]  # strip "- "
        list_items.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ul", children=list_items)


def ordered_list_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for i, item in enumerate(items):
        prefix = f"{i + 1}. "
        text = item[len(prefix):]
        list_items.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ol", children=list_items)
