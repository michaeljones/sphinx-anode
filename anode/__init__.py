
from docutils import nodes
from docutils.parsers.rst import directives

import os

# Nodes
# -----

class Anode(nodes.General, nodes.Element):

    @staticmethod
    def visit(visitor, node):
        visitor.body.append(
                visitor.starttag(
                    node,
                    "div",
                    style="position: relative; width: %spx; height: %spx; background-image: url(%s)"
                                % ( node.width, node.height, node.url)
                    )
                )

        visitor.body.append("\n")
        for entry in node.content:

            div_style =  "position: absolute;"
            div_style += "top: %spx;" % entry[0]
            div_style += "left: %spx;" % entry[1]
            # div_style += "border: 1px solid black;"

            a_style = "height: %spx;" % entry[2]
            a_style += "width: %spx;" % entry[3]
            a_style += "cursor: pointer;"
            a_style += "display: block;"

            name = entry[4]

            id = name.replace(" ", "_")

            a_mouseover = "$('#" + id + "').css('background-color', 'yellow');"
            a_mouseout = "$('#" + id + "').css('background-color', 'transparent');"

            visitor.body.append(visitor.starttag( node, "div", style=div_style))
            visitor.body.append(visitor.starttag( node, "a", style=a_style, onmouseout=a_mouseout, onmouseover=a_mouseover))
            visitor.body.append("</a>")
            visitor.body.append("</div>\n")

        visitor.body.append("</div>\n")
        visitor.body.append("\n")


        visitor.body.append(visitor.starttag( node, "div" ))

        for entry in node.content:

            name = entry[4]
            content = entry[5]
            
            id = name.replace(" ", "_")
            
            visitor.body.append(visitor.starttag( node, "div", ids=[id]))
            visitor.body.append(name)
            visitor.body.append(content)
            visitor.body.append("</div>\n")


        visitor.body.append("</div>")

    @staticmethod
    def depart(visitor, node):
        pass

# Directives
# ----------

def anode_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):

    for i, line in enumerate(content):
        content[i] = line.lstrip()

    code = "\n".join(content)

    result = eval(code)

    height = arguments[0]
    width = arguments[1]
    reference = directives.uri(arguments[2])
    url = arguments[2]

    anode = Anode()
    anode.reference = reference
    anode.url = url
    anode.height = height
    anode.width = width
    anode.content = result

    return [anode]



# Setup
# -----

def setup(app):

    app.add_directive(
            "anode",
            anode_directive,
            1,
            (3,0,0)
            )

    app.add_node(Anode, html=(Anode.visit, Anode.depart))

