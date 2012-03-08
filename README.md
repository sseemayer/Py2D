Py2D game utility library
=========================

Py2D attempts to help game developers with commonly found tasks, especially in vector-based games.

The library is still in very early development, supported features so far are:

* Classes for Vectors, Polygons and Affine Transformations with basic operations
* Polygonal Field-of-Vision Calculation
* Generate polygon obstructors from tile map data
* Perform boolean operations (union, intersection, difference) on polygons
* Grow and shrink polygons (polygon buffering, polygon offsetting)

Getting Started
---------------

You can see some functionality of Py2D in the examples package. Just run the script run_examples.py.

	$ python2 run_examples.py -e EXAMPLE_NAME

Example names are given as Packagename.Classname - Valid example names are:

* Logo.Logo - A bouncing Py2D logo made of vectors. Neat!
* Draw.Draw - Draw polygons using the mouse
* Math.Boolean - Demonstrate boolean operations on polygons
* Math.Offset - Demonstrate polygon offsetting (also known as polygon buffering)
* FOV.FOV - Field of View calculation

If you get lost, press F1 in the example runner to display a help text. And remember to use the source, Luke!
