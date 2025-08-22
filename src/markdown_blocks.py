from enum import Enum
import re
from htmlnode import *
from textnode import *
from split_delimiter import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    split_md = list(map(lambda x: x.strip(), split_md))
    for item in split_md:
        if item.startswith(" ") == True:
            split_md.remove(item)
    return split_md

def block_to_block_type(block):
    if block.startswith("#"):
        count = len(block) - len(block.lstrip("#"))
        if count > 6:
            raise Exception("too many leading #'s - invalid heading")
        
        return BlockType.HEADING
        
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
        
        
        
    if block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                raise Exception("line in quote not startswith >")
            
        return BlockType.QUOTE
            
    if block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                raise Exception("line in unordered list not startswith '- '")    

        return BlockType.UNORDERED_LIST    
            
    if block.startswith("1."):
        lines = block.split("\n")
        counter = 1
        for line in lines:
            if line[0] != f"{counter}" or line[1] != ".":
                raise Exception("list out of order")
            counter += 1
        return BlockType.ORDERED_LIST
            
    return BlockType.PARAGRAPH



#HELPER FUNCTIONS
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes
    
def list_item_children(block, blocktype):
    lines = block.split("\n")
    #print(f"Processing list block with {len(lines)} lines:")
    #for i, line in enumerate(lines):
        #print(f"  Line {i}: '{line}'")
    
    nodes = []
    for line in lines:
        if blocktype ==  BlockType.UNORDERED_LIST:
            stripped = line.lstrip("- ")
            #print(f"  Stripped line: '{stripped}'")
            children = text_to_children(stripped)
            #print(f"  Children from text_to_children: {children}")
            nodes.append(ParentNode("li", children=children))
        else:
            nodes.append(ParentNode("li", children=text_to_children(re.sub(r"^\d+\.\s", "", line))))
    return nodes 
    




def markdown_to_html_node(markdown):
    #break markdown up into blocks
    blocks = markdown_to_blocks(markdown)
    nodes = []
    #iterate over each block
    for block in blocks:
        # check theres no leading or trailing whitespace
        if not block.strip():
            continue
        #grab the block type for decision making 
        type = block_to_block_type(block)

        #print(f"Block: {block[:50]}... Type: {type}")

        node = None
        if type is BlockType.CODE:
            #strip code ```'s and leading newlines
            content = block.lstrip('```').rstrip('```').lstrip('\n')
            node = ParentNode(
                tag="pre",
                children=[text_node_to_html_node(TextNode(content, TextType.CODE)),]
            )
        if type is BlockType.PARAGRAPH:
            node = ParentNode(
                tag="p", 
                children=text_to_children(block.replace("\n", " "))
            )
        
        if type is BlockType.HEADING:
            node = ParentNode(
                #set tag as h1 - h6 based on number of #'s
                tag=f"h{len(block) - len(block.lstrip("#"))}",
                #strip #'s , leading and trailing whitespace, and newlines
                children=text_to_children(block.lstrip("#").strip().replace("\n", " "))
            )
        
        if type is BlockType.ORDERED_LIST:
            node = ParentNode(
                tag="ol", 
                children=list_item_children(block, blocktype=type)
            )

        if type is BlockType.UNORDERED_LIST:
            node = ParentNode(
                tag="ul", 
                children=list_item_children(block, blocktype=type)
            )
        
        if type is BlockType.QUOTE:
            # Split into lines, remove > from each line, then rejoin
            lines = block.split("\n")
            cleaned_lines = []
            for line in lines:
                cleaned_lines.append(line.lstrip("> "))  # Remove > and space
            quote_text = " ".join(cleaned_lines)  # Join with spaces
            node = ParentNode(
                tag="blockquote", 
                children=text_to_children(quote_text)
            )
        if node is None:
            raise Exception("Unknown block type")
        nodes.append(node)

    return ParentNode("div", children=nodes)





def extract_title(markdown):
    for line in markdown.split('\n'):
        # Must be "# " at the start (not "##", etc.)
        if line.startswith("# "):
            # Only the first, with leading/trailing whitespace stripped
            return line[2:].strip()
    raise Exception("no title found")