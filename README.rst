
Anode Project
=============

This project is aimed at creating restructed text directives for annotating
images. The inital drive is towards creating a Sphinx extension.

Features
--------

* Directives for annotating images
* A standalone web page for generating the rst syntax

Status
------

A basic implementation of the directives is in place and working. 

The web page works and is useful but looks mighty ugly.

Syntax
------

This project introduces two rst directives::

   .. annotated-image:: <height> <width> <image src>

and::

   .. annotation:: <top> <left> <height> <width>
      :name: Optional name

      Text to associate with the specified region of the image.


The ``annotation`` directives should be nested within the ``annotated-image``
block.

