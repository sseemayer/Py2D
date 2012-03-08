"""Navigation Mesh generation and navigation."""

import Math

def poly_midpoint_distance(poly_a, poly_b):
	"""Polygon distance function that takes the euclidean distance between polygon midpoints."""
	return (poly_a.get_centerpoint() - poly_b.get_centerpoint()).length

class Mesh(object):
	"""Class for representing a navigation mesh"""

	def __init__(self):
		"""Create a new, empty navigation mesh"""
		self._polygons = []
		self._nodes = []
	
	@staticmethod
	def generate(boundary, walls=[], distance_function=poly_midpoint_distance):
		"""Generate a new navigation mesh from a boundary polygon and a list of walls.

		The method will delete wall areas from the boundary polygon and then decompose the resulting polygon into convex polygons, generating a navigation graph in the process.

		@type boundary: Polygon
		@param boundary: The boundary of the navigable area.

		@type walls: List
		@param walls: List of Wall Polygons to subtract from the boundary polygon. These may intersect the polygon boundary or be properly inside the polygon.

		@type distance_function: Function
		@param distance_function: Function of the type f(p_a, p_b) that returns the distance between polygon objects p_a and p_b according to some metric.
		"""
		raise NotImplementedError()
	

class Node(object):
	"""Node in a navigation mesh"""
	def __init__(self, polygon):
		self.polygon = polygon

class NavPolygon(Math.Polygon):
	"""Polygon class with added navigation data"""
	def __init__(self):
		Math.Polygon.__init__(self)
		self.nodes = []
	



