---
title: Math Functions
layout: default
root: ../../
---


# Math functions

Py2D has classes for <code>Vector</code>s, <code>Polygon</code>s and Affine <code>Transform</code>ations. 
The following sections will outline some of the common use cases of these classes.

{% include toc.html %}


## Vector

Vectors in Py2D are always two-dimensional and can have <code>int</code> or <code>float</code> components. You can initialize them like this:

{% highlight python %}
>>> v = Vector(3.0, 2.0)
{% endhighlight %}

### Vector components

You can access a <code>Vector</code>'s components using a variety of ways:

{% highlight python %}

>>> v.x, v.y
(3.0, 2.0)

>>> x,y = v[0], v[1]
(3.0, 2.0)

>>> v.as_tuple()
(3.0, 2.0)

>>>v.x = 10
>>>v[0] = 10

{% endhighlight %}

### Vector arithmetic

The <code>Vector</code> class has all the important arithmetic operators overridden:

{% highlight python %}

>>> u = Vector(3.0, 4.0)
>>> v = Vector(1.0, 7.0)

>>> u + v
Vector(4.000, 11.000)

>>> u - v
Vector(2.000, -3.000)

>>> u * 2
Vector(6.000, 8.000)

>>> u / 2
Vector(1.500, 2.000)

>>> u * v	# this is the dot product.
31

{% endhighlight %}

### Vector equality

Vectors are defined as equal if the differences of their x and y values are both smaller than <code>Math.EPSILON</code> (i.e. 0.0001):

{% highlight python %}
>>> u = Vector(3.0, 4.0)
>>> v = Vector(1.0, 2.0)
>>> w = Vector(2.0, 2.0)

>>> u == v, u == w, v == w
(False, False, False)

>>> u == v + w
True

{% endhighlight %}

### Vector length and normalization

The <code>length</code> and <code>length_squared</code> properties give the vector's length. To normalize to a length of 1, use <code>normalize</code>. To normalize to a length of 1 or smaller, use <code>clamp</code>.

{% highlight python %}
>>> u = Vector(3.0, 4.0)
>>> v = Vector(0.5, 0)
>>> u.length, u.length_squared
(5.0, 25.0)

>>> u.normalize()
Vector(0.600, 0.800)

>>> v.normalize()
Vector(1.000, 0.000)

>>> u.clamp()
Vector(0.600, 0.800)

>>> v.clamp()
Vector(0.500, 0.000)


{% endhighlight %}

### Derived vectors

You can <code>clone</code> vectors and get <code>normal</code> vectors easily:

{% highlight python %}
>>> u = Vector(3.0, 4.0)
>>> u.clone()
Vector(3.000, 4.000)

>>> u.normal()
Vector(-4.000, 3.000)

{% endhighlight %}



## Polygon

In Py2D, <code>Polygon</code>s are essentially list of <code>Vector</code>s. We normally assume that the polygon is closed, i.e. that the last Vector will be connected to the first Vector.

There are multiple ways of constructing polygons:

{% highlight python %}
>>> p = Polygon()
>>> q = Polygon.regular(center, radius, points)
>>> r = Polygon.from_pointlist([ Vector(1,2), Vector(2,1), Vector(0,0) ])
>>> s = Polygon.from_tuples([ (1,2), (2,1), (0,0) ])
{% endhighlight %}

### Points on the polygon

The list of points is accessible by the <code>points</code> property. Alternatively, you may use <code>add_point</code> to add one point to the end of the polygon, or <code>add_points</code> to add multiple points.

You can check whether the polygon contains a certain point by using the <code>contains_point</code> function:

{% highlight python %}
>>> s = Polygon.from_tuples([ (0,0), (3,2), (1,3) ])
>>> s.contains_point(Vector(2,2))
True
{% endhighlight %}

### Polygon orientation, convexity

A polygon may be oriented either clock-wise or counter-clockwise. You can test using the <code>is_clockwise</code> function or get a new clockwise or counter-clockwise copy using the <code>clone_cw</code> and <code>clone_ccw</code> functions:

{% highlight python %}
>>> p = Polygon.from_tuples([ (1,2), (2,1), (0,0) ])
>>> p.is_clockwise()
False

>>> q = Polygon.from_tuples([ (0,0), (2,1), (1,2) ])
>>> q.is_clockwise()
True

>>> p.clone_cw()
Polygon([ (1,2), (2,1), (0,0) ])

>>> q.clone_ccw()
Polygon([ (1,2), (2,1), (0,0) ])

{% endhighlight %}


Additionally, a polygon may be convex or concave. You can test for convexity using the <code>is_convex</code> function:

{% highlight python %}
>>> s = Polygon.from_tuples([ (0,0), (10,0), (10,10), (5,5), (0,10)])
>>> s.is_convex()
False

>>> del s.points[-2]
>>> s.is_convex()
True
{% endhighlight %}


## Transform

{% highlight python %}

{% endhighlight %}
<!--
vim: filetype=markdown
-->
