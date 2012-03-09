---
layout: default
title: Getting Started
root: ../
---

Getting Started
===============

Py2D has the following requirements:

* Python 2.7 (it might work on older pythons, but I did not test it)
* pygame (only if you would like to run the examples!)

After installing the requirements, download Py2D onto your local machine and run some examples. 
Then check out the <a href="{{ page.root }}documentation.html">Documentation</a> or the examples' source code.

Running examples
----------------

You can see some functionality of Py2D in the examples package. Just run the script run_examples.py.

	$ python2 run_examples.py -e EXAMPLE_NAME

Example names are given as <code>Packagename.Classname</code> - Valid example names are:

* **Logo.Logo** - A bouncing Py2D logo made of vectors. Neat!
* **Draw.Draw** - Draw polygons using the mouse
* **Math.Boolean** - Demonstrate boolean operations on polygons
* **Math.Offset** - Demonstrate polygon offsetting (also known as polygon buffering)
* **FOV.FOV** - Field of View calculation

If you get lost, press F1 in the example runner to display a help text. And remember to use the source, Luke!
