from __future__ import annotations
from typing import List, Dict, Optional

class HTMLNode():
    def __init__(
            self, 
            tag: Optional[str] = None, 
            value: Optional[str] = None, 
            children: Optional[List[HTMLNode]] = None, 
            props: Optional[Dict[str, str]] = None
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_string = ""
        if self.props is None:
            return props_string
        for key, value in self.props.items():
            props_string += f" {key}=\"{value}\""
        return props_string.strip()
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"