---
title: Convex Decomposition
layout: default
root: ../../
---

# Convex Decomposition

From a Polygon <code>p</code> and a list of holes <code>holes</code>, you can compute a decomposition of <code>p</code> into a set of convex polygons:

{% highlight python %}
>>> result = Polygon.convex_decompose(p, holes)
{% endhighlight %}

The result will be a list of convex polygons or an empty list if self-intersections were found.
