"""Math utilities for games"""
import math

from collections import defaultdict

def tip_decorator_pointy(a,b,c,d,is_cw):
	intersection = intersect_line_line(a,b,c,d) 
	return [intersection] 

def tip_decorator_flat(a,b,c,d,is_cw):
	return []

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
	
	def get_slope(self):
		"""Get the slope of the vector, or float('inf') if x == 0"""
		if self.x == 0: return float('inf')
		return float(self.y)/self.x

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

	def normal(self):
		"""Return a normal vector of this vector"""
		return Vector(-self.y, self.x)

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
		return "Vector(%.3f, %.3f)" % (self.x, self.y)
	
	def __eq__(self, other):
		if not isinstance(other, Vector): return False
		d = self - other
		return abs(d.x) < EPSILON and abs(d.y) < EPSILON 

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

	slope = property(get_slope, None, None)

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

	@staticmethod
	def from_tuples(tuples):
		"""Create a polygon from 2-tuples

		@type tuples: List
		@param tuples: List of tuples of x,y coordinates
		"""

		p = Polygon()
		p.points = [ Vector(t[0], t[1]) for t in tuples ]
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
		@param points: A list of Vectors to add
		"""
		self.points.extend(points)

	def get_centerpoint(self):
		"""Get the center of mass for the polygon"""

		xes = [p.x for p in self.points]
		yes = [p.y for p in self.points]

		return Vector(float(sum(xes)) / len(xes), float(sum(yes)) / len(yes) )

	def sort_around(self, center):
		"""Re-order points by their angle with respect to a certain center point"""

		def angle_from_origin(p):
			phi = math.acos(float(p.x) / p.get_length())
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

	def clone_ccw(self):
		p = self.clone()
		if p.is_clockwise(): p.flip()
		return p

	@staticmethod
	def boolean_operation(polygon_a, polygon_b, operation):
		"""Perform a boolean operation on two polygons.

		Reference:
		Avraham Margalit. An Algorithm for Computing the Union, Intersection or Difference of Two Polygons. 
		Comput & Graphics VoI. 13, No 2, pp 167-183, 1989

		This implementation will only consider island-type polygons, so control tables are replaced by small boolean expressions.
	
		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon

		@type operation: char
		@param operation: The operation to perform. Either 'u' for union, 'i' for intersection, or 'd' for difference.
		"""

		def inorder_extend(v, v1, v2, ints):
			"""Extend a sequence v by points ints that are on the segment v1, v2"""

			k, r = None, False
			if v1.x < v2.x:
				k = lambda i: i.x
				r = True
			elif v1.x > v2.x:
				k = lambda i: i.x
				r = False
			elif v1.y < v2.y:
				k = lambda i: i.y
				r = True
			else:
				k = lambda i: i.y
				r = False

			l = [ (p, 2) for p in sorted(ints, key=k, reverse=r) ]

			i = next((i for i, p in enumerate(v) if p[0] == v2), -1)
			assert(i>=0)

			for e in l:
				v.insert(i, e)

		if operation not in 'uid' or len(operation) > 1: raise ValueError("Operation must be 'u', 'i' or 'd'!")
	
		# for union and intersection, we want the same orientation on both polygons. for difference, we want different orientation.
		matching_orientation = polygon_a.is_clockwise() == polygon_b.is_clockwise()
		if matching_orientation != (operation != 'd'): 
			
			polygon_b = polygon_b.clone()
			polygon_b.flip()

		# initialize vector rings
		v_a = [(p, polygon_b.contains_point(p)) for p in polygon_a.points]
		v_b = [(p, polygon_a.contains_point(p)) for p in polygon_b.points]


		# find all intersections 
		intersections_a = defaultdict(list)
		intersections_b = defaultdict(list)
		for a1, a2 in zip(v_a, v_a[1:]) + [(v_a[-1], v_a[0])]:
			for b1, b2 in zip(v_b, v_b[1:]) + [(v_b[-1], v_b[0])]:
				i = intersect_lineseg_lineseg(a1[0],a2[0],b1[0],b2[0])
				if i:
					intersections_a[(a1[0],a2[0])].append(i)
					intersections_b[(b1[0],b2[0])].append(i)

			
		# extend vector rings by intersections 
		for k, v in intersections_a.iteritems():
			inorder_extend(v_a, k[0], k[1], v)

		for k, v in intersections_b.iteritems():
			inorder_extend(v_b, k[0], k[1], v)
		

		edge_fragments = defaultdict(list)
		
		def extend_fragments(v, poly, fragment_type):
			for v1, v2 in zip(v, v[1:]) + [(v[-1], v[0])]:
				if v1[1] == fragment_type or v2[1] == fragment_type:
					# one of the vertices is of the required type
					edge_fragments[v1[0]].append( v2[0] )		

				elif v1[1] == 2 and v2[1] == 2:
					# we have two boundary vertices
					m = (v1[0] + v2[0]) / 2.0
					t = poly.contains_point(m)
					if t == fragment_type or t == 2:
						edge_fragments[v1[0]].append( v2[0] )

		fragment_type_a = 1 if operation == 'i' else 0
		fragment_type_b = 1 if operation != 'u' else 0
	
		extend_fragments(v_a, polygon_b, fragment_type_a)
		extend_fragments(v_b, polygon_a, fragment_type_b)

		def print_edge():
			for k in edge_fragments.keys():
				for v in edge_fragments[k]:
					print "%s -> %s" % (k, v)




		output = []
		while edge_fragments:
			start = edge_fragments.keys()[0]
			current = edge_fragments[start][0]
			sequence = [start]
	
			# follow along the edge fragments sequence
			while not current in sequence:
				sequence.append(current)
				current = edge_fragments[current][0]


			# get only the cyclic part of the sequence
			sequence = sequence[sequence.index(current):]

			for c,n in zip(sequence, sequence[1:]) + [(sequence[-1], sequence[0])]:
				edge_fragments[c].remove(n)

				if not edge_fragments[c]: 
					del edge_fragments[c]



			output.append(Polygon.from_pointlist(Polygon.simplify_sequence(sequence)))

		return output

	@staticmethod
	def simplify_sequence(seq):
		"""Simplify a point sequence so that no subsequent points are on the same line"""

		i = 0
		while i < len(seq):
			p, c, n = seq[i-1], seq[i], seq[(i + 1) % len(seq)]

			if p == c or c == n or p == n or distance_point_lineseg_squared(c, p, n) < EPSILON:
				del seq[i]
			else:
				i+=1
		return seq


	@staticmethod
	def union(polygon_a, polygon_b):
		"""Get the union of polygon_a and polygon_b

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon
		
		@return: A list of fragment polygons
		"""
		return Polygon.boolean_operation(polygon_a, polygon_b, 'u')

	@staticmethod
	def intersect(polygon_a, polygon_b):
		"""Intersect the area of polygon_a and polygon_b

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon
		
		@return: A list of fragment polygons
		"""
		return Polygon.boolean_operation(polygon_a, polygon_b, 'i')

	@staticmethod
	def subtract(polygon_a, polygon_b):
		"""Subtract the area of polygon_b from polygon_a

		@type polygon_a: Polygon
		@param polygon_a: The first polygon

		@type polygon_b: Polygon
		@param polygon_b: The second polygon
		
		@return: A list of fragment polygons
		"""
		return Polygon.boolean_operation(polygon_a, polygon_b, 'd')
	
	
	@staticmethod
	def offset(polys, amount, tip_decorator=tip_decorator_pointy, debug_callback=None):
		"""Shrink or grow a polygon by a given amount.

		@type polys: List
		@param polys: The list of polygons to offset. Counter-clockwise polygons will be treated as islands, clockwise polygons as holes.

		@type amount: float
		@param amount: The amount to offset. Positive values will grow the polygon, negative values will shrink.

		@type tip_decorator: function
		@param tip_decorator: A function used for decorating tips generated in the offset polygon
		"""

		# fix passing a single polygon instead of a poly list
		if isinstance(polys, Polygon): polys = [polys]

		if amount == 0: return polys

		def offset_poly(poly):
			r = []
			for i in range(len(poly.points)): 
				c, n, n2 = poly.points[i], poly.points[ (i+1) % len(poly) ], poly.points[ (i+2) % len(poly) ]
				is_convex = point_orientation(c,n,n2) 

				unit_normal = (n - c).normal().normalize()
				unit_normal2 = (n2 - n).normal().normalize()
				
				c_prime = c + unit_normal * amount
				n_prime = n + unit_normal * amount
				n2_prime = n2 + unit_normal2 * amount
				n_prime2 = n + unit_normal2 * amount

				r.append(c_prime)
				r.append(n_prime)

				if is_convex == (amount > 0): 
					r.append(n)
				else: 
					r.extend(tip_decorator(c_prime, n_prime, n_prime2, n2_prime, True))

	
			return r


		def decompose(poly_points):
			"""Decompose a possibly self-intersecting polygon into multiple simple polygons."""

			def inorder_extend(v, v1, v2, ints):
				"""Extend a sequence v by points ints that are on the segment v1, v2"""

				k, r = None, False
				if v1.x < v2.x:
					k = lambda i: i.x
					r = True
				elif v1.x > v2.x:
					k = lambda i: i.x
					r = False
				elif v1.y < v2.y:
					k = lambda i: i.y
					r = True
				else:
					k = lambda i: i.y
					r = False

				l = sorted(ints, key=k, reverse=r)
				i = next((i for i, p in enumerate(v) if p == v2), -1)
				assert(i>=0)

				for e in l:
					v.insert(i, e)

			pts = [p for p in poly_points]

			# find self-intersections
			ints = defaultdict(list)
			for i in range(len(pts)):
				for j in range(i+1, len(pts)):
					a = pts[i]
					b = pts[(i+1)%len(pts)]
					c = pts[j]
					d = pts[(j+1)%len(pts)]

					x = intersect_lineseg_lineseg(a, b, c, d)
					if x and x not in (a,b,c,d):
						ints[(a,b)].append( x )
						ints[(c,d)].append( x )


			# add self-intersection points to poly
			for k, v in ints.iteritems():
				inorder_extend(pts, k[0], k[1], v)

			# build a list of loops
			out = []
			while pts:
				
				# build up a list of seen points until we re-visit one - a loop!
				seen = []
				for p in pts + [pts[0]]:
					if p not in seen:
						seen.append(p)
					else:
						break

				loop = seen[seen.index(p):]

				# remove the loop from pts
				for p in loop:
					pts.remove(p)

				out.append(loop)

			return out


		def winding_number(p, raw):

			# compute winding number of point
			#http://softsurfer.com/Archive/algorithm_0103/algorithm_0103.htm

			wn = 0
			for pp in raw:
				for a,b in zip(pp, pp[1:]) + [(pp[-1], pp[0])]:
					if a.y < p.y and b.y > p.y:
						i = intersect_lineseg_ray(a,b,p,p+VECTOR_X)
						if i and i.x > p.x:
							wn -= 1

					if a.y > p.y and b.y < p.y:
						i = intersect_lineseg_ray(a,b,p,p+VECTOR_X)
						if i and i.x > p.x:
							wn += 1
			return wn	


		def find_point_in_poly(pts):
			# find point inside of pts according to http://www.exaflop.org/docs/cgafaq/cga2.html#Subject%202.06:%20How%20do%20I%20find%20a%20single%20point%20inside%20a%20simple%20polygonu

			if len(pts) == 3: return (pts[0] + pts[1] + pts[2]) / 3

			
			# find convex point v
			v = None
			for i in range(len(pts)):
				a, v, b = pts[i-1], pts[i], pts[(i+1) % len(pts)]
				if not point_orientation(a,v,b): break


			q_s = [ q for q in pts if q not in [a,v,b] and point_in_triangle(q, a,v,b) ]

			if len(pts) >= 5:
				dbg(v, 0x000000, "V")
				dbg(a, 0x000000, "A")
				dbg(b, 0x000000, "B")
					
				for q in q_s:
					dbg(q, 0x000000, "Q")

			if q_s:
				# return the midpoint of the shortest diagonal qv
				q = min(q_s, key=lambda q: (q-v).length_squared ) 


				return (q - v) / 2.0 + v
			else:
				# no diagonal from v, return midpoint of ab instead
				return (b - a) / 2.0 + a
	


		def dbg(p, color, text):
			if debug_callback:
				debug_callback(p,color,text)


		raw = []
		for poly in polys:

			offset = offset_poly(poly)
			decomp = decompose( offset )
			
			raw.extend( decomp )


		#print "\n-----------------\n"
		output = []
		for poly in raw:
		
			poly = Polygon.simplify_sequence(poly)
			p = find_point_in_poly( poly )
			wn = winding_number(p, raw) 

			
			dbg(p, 0xffff00, "%d %d" % (wn, len(poly)))
			#print "%d %d" % (wn, len(poly))

			# shrink: include poly in solution only if winding number of that region is greater than 1			
			# grow: include only if winding number is 1
			if False or (amount < 0 and wn > 0) or (amount > 0 and wn == 1):
				output.append(Polygon.from_pointlist(poly))



		return output

	

	def is_clockwise(self):
		"""Determines whether the polygon has a clock-wise orientation."""

		# get index of point with minimal x value
		i_min = min(xrange(len(self.points)), key=lambda i: self.points[i].x)
	
		# get previous, current and next points
		a = self.points[i_min-1]
		b = self.points[i_min]
		c = self.points[(i_min+1) % len(self.points)]

		return point_orientation(a,b,c)


	def flip(self):
		"""Reverses the orientation of the polygon"""
		self.points.reverse()

	def contains_point(self, p):
		"""Checks if p is contained in the polygon, or on the boundary.
		
		@return: 0 if outside, 1 if in the polygon, 2 if on the boundary.
		"""

		# see if we find a line segment that p is on
		for a,b in zip(self.points[0:], self.points[1:]) + [(self.points[-1], self.points[0])]:

			d = distance_point_lineseg_squared(p, a, b)
			if p == Vector(2,2): 
				print "%s vs. [%s - %s]: %f" % (p, a,b,d)
			if d < EPSILON * EPSILON: return 2

		# p is not on the boundary, cast ray and intersect to see if we are inside
		intersections = set(intersect_poly_ray(self.points, p, p + Vector(1,0)))

		# filter intersection points that are boundary points
		for int_point in filter(lambda x: x in self.points, intersections):

			i = self.points.index(int_point)
			prv = self.points[i-1]
			nxt = self.points[(i+1) % len(self.points)]

			if point_orientation(p, int_point, nxt) == point_orientation(p,int_point, prv):
				intersections.remove(int_point)

		# we are inside if we have an odd amount of polygon intersections
		return 1 if len(intersections) % 2 == 1 else 0


	def as_tuple_list(self):
		return [(p.x, p.y) for p in self.points]

	def get_width(self):
		return self.right - self.left

	def get_height(self):
		return self.bottom - self.top

	def get_left(self):
		return min(self.points, key=lambda p: p.x).x

	def get_right(self):
		return max(self.points, key=lambda p: p.x).x

	def get_top(self):
		return min(self.points, key=lambda p: p.y).y

	def get_bottom(self):
		return max(self.points, key=lambda p: p.y).y

	append = add_point
	extend = add_points

	center = property(get_centerpoint)

	left = property(get_left)
	right = property(get_right)

	top = property(get_top)
	bottom = property(get_bottom)

	width = property(get_width)
	height = property(get_height)

class Transform(object):
	"""Class for representing affine transformations"""

	def __init__(self, data):
		self.data = data
		
	@staticmethod
	def unit():
		"""Get a new unit tranformation"""
		return Transform([[1, 0, 0],
		                  [0, 1, 0],
			          [0, 0, 1]])

	@staticmethod
	def move(dx, dy):
		"""Get a transformation that moves by dx, dy"""
		return Transform([[1, 0, dx],
		                  [0, 1, dy],
			          [0, 0, 1]])

	@staticmethod
	def rotate(phi):
		"""Get a transformation that rotates by phi"""
		return Transform([[math.cos(phi), -math.sin(phi), 0],
		                  [math.sin(phi), math.cos(phi), 0],
			          [0, 0, 1]])


	@staticmethod
	def scale(sx, sy):
		"""Get a transformation that scales by sx, sy"""
		return Transform([[sx, 0, 0],
		                  [0, sy, 0],
			          [0, 0, 1]])

	def __add__(self, b):
		t = Transform()
		t.data = [[self.data[x][y] + b.data[x][y] for y in range(3)] for x in range(3)]
		return t
	
	def __sub__(self, b):
		t = Transform()
		t.data = [[self.data[x][y] - b.data[x][y] for y in range(3)] for x in range(3)]
		return t

	def __mul__(self, val):

		if isinstance(val, Vector):

			x = val.x * self.data[0][0] + val.y * self.data[0][1] + self.data[0][2]
			y = val.x * self.data[1][0] + val.y * self.data[1][1] + self.data[1][2]
			
			return Vector(x,y)

		else:
			data = [[0 for y in range(3)] for x in range(3)]
			for i in range(3):
				for j in range(3):
					for k in range(3):
						data[i][j] += self.data[i][k] * val.data[k][j]

			return Transform(data)


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
	@param p2: The ending point of the line segment

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
	@param p2: The second point of the first line
	
	@type q1: Vector
	@param q1: The first point of the second line

	@type q2: Vector
	@param q2: The second point of the second line

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
	@param p2: The ending point of the line segment

	@type q1: Vector
	@param q1: The first point on the line 

	@type q2: Vector
	@param q2: The second point on the line
	
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
	@param p2: The ending point of the line segment

	@type q1: Vector
	@param q1: The first point on the ray

	@type q2: Vector
	@param q2: The second point on the ray
	
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
	@param p2: The second point on the ray
	
	@return: The list of intersections or an empty list 
	"""
	intersect_points = []

	for line_segment in segs:
		intersect = intersect_lineseg_ray(line_segment[0], line_segment[1], p1, p2)
		if intersect:
			#if line_segment[0] != p2 and line_segment[1] != p2:
			intersect_points += [intersect]

	return intersect_points

