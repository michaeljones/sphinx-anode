
from docutils import nodes
from docutils.parsers.rst import directives, Directive

import os
import hashlib

# Nodes
# -----

class AnnotatedImage(nodes.image):

    @staticmethod
    def visit(visitor, node):

        visitor.body.append(
                visitor.starttag(
                    node,
                    "div",
                    style="position: relative; width: %spx; height: %spx; background-image: url(%s)"
                                % ( node.width, node.height, node.uri_path )
                    )
                )

        for child in node.children:

            if hasattr( child, "annotation_info" ):

                info = child.annotation_info()

                div_style =  "position: absolute;"
                div_style += "top: %spx;" % info["top"]
                div_style += "left: %spx;" % info["left"]
                # div_style += "border: 1px solid black;"

                a_style = "height: %spx;" % info["height"]
                a_style += "width: %spx;" % info["width"]
                a_style += "cursor: pointer;"
                a_style += "display: block;"

                a_mouseover = "$('#" + info["id"] + "').css('background-color', 'yellow');"
                a_mouseout = "$('#" + info["id"] + "').css('background-color', 'transparent');"

                visitor.body.append(visitor.starttag( node, "div", style=div_style))
                visitor.body.append(visitor.starttag( node, "a", style=a_style, onmouseout=a_mouseout, onmouseover=a_mouseover))
                visitor.body.append("</a>")
                visitor.body.append("</div>\n")

        visitor.body.append("</div>\n")
        visitor.body.append("\n")

    @staticmethod
    def depart(visitor, node):
        pass



class Annotation(nodes.General, nodes.Element):

    def annotation_info(self):

        return dict(id=self.hashid, top=self.top, left=self.left, height=self.height, width=self.width)

    @staticmethod
    def visit(visitor, node):

        id = node.hashid
        visitor.body.append(visitor.starttag( node, "div", ids=[id]))

    @staticmethod
    def depart(visitor, node):

        visitor.body.append("</div>")



# Directives
# ----------

class AnnotatedImageDirective(Directive):

    required_arguments = 3
    has_content = True

    def run(self):

        height = self.arguments[0]
        width = self.arguments[1]
        uri = self.arguments[2]

        reference = directives.uri(self.arguments[2])
        self.options['uri'] = reference

        annotated_image = AnnotatedImage(**self.options)
        annotated_image.uri_path = uri
        annotated_image.height = height
        annotated_image.width = width

        self.state.nested_parse(self.content, self.content_offset, annotated_image)

        return [annotated_image]


class AnnotationDirective(Directive):

    required_arguments = 4
    has_content = True

    hashes = []

    def run(self):

        annotation = Annotation()

        annotation.hashid = hashlib.sha1(str(len(self.hashes))).hexdigest()
        self.hashes.append(annotation.hashid)

        annotation.top = self.arguments[0]
        annotation.left = self.arguments[1]
        annotation.height = self.arguments[2]
        annotation.width = self.arguments[3]

        self.state.nested_parse(self.content, self.content_offset, annotation)
    
        return [annotation]


# Setup
# -----

def setup(app):

    app.add_directive(
            "annotated-image",
            AnnotatedImageDirective,
            1,
            (3,0,0)
            )

    app.add_directive(
            "annotation",
            AnnotationDirective,
            1,
            (4,0,0)
            )

    app.add_node(AnnotatedImage, html=(AnnotatedImage.visit, AnnotatedImage.depart))
    app.add_node(Annotation, html=(Annotation.visit, Annotation.depart))


