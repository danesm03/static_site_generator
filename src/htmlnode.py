from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value =  value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        str_rep = ""
        for k, v in self.props.items():
            str_rep += f' {k}="{v}"'
        return str_rep
    

    def __repr__(self):
        tag = f'"{self.tag}"' if self.tag is not None else "None"
        value = f'"{self.value}"' if self.value is not None else "None"
        if self.children is None:
            children_str = "None"
        else:
            children_str = ", ".join([f'"{repr(child)}"' for child in self.children])
        repr_str = f"HTMLNode({tag}, {value}, {children_str if self.children else 'None'}, {self.props_to_html()})"
        return repr_str
        


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)


    def to_html(self):
        if not self.value:
            raise ValueError("Leaf Node must have a value")
        
        if self.children:
            raise ValueError("LeafNode cannot have any children")
        
        if not self.tag:
            return f"{self.value}"
        else:
            #print(f"self.props = {self.props}")
            #print(f"bool(self.props) = {bool(self.props)}")
            if self.props:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            else:
                return f'<{self.tag}>{self.value}</{self.tag}>'
          

    

        