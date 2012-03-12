---
title: Field of Vision
layout: default
root: ../../
---

# Field of Vision

{% include toc.html %}

FOV calculation in Py2D is handled by the <code>py2d.FOV.Vision</code> class. It manages obstructor data and caching for the vision polygon.

Obstructor data is passed as a list of line strips, i.e. a list of lists of <code>Vector</code>s:

{% highlight python %}
>>> obstructors = [
... 	[ Vector(1,3), Vector(3, 4), ... ],
...	[ Vector(4,10), Vector(7,5), ... ],
... ]
{% endhighlight %}

If you want to specify polygons as obstructors, you have to close the line strips manually by adding the first Vector to the end of the list.

With the obstructor data at hand, you can create a new <code>Vision</code> object:

{% highlight python %}
>>> vision = Vision(obstructors)
{% endhighlight %}

So far, Py2D has no special handling for moving obstructors - just re-set the obstructors using the <code>set_obstructors</code> method on the <code>Vision</code> instance. Right now, the obstructor data is write-only since it will be converted into a more computationally efficient representation.

## Updating the Field of Vision
Everytime your scene changes, you will want to calculate a new vision polygon. To do so, you need the <code>eye</code> position and a <code>boundary</code> polygon with a given <code>radius</code>.

In this example, we will create a 16-point polygon around the eye position as our boundary polygon and give it our vision radius as a radius:

{% highlight python %}
>>> boundary = Polygon.regular(eye, radius, 16)
{% endhighlight %}

We can then get the vision polygon like this:

{% highlight python %}
>>> vision = vision.get_vision(eye, radius, boundary)
{% endhighlight %}


## FOV for tile-based maps

If you are creating a game with tiled maps, the <code>py2d.FOVConverter</code> package might interest you. It contains a converter for generic tile-based maps into obstructor data that can be used for <code>Vision</code> objects.

For example, if you have a map data structure in <code>map</code> with 

* a function <code>map.get_block_light(x,y)</code> to determine whether the tile at x,y blocks light, 
* a width of <code>map.width</code> tiles and a height of <code>map.height</code> tiles and 
* tiles are <code>tile_width</code> pixels wide and <code>tile_height</code> pixels high, 

you can generate obstructor data like this:


{% highlight python %}
>>> blocking_function = lambda x,y: map.get_block_light(x,y)
>>> obstructors = convert_tilemap(
...	map.width, map.height, 
...	blocking_function, 
...	tile_width, tile_height
... )
{% endhighlight %}

<!--
vim: filetype=markdown
-->
