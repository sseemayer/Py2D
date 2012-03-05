"""Math utilities for games"""
import math

class Vector(object):
	"""Class for 2D Vectors.
	
	Vectors v have an x and y component that can be accessed multiple ways:

		- v.x, v.y
		- v[0], v[1]
		- x,y = v.as_tuple()

	"""

	def __init__(self, x, y):
		"""Create a new vector object.

		@type x: float
		@param x: The X component of the vector

		@type y: float
		@param y: The Y component of the vector
		"""

		self.x = x
		self.y = y


	def get_length(self):
		"""Get the length of the vector."""
		return math.sqrt(self.get_length_squared())

	def get_length_squared(self):
		"""Get the squared length of the vector, not calculating the square root for a performance gain"""
		return self.x * self.x + self.y * self.y;
	
	def normalize(self):
		"""Return a normalized version of the vector that will always have a length of 1."""
		return self / self.get_length()

	def clamp(self):
		"""Return a vector that has the same direction than the current vector, but is never longer than 1."""
		if self.get_length() > 1:
			return self.normalize()
		else:
			return self
	
	def clone(self):
		"""Return a copy of this vector"""
		return Vector(self.x, self.y)

	def as_tuple(self):
		"""Convert the vector to a non-object tuple"""
		return (self.x, self.y)

	def __add__(self, b):
		return Vector(self.x + b.x, self.y + b.y)
	
	def __sub__(self, b):
		return Vector(self.x - b.x, self.y - b.y)

	def __mul__(self, val):

		if isinstance(val, Vector):
			return self.x * val.x + self.y * val.y
		else:
			return Vector(self.x * val, self.y * val)
	
	def __div__(self, val): 
		return Vector(self.x / val, self.y / val)

	def __repr__(self):
		return "Vector(%f, %f)" % (self.x, self.y)
	
	def __eq__(self, other):
		d = self - other
		return abs(d.x) <  0.0001 and abs(d.y) < 0.0001


	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash("%.4f %.4f" % (self.x, self.y))

	def __getitem__(self, key):
		if key == 0: return self.x
		elif key == 1: return self.y
		else: raise KeyError('Invalid key: %s. Valid keys are 0 and 1 for x and y' % key)

	def __setitem__(self, key, value):
		if key == 0: self.x = value
		elif key == 1: self.y = value
		else: raise KeyError('Invalid key: %s. Valid keys are 0 and 1 for x and y' % key)

	length = property(get_length, None, None)
	length_squared = property(get_length_squared, None, None)

class Polygon(object):
	"""Class for 2D Polygons.
	
	A Polgon behaves like a list of points, but the last point in the list is assumed to be connected back to the first point.
	"""

	def __init__(self):
		"""Create a new, empty Polygon object"""
		self.points = []

	@staticmethod
	def regular(center, radius, points):
		"""Create a regular polygon

		@type center: Vector
		@param center: The center point of the polygon

		@type radius: float
		@param radius: The radius of the polygon

		@type points: int
		@param points: The number of polygon points. 3 will create a triangle, 4 a square, and so on.
		"""

		angular_increment = 2 * math.pi / points

		p = Polygon()
		for i in range(points):
			p.add_point( Vector(center.x + radius * math.cos(i * angular_increment), center.y + radius * math.sin(i * angular_increment)) )

		return p

	@staticmethod
	def from_pointlist(points):
		"""Create a polygon from a list of points
		
		@type points: List
		@param points: List of Vectors that make up the polygon
		"""

		p = Polygon()
		p.points = points
		return p

	def add_point(self, point):
		"""Add a new point at the end of the polygon
		
		@type point: Vector
		@param point: The new Vector to add to the polygon
		"""
		self.points.append(point)

	def add_points(self, points):
		"""Add multiple new points to the end of the polygon
		
		@type points: List
		@type points: A list of Vectors to add
		"""
		self.points.extend(points)

	def get_centerpoint(self):
		"""Get the center of mass for the polygon"""

		xes = [p.x for p in self.points]
		yes = [p.y for p in self.points]

		return Vector(sum(xes) / len(xes), sum(yes) / len(yes) )

	def sort_around(self, center):
		"""Re-order points by their angle with respect to a certain center point"""

		def angle_from_origin(p):
			phi = math.acos(p.x / p.get_length())
			if p.y < 0: phi = 2 * math.pi - phi
			return phi 
	
	
		self.points.sort(key=lambda p: angle_from_origin(p - center))

	def __repr__(self):
		pts = ["(%.2f, %.2f)" % (p.x, p.y) for p in self.points]
		return "Polygon [%s]" % ", ".join(pts)

	def __getitem__(self, key):
		return self.points[key]

	def __setitem__(self, key, value):
		self.points[key] = value

	def __delitem__(self, key):
		del self.points[key]

	def __len__(self):
		return len(self.points)

	def __eq__(self, other):
		if not isinstance(other, Polygon): return False
		return self.points == other.points

	def clone(self):
		"""Return a shallow copy of the polygon (points are not cloned)"""
		poly = Polygon()
		poly.points = [ p for p in self.points ]
		return poly

	append = add_point
	extend = add_points

	center = property(get_centerpoint)

