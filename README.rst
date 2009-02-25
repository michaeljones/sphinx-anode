
Anode Project
=============

This project is aimed at creating restructed text directives for annotating
images.

Features
--------

* Directives for annotating images
* A standalone web page for generating the rst syntax

Status
------

A basic implementation of the directives is in place and working. 

The web page is still in development.

Syntax
------

This project introduces two rst directives::

   .. annotated-image:: <height> <width> <image src>

and::

   .. annotation:: <top> <left> <height> <width>

      Text to associate with the specified region of the image.


The ``annotation`` directives should be nested within the ``annotated-image``
block.
