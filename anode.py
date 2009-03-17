
from docutils import nodes
from docutils.parsers.rst import directives, Directive

import os
import hashlib
import posixpath

# Nodes
# -----

class AnnotatedImage(nodes.image):

    @staticmethod
    def visit(visitor, node):
        
        olduri = node['uri']
        # rewrite the URI if the environment knows about it
        if olduri in visitor.builder.images:
            node['uri'] = posixpath.join(visitor.builder.imgpath,
                                         visitor.builder.images[olduri])

        # Create the div which will display the image
        visitor.body.append(
                visitor.starttag(
                    node,
                    "div",
                    style="position: relative; width: %spx; height: %spx; background-image: url(%s)"
                                % ( node.width, node.height, node['uri'] )
                    )
                )

        # Create the divs which represent the regions of the image to annotate.
        for child in node.children:

            if hasattr( child, "annotation_info" ):

                info = child.annotation_info()

                div_style =  "position: absolute;"
                div_style += "top: %spx;" % info["top"]
                div_style += "left: %spx;" % info["left"]

                a_style = "height: %spx;" % info["height"]
                a_style += "width: %spx;" % info["width"]
                a_style += "border: 2px solid transparent;"
                a_style += "cursor: pointer;"
                a_style += "display: block;"

                name_style = "padding: 2px; display: none; background-color: black; color: white; font-size: x-small;"
                    
                a_mouseover = "$('#" + info["id"] + "').css('background-color', '#ffffaa');"
                a_mouseover += "$(this).css('border-color','black');"
                a_mouseout = "$('#" + info["id"] + "').css('background-color', 'transparent');"
                a_mouseout += "$(this).css('border-color', 'transparent');"
                
                if info["name"]:
                    name_id = info["id"] + "_name"
                    a_mouseover += "$('#" + name_id + "').css('display','inline');"
                    a_mouseout += "$('#" + name_id + "').css('display','none');"

                visitor.body.append(visitor.starttag(node, "div", style=div_style))
                visitor.body.append(
                        visitor.starttag(
                            node,
                            "a",
                            style=a_style,
                            onmouseout=a_mouseout,
                            onmouseover=a_mouseover
                            )
                        )
                visitor.body.append("</a>")

                # If a name is specfied then add that
                if info["name"]:
                    name_id = info["id"] + "_name"
                    visitor.body.append(visitor.starttag(node, "div"))
                    visitor.body.append(visitor.starttag(node, "span", ids=[name_id], style=name_style))
                    visitor.body.append(info["name"]);
                    visitor.body.append("</span>")
                    visitor.body.append("</div>")

                visitor.body.append("</div>\n")

        visitor.body.append("</div>\n")
        visitor.body.append("\n")

    @staticmethod
    def depart(visitor, node):
        pass



class Annotation(nodes.General, nodes.Element):

    def annotation_info(self):

        return dict(
                id=self.hashid,
                name=self.name,
                top=self.top,
                left=self.left,
                height=self.height,
                width=self.width
                )

    @staticmethod
    def visit(visitor, node):

        # Create the div with the desired id
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
    option_spec = {'name': directives.unchanged }

    # Have to use a list as using a integer to simply count seems to be reset each time
    hashes = []

    def run(self):

        annotation = Annotation()
        
        # Generate an id for the div
        annotation.hashid = hashlib.sha1(str(len(self.hashes))).hexdigest()
        self.hashes.append(annotation.hashid)

        annotation.top = self.arguments[0]
        annotation.left = self.arguments[1]
        annotation.height = self.arguments[2]
        annotation.width = self.arguments[3]

        try: 
            annotation.name = self.options["name"]
        except KeyError:
            annotation.name = None

        # Parse the children
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