def __intersect_line_line_u(p1, p2, q1, q2):

	d = (q2.y - q1.y) * (p2.x - p1.x) - (q2.x - q1.x) * (p2.y - p1.y)
	n1 = (q2.x - q1.x) * (p1.y - q1.y) - (q2.y - q1.y) * (p1.x - q1.x)
	n2 = (p2.x - p1.x) * (p1.y - q1.y) - (p2.y - p1.y) * (p1.x - q1.x)

	if d == 0: return None

	u_a = float(n1) / d
	u_b = float(n2) / d

	return (u_a, u_b)

def intersect_poly_lineseg(poly_points, p1, p2):
	"""Intersect a polygon and a line segment.

	@type poly_points: List
	@param poly_points: The list of points in the polygon
	
	@type p1: Vector
	@param p1: The starting point of the line segment

	@type p2: Vector
	@type p2: The ending point of the line segment

	@return: The list of intersection points or an empty list
	"""
	return intersect_linesegs_lineseg(zip(poly_points[0:], poly_points[1:]) + [(poly_points[-1], poly_points[0])], p1, p2)

def intersect_poly_ray(poly_points, p1, p2):
	"""Intersect a polygon and a ray

	@type poly_points: List
	@param poly_points: The list of points in the polygon
	
	@type p1: Vector
	@param p1: The starting point of the ray

	@type p2: Vector
	@param p2: The ending point of the ray
	
	@return: The list of intersection points or an empty list
	"""
	return intersect_linesegs_ray(zip(poly_points[0:], poly_points[1:]) + [(poly_points[-1], poly_points[0])], p1, p2)

def intersect_line_line(p1, p2, q1, q2):
	"""Intersect two lines

	@type p1: Vector
	@param p1: The first point of the first line

	@type p2: Vector
	@type p2: The second point of the first line
	
	@type q1: Vector
	@param q1: The first point of the second line

	@type q2: Vector
	@type q2: The second point of the second line

	@return: The point of intersection or None
	"""

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) ) 

def intersect_lineseg_line(p1, p2, q1, q2):
	"""Intersect a line segment and a line
	
	@type p1: Vector
	@param p1: The starting point of the line segment

	@type p2: Vector
	@type p2: The ending point of the line segment

	@type q1: Vector
	@param q1: The first point on the line 

	@type q2: Vector
	@type q2: The second point on the line
	
	@return: The point of intersection or None
	"""

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	if ll[0] < 0 or ll[0] > 1: return None

	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) ) 

def intersect_lineseg_ray(p1, p2, q1, q2):
	"""Intersect a line segment and a ray
	
	@type p1: Vector
	@param p1: The starting point of the line segment

	@type p2: Vector
	@type p2: The ending point of the line segment

	@type q1: Vector
	@param q1: The first point on the ray

	@type q2: Vector
	@type q2: The second point on the ray
	
	@return: The point of intersection or None
	"""

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	if ll[0] < 0 or ll[0] > 1: return None
	if ll[1] < 0: return None

	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) ) 

def intersect_linesegs_ray(segs, p1, p2):
	"""Intersect a list of line segments and a ray
	
	@type segs: List
	@param segs: The list of line segments, i.e. a list of 2-tuples of vectors

	@type p1: Vector
	@param p1: The first point on the ray

	@type p2: Vector
	@type p2: The second point on the ray
	
	@return: The list of intersections or an empty list 
	"""
	intersect_points = []

	for line_segment in segs:
		intersect = intersect_lineseg_ray(line_segment[0], line_segment[1], p1, p2)
		if intersect:
			if line_segment[0] != p2 and line_segment[1] != p2:
				intersect_points += [intersect]

	return intersect_points

