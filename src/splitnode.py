from textnode import TextNode, TextType
from links_and_images import extract_markdown_images, extract_markdown_links

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # or "_" depending on your preference
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        nodelist = node.text.split(sep=delimiter)
        
        if len(nodelist) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: closing delimiter '{delimiter}' not found.")
        
        for i in range(len(nodelist)):
            if nodelist[i] == "":
                continue
            
            if i % 2 == 0:
                new_nodes.append(TextNode(nodelist[i], TextType.PLAIN))
            else:
                new_nodes.append(TextNode(nodelist[i], text_type))
                
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # 1. Skip non-text nodes
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # 2. Get the pre-extracted images
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        # 3. Track our working string as we chop pieces off it
        current_text = node.text
        
        for alt_text, url in images:
            # Reconstruct the exact string to split on
            image_markdown = f"![{alt_text}]({url})"
            
            # Split into exactly 2 parts: [everything_before, everything_after]
            sections = current_text.split(image_markdown, 1)
            
            # If there's text before the image, add it as a plain text node
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # The remaining text becomes our new starting point for the next image
            current_text = sections[1]
                
        # 4. After processing all images, add any remaining trailing text
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.PLAIN))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        # 1. Skip non-text nodes
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        # 2. Get the pre-extracted links
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        # 3. Track our working string as we chop pieces off it
        current_text = node.text
        
        for anchor_text, url in links:
            # Reconstruct the exact link string to split on
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split into exactly 2 parts: [everything_before, everything_after]
            sections = current_text.split(link_markdown, 1)
            
            # If there's text before the link, add it as a plain text node
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # The remaining text becomes our new starting point for the next link
            current_text = sections[1]
                
        # 4. After processing all links, add any remaining trailing text
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.PLAIN))

    return new_nodes