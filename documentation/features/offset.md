---
title: Polygon Offsetting
layout: default
root: ../../
---

# Polygon Offsetting

You can offset a list of <code>Polygon</code>s <code>polys</code> by an amount <code>amount</code> like this:

{% highlight python %}
>>> result = Polygon.offset(polys, amount)
{% endhighlight %}

Again, the return variable will be a list of <code>Polygon</code>s since offsetting may create additional polygons.

Positive values for <code>amount</code> result in a growing of the polygons, negative values result in shrinking by that amount.

You may specify an optional <code>tip_decorator</code> argument which takes a reference to a tip decorator function of the type <code>f(a,b, c,d, is_cw)</code>. The tip decorator function will return a list of additional vertices to insert between the line segments (a,b) and (c,d) to make them look nicer. The <code>is_cw</code> variable specifies the orientation of the line segments. As an example for a tip decorator function, have a look at the default "pointy" tip decorator from the Py2D source:


{% highlight python %}
def tip_decorator_pointy(a,b, c,d, is_cw):
	intersection = intersect_line_line(a,b,c,d)
	return [intersection]
{% endhighlight %}