def intersect_linesegs_lineseg(segs, p1, p2):
	"""Intersect a list of line segments and a line segment
	
	@type segs: List
	@param segs: The list of line segments, i.e. a list of 2-tuples of vectors

	@type p1: Vector
	@param p1: The first point on the line segment

	@type p2: Vector
	@type p2: The second point on the line segment
	
	@return: The list of intersections or an empty list 
	"""
	intersect_points = []

	for line_segment in segs:
		intersect = intersect_lineseg_lineseg(line_segment[0], line_segment[1], p1, p2)
		if intersect:
			if line_segment[0] != p2 and line_segment[1] != p2:
				intersect_points += [intersect]
	
	return intersect_points

def intersect_poly_poly(poly_points1, poly_points2):
	"""Intersect two polygons

	@type poly_points1: List
	@param poly_points1: The list of points of polygon 1

	@type poly_points2: List
	@param poly_points2: The list of points of polygon 2
	
	@return: The list of intersections or an empty list 
	"""

	return intersect_linesegs_linesegs(zip(poly_points1[0:], poly_points1[1:]) + [(poly_points1[-1], poly_points1[0])], zip(poly_points2[0:], poly_points2[1:]) + [(poly_points2[-1], poly_points2[0])])

def intersect_linesegs_linesegs(segs1, segs2):
	"""Intersect two lists of line segments
	
	@type segs1: List
	@param segs1: The first list of line segments, i.e. a list of 2-tuples of vectors

	@type segs2: List
	@param segs2: The second list of line segments, i.e. a list of 2-tuples of vectors
	
	@return: The list of intersections or an empty list 
	"""
	intersect_points = []
	for ls1 in segs1:
		intersect_points += intersect_linesegs_lineseg(segs2, ls1[0], ls1[1])

	return intersect_points

def intersect_lineseg_lineseg(p1, p2, q1, q2):
	"""Intersect two line segments

	@type p1: Vector
	@param p1: The first point on the first line segment

	@type p2: Vector
	@type p2: The second point on the first line segment


	@type q1: Vector
	@param q1: The first point on the secondline segment

	@type q2: Vector
	@type q2: The second point on the second line segment
	"""

	if max(q1.x, q2.x) < min(p1.x, p2.x): return None
	if min(q1.x, q2.x) > max(p1.x, p2.x): return None
	if max(q1.y, q2.y) < min(p1.y, p2.y): return None
	if min(q1.y, q2.y) > max(p1.y, p2.y): return None

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return None
	if ll[0] < 0 or ll[0] > 1: return None
	if ll[1] < 0 or ll[1] > 1: return None

	return Vector(p1.x + ll[0] * (p2.x - p1.x) , p1.y + ll[0] * (p2.y - p1.y) ) 

def check_intersect_lineseg_lineseg(p1, p2, q1, q2):
	"""Check if two line segments intersect - this can conserve memory if we don't need the intersection points

	@type p1: Vector
	@param p1: The first point on the first line segment

	@type p2: Vector
	@type p2: The second point on the first line segment


	@type q1: Vector
	@param q1: The first point on the secondline segment

	@type q2: Vector
	@type q2: The second point on the second line segment

	"""

	if max(q1.x, q2.x) < min(p1.x, p2.x): return False
	if min(q1.x, q2.x) > max(p1.x, p2.x): return False
	if max(q1.y, q2.y) < min(p1.y, p2.y): return False
	if min(q1.y, q2.y) > max(p1.y, p2.y): return False

	ll = __intersect_line_line_u(p1, p2, q1, q2)

	if ll == None: return False
	if ll[0] < 0 or ll[0] > 1: return False
	if ll[1] < 0 or ll[1] > 1: return False

	return True

def distance_point_lineseg_squared(p, a, b):
	"""Get the shortest distance from a point to a line segment.

	This can either be a perpendicular to a point on the line segment or the straight connection of p to one of the end points.

	@type p: Vector
	@param p: The point to compare to the line segment

	@type a: Vector
	@param a: The first point on the first line segment

	@type b: Vector
	@type b: The second point on the first line segment
	"""

	ap_squared = (p - a).get_length_squared()
	bp_squared = (p - b).get_length_squared()
	ap_prime = a * b
	
	perpendicular_squared = abs( ap_squared - ap_prime * ap_prime )

	return min(ap_squared, bp_squared, perpendicular_squared)


VECTOR_NULL = Vector(0,0)

