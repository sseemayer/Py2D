---
title: Navigation
layout: default
root: ../../
---

# Navigation

Py2D navigation code is contained in the py2d.Navigation package. You can generate a <code>NavMesh</code> object from polygonal navigation data with holes using the function <code>NavMesh.generate</code>:

{% highlight python %}
>>> mesh = NavMesh.generate(boundary, holes)
{% endhighlight %}

This will automatically calculate optimal paths between all polygons in the generated navigation mesh.

## Pathfinding

With the navigation mesh generated, you can query the mesh for paths. Simply use the <code>get_path</code> method to find the optimal path from Vector v to Vector w:

{% highlight python %}
>>> path = mesh.get_path(v,w) 
{% endhighlight %}

If a path between the two vectors can be solved by the mesh, <code>get_path</code> will return a <code>NavPath</code> object that contains the sequence of polygons to traverse. You can also call <code>get_path</code> with two polygons instead of vectors.

## Path following

You can use the <code>NavPath</code> object to generate the actual vertices an agent will have to walk to in order to reach their target as they are needed. Simply call <code>get_next_move_to</code> everytime you arrive at a target vector and you will receive the next target.

A simple agent moving along a NavPath <code>self.path</code> from <code>self.position</code> to <code>self.goal</code> might have the following per-frame update code:

{% highlight python %}
def update(self, time_elapsed):
	if not self.move_to and (self.position - self.goal).length_squared > 0.1:
		self.move_to = self.path.get_next_move_to(self.position, self.goal)

	if self.move_to: 
		direction = self.move_to - self.position
		self.position += direction.clamp() * (time_elapsed * self.speed)		
		if (self.position - self.move_to).length_squared < 0.0001: 
			self.move_to = None
{% endhighlight %}


<!--
vim: filetype=markdown
-->
