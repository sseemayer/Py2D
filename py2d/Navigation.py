"""Navigation Mesh generation and navigation."""

import Math

from collections import defaultdict

def poly_midpoint_distance(poly_a, poly_b):
	"""Polygon distance function that takes the euclidean distance between polygon midpoints."""
	return (poly_a.get_centerpoint() - poly_b.get_centerpoint()).length

class NavMesh(object):
	"""Class for representing a navigation mesh"""

	def __init__(self, polygons):
		"""Create a new navigation mesh"""
		self._polygons = polygons
		self.update_nav()
	
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

		convex_decomp = Math.Polygon.convex_decompose(boundary, walls)

		# make NavPolygons out of the convex decomposition polygons
		polygons = [NavPolygon(poly) for poly in convex_decomp]

		# create dict of shared edges
		polygon_edges = defaultdict(list)
		for poly in polygons:
			for a,b in zip(poly, poly[1:]) + [(poly[-1],poly[0])]:
				c,d = (a,b) if a.x < b.x or (a.x == b.x and a.y < b.y ) else (b,a)
				polygon_edges[(c,d)].append(poly)

		# link polys that share edges
		for e, polys in polygon_edges.iteritems():
			for i, p_a in enumerate(polys):
				for p_b in polys[i+1:]:
					
					dist = distance_function(p_a, p_b)

					p_a.neighbors[p_b] = dist
					p_b.neighbors[p_a] = dist

		return NavMesh(polygons)


	def update_nav(self):
		"""Pre-compute navigation data for the navigation mesh.
		
		This is called automatically upon mesh initialization, but you might want to call it if you have changed the navigation mesh.
		"""

		# initialize with simple distances
		self._nav_data = [[ (self._polygons[i].neighbors[p],j) if p in self._polygons[i].neighbors.keys() else (float('inf'),-1) for j,p in enumerate(self._polygons) ] for i in range(len(self._polygons))]

		# floyd-warshall algorithm to compute all-pair shortest paths
		for k in range(len(self._polygons)):
			for i in range( len(self._polygons) ):
				for j in range(len(self._polygons)):
					
					if k not in (i,j) and i != j:
						dist  = self.get_data(i,j)[0]
						dist2 = self.get_data(i,k)[0] + self.get_data(k,j)[0]
						if dist2 < dist: 
							self.set_data(i,j, (dist2, k))

	def find_polygon(self, p):
		"""Find the NavPolygon that contains p"""
		for poly in self._polygons:
			if poly.contains_point(p):
				return poly

		return None


	def get_path(self, start, stop):
		"""Get a high-level path from start to stop.

		The path returned will be an optimal sequence of NavPolygons leading to the desired target.
		"""
		
		if isinstance(start, Math.Vector): start = self.find_polygon(start)
		if isinstance(stop, Math.Vector): stop = self.find_polygon(stop)

		if not (start and stop): return None

		def get_path_rec(i,j):
			d = self.get_data(i,j)[1]
			if d == j:
				return [j]
			else: 
				return get_path_rec(i,d) + get_path_rec(d,j)

		i = self._polygons.index(start)
		j = self._polygons.index(stop)

		out = [i] + get_path_rec(i,j)

		return [self._polygons[i] for i in out]

	def get_data(self, i, j):
		return self._nav_data[i][j]

	def set_data(self, i, j, d):
		self._nav_data[i][j] = d

	def get_polygons(self):
		return self._polygons

	def get_nodes(self):
		return self._nodes

	polygons = property(get_polygons)
	nodes = property(get_nodes)


class NavPolygon(Math.Polygon):
	"""Polygon class with added navigation data"""
	def __init__(self, polygon):
		Math.Polygon.__init__(self)
		
		self.points = polygon.points
		self.neighbors = {}

	



