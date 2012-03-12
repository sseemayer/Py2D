---
title: Boolean Operations
layout: default
root: ../../
---

# Boolean operations

With two polygons <code>a</code> and <code>b</code>, you can compute boolean operations like this:

{% highlight python %}
>>> union = Polygon.union(a,b)
>>> intersection = Polygon.intersect(a,b)
>>> difference = Polygon.subtract(a,b)
{% endhighlight %}

The return values will be lists of <code>Polygon</code>s since the boolean operations can yield multiple result polygons.

<!--
vim: filetype=markdown
-->
