Py2D game utility library
=========================

Py2D attempts to help game developers with commonly found tasks, especially in vector-based games.

The library is still in very early development, among the features so far are:

* Classes for Vectors, Polygons and Affine Transformations with basic operations
* Polygonal Field-of-Vision Calculation
* Generate polygon obstructors from tile map data
* Perform boolean operations (union, intersection, difference) on polygons
* Grow and shrink polygons (polygon buffering, polygon offsetting)
* Decompose polygons into convex parts

To learn more about features and how to get started, check out the [Py2D website](http://sseemayer.github.com/Py2D)!


Cython support
--------------
Parts of Py2D can now be compiled to C modules using Cython. If you do a setup.py build install, 
you should get binary versions of the supported modules. Alternatively, for development, you can 
compile in-place by running

	$ python setup.py build_ext --inplace


License (2-clause BSD)
----------------------

Copyright (c) 2012, Stefan Seemayer
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
