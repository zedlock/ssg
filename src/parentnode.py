from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")

        def inner_to_html(node):
            if not node.children:
                return node.to_html()
            
            html = f"<{self.tag}"
            if self.props:
                html += ' ' + super().props_to_html()
            html += ">"
            
            for child in node.children:
                html = html + child.to_html()

            html += f"</{self.tag}>"

            return html

        return inner_to_html(self)
