from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delim_list = node.text.split(delimiter)
            if len(delim_list) > 1:
                if len(delim_list) % 2 == 0:
                    raise Exception("closing delimiter not found - invalid syntax")
                else:
                    for index, item in enumerate(delim_list):
                        if item == "":
                            continue
                        if  index % 2 != 0:
                            new_nodes.append(TextNode(item, text_type=text_type))
                        else:
                            new_nodes.append(TextNode(item, TextType.TEXT))
            if len(delim_list) == 1:
                new_nodes.append(TextNode(delim_list[0], TextType.TEXT))
    return new_nodes
    

def split_nodes_image(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            if node.text == "":
                continue
            text_list = []
            img_list = extract_markdown_images(node.text)
            current_text = node.text
            for image_text, image_link in img_list:
                sections = current_text.split(f"![{image_text}]({image_link})", maxsplit=1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                text_list.append(sections[0])
                current_text = sections[1]
            if len(img_list) > 0:
                for index, item in enumerate(text_list):
                    if item == "":
                        continue
                    final_list.append(TextNode(item,  TextType.TEXT))
                    final_list.append(TextNode(img_list[index][0], TextType.IMAGE, url=img_list[index][1]))

            if current_text != "":
                final_list.append(TextNode(current_text, TextType.TEXT))
    return final_list

                
            



def split_nodes_links(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            if node.text == "":
                continue
            text_list = []
            link_list = extract_markdown_links(node.text)
            current_text = node.text
            for link_text, link in link_list:
                sections = current_text.split(f"[{link_text}]({link})", maxsplit=1)
                if len(sections) != 2:
                    raise ValueError("invalid markdown, image section not closed")
                text_list.append(sections[0])
                current_text = sections[1]
            if len(link_list) > 0:
                for index, item in enumerate(text_list):
                    if item != "":  # Only add non-empty text
                        final_list.append(TextNode(item, TextType.TEXT))
                    # Always add the corresponding link (regardless of whether text was empty)
                    if index < len(link_list):  # Make sure we don't go out of bounds
                        final_list.append(TextNode(link_list[index][0], TextType.LINK, url=link_list[index][1]))
            if current_text != "":
                final_list.append(TextNode(current_text, TextType.TEXT))
    return final_list



def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_links = split_nodes_links(split_code)
    split_image = split_nodes_image(split_links)
    print("DEBUG: split_image nodes for text:", text)
    for n in split_image:
        print("  node:", n, "type:", n.text_type)
    return split_image



    

