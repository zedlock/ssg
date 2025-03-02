from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, value, tag, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        html = self.value
        if self.tag:
            if self.props:
                attr_string = f" {super().props_to_html()}"
            else: 
                attr_string = ""
            html = f"<{self.tag}{attr_string}>{html}</{self.tag}>"

        return html