def intersect_linesegs_lineseg(segs, p1, p2):
	"""Intersect a list of line segments and a line segment
	
	@type segs: List
	@param segs: The list of line segments, i.e. a list of 2-tuples of vectors

	@type p1: Vector
	@param p1: The first point on the line segment

	@type p2: Vector
	@param p2: The second point on the line segment
	
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
	@param p2: The second point on the first line segment

	@type q1: Vector
	@param q1: The first point on the secondline segment

	@type q2: Vector
	@param q2: The second point on the second line segment
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
	@param p2: The second point on the first line segment


	@type q1: Vector
	@param q1: The first point on the secondline segment

	@type q2: Vector
	@param q2: The second point on the second line segment

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
	@param b: The second point on the first line segment
	"""


	ap = p - a
	ab = b - a
	bp = p - b

	r = float(ap * ab) / ab.length_squared

	if r <= 0: return ap.length_squared
	if r >= 1: return bp.length_squared
	
	s = ((a.y - p.y) * (b.x - a.x) - (a.x - p.x) * (b.y - a.y))

	return float(s * s) / ab.length_squared
	
	# ap_squared = (p - a).get_length_squared()
	# bp_squared = (p - b).get_length_squared()
	# ap_prime = a * b
	
	# perpendicular_squared = abs( ap_squared - ap_prime * ap_prime )

	# return min(ap_squared, bp_squared, perpendicular_squared)


def point_in_triangle(p, a,b,c):
	to = point_orientation(a,b,c)
	return point_orientation(a,b,p) == to and point_orientation(b,c,p) == to and point_orientation(a,p,c) == to

def point_orientation(a,b,c):
	"""Returns the orientation of the triangle a, b, c.
	
	Return True if a,b,c are oriented clock-wise.
	"""
	return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0

VECTOR_NULL = Vector(0,0)
VECTOR_X = Vector(1,0)
VECTOR_Y = Vector(0,1)
EPSILON = 0.0001
