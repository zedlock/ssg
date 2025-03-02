class HTMLNode:
    def __init__(
        self,
        tag = None,
        value = None,
        children = None,
        props = None
    ):
        self.tag = tag
        self.value = value
        if children == None:
            self.children = []
        else:
            self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        attr_strings = []
        if (self.props):
            for prop in self.props:
                attr_strings.append(f"{prop}=\"{self.props[prop]}\"")
        return " ".join(attr_strings)

    def __repr__(self):
        tag = f"tag: {self.tag}\n"
        value = f"value: {self.value}\n"
        children = f"children: {len(self.children)}\n"
        props = f"props: {self.props}"
        return tag + value + children + props
