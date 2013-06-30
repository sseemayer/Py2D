import pygame
from pygame.locals import *

from py2d.Math import *
from examples import Example

class Decompose(Example):
	"""Convex Decomposition Sample

	Draw a polygon and holes and observe its convex decomposition.

	The currently active polygon is colored white. You can switch active polygons with the number keys 0-9.

	The polygons are numbered as follows:
	  0    The Main Polygon (color: green)
	  1-9  Holes in the Main polygon (color: red)

	The result of the decomposition will be shown in yellow.

	Key mappings:

	  0-9: Switch active polygon
	  F: Toggle polygon fill

	  MOUSE1: Add new point to the end of the active polygon
	  BACKSPACE: Delete the last point of the active polygon

	Have fun!
	"""
	def __init__(self, runner):
		self.runner = runner
		self.title = "Polygon Decomposition"

		self.polys = [Polygon() for i in range(10)]
		self.active_poly = 0

		self.decomp = []

		self.debug = False
		self.fill = False

		self.update_decomp()


	def update(self, time_elapsed):
		if self.runner.keys[K_BACKSPACE]:

			self.runner.keys[K_BACKSPACE] = False

			if self.polys[self.active_poly].points: del(self.polys[self.active_poly].points[-1])


			self.update_decomp()

		for i in range(10):
			key = ord(str(i))
			if self.runner.keys[key]:
				self.runner.keys[key] = False
				self.active_poly = i

		if self.runner.keys[K_d]:
			self.runner.keys[K_d] = False
			self.debug = not self.debug

		if self.runner.keys[K_f]:
			self.runner.keys[K_f] = False
			self.fill = not self.fill

	def render(self):


		self.draw_poly(self.polys[0], 0x00ff00, False)

		for h in self.polys[1:]:
			self.draw_poly(h, 0xff0000, False)

		for p in self.decomp:
			self.draw_poly(p, 0xffff00, self.fill)

		if self.debug:
			for p,c,t in self.debug_points:
				self.runner.screen.blit(self.runner.font.render(t, True, c), p.as_tuple())

	def draw_poly(self, poly, color, fill):
		if len(poly) > 1:
			if fill and len(poly) > 2:
				pygame.draw.polygon(self.runner.screen, color, poly.as_tuple_list())


			pygame.draw.lines(self.runner.screen, color, True, poly.as_tuple_list())
		elif poly.points:
			pygame.draw.circle(self.runner.screen, color, poly.points[0].as_tuple(), 2)



	def mouse_down(self, pos, button):
		if button == 1:

			self.polys[self.active_poly].add_point(Vector(pos[0], pos[1]))

			self.update_decomp()

	def update_decomp(self):
		self.debug_points = []
		if len(self.polys[0]) > 2:

			holes = [h for h in self.polys[1:] if len(h) > 2]

			def debug_point(p,c,t):
				self.debug_points.append((p,c,t))

			self.decomp = Polygon.convex_decompose(self.polys[0], holes, debug_callback=debug_point)
		else:
			self.decomp = []


class Offset(Example):
	"""Polygon Offset Sample

	Draw a polygon outline with the mouse. Py2D will calculate offset polygons.

	Key mappings:

	  MOUSE1: Add new point to the end of the active polygon
	  BACKSPACE: Delete the last point of the active polygon

	  c: Increase offset amount
	  x: Decrease offset amount

	  F: Toggle polygon fill

	Have fun!
	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Polygon Offset"
		self.poly = Polygon()

		self.update_offset()

		self.amount = 10

		self.fill = False
		self.debug = False

		self.tip_decorator = tip_decorator_pointy

	def update(self, time_elapsed):
		if self.runner.keys[K_BACKSPACE] and self.poly.points:
			del(self.poly.points[len(self.poly.points)-1])
			self.runner.keys[K_BACKSPACE] = False
			self.update_offset()

		if self.runner.keys[K_c]:
			self.amount += time_elapsed * 0.01
			self.update_offset()

		if self.runner.keys[K_x]:
			self.amount -= time_elapsed * 0.01
			if self.amount < 1: self.amount = 1
			self.update_offset()

		if self.runner.keys[K_f]:
			self.runner.keys[K_f] = False
			self.fill = not self.fill

		if self.runner.keys[K_d]:
			self.runner.keys[K_d] = False
			self.debug = not self.debug


		if self.runner.keys[K_1]:
			self.runner.keys[K_1] = False
			self.tip_decorator = tip_decorator_pointy
			self.update_offset()

		if self.runner.keys[K_2]:
			self.runner.keys[K_2] = False
			self.tip_decorator = tip_decorator_flat
			self.update_offset()

		if self.runner.keys[K_3]:
			self.runner.keys[K_3] = False
			self.update_offset()

	def render(self):

		for p in self.grow:
			self.draw_poly(p, 0x00ff00)

		self.draw_poly(self.poly, 0xffffff)

		for p in self.shrink:
			self.draw_poly(p, 0xff0000)


	def draw_poly(self, poly, color):
		if len(poly) > 1:
			if self.fill and len(poly) > 2:
				pygame.draw.polygon(self.runner.screen, color, poly.as_tuple_list())
				pygame.draw.lines(self.runner.screen, 0x000000, True, poly.as_tuple_list())
			elif len(poly) > 1:
				pygame.draw.lines(self.runner.screen, color, True, poly.as_tuple_list())
		elif poly.points:
			pygame.draw.circle(self.runner.screen, color, poly.points[0].as_tuple(), 2)

		if self.debug:
			for p, c, t in self.debug_points:
				self.runner.screen.blit(self.runner.font.render(t, False, c), p.as_tuple())


	def mouse_down(self, pos, button):
		if button == 1:
			self.poly.add_point(Vector(pos[0], pos[1]))
			self.update_offset()

	def update_offset(self):
		self.debug_points = []


		def debug_point(color):
			return lambda p, c, t: self.debug_points.append((p,color,t))

		if len(self.poly) > 2:
			self.shrink = Polygon.offset([self.poly.clone_ccw()], -self.amount, self.tip_decorator, debug_callback=debug_point((255,0,0)))
			self.grow = Polygon.offset([self.poly.clone_ccw()], self.amount, self.tip_decorator, debug_callback=debug_point((0,255,0)))
		else:
			self.shrink = []
			self.grow = []


class Boolean(Example):
	"""Boolean Operations sample

	Draw polygons A and B and observe their intersections, unions and differences.

	The currently active polygon is colored white. You can switch active polygons with the SPACE BAR.
	If not active, the polygon A will be colored red. Polygon B will be colored green.

	The result of the boolean operation will be shown in yellow.

	Key mappings:

	  SPACE BAR: Toggle active polygon
	  F: Toggle polygon fill

	  U: Switch to Union mode, show the union of A and B
	  I: Switch to Intersection mode, show the intersection of A and B
	  D: Switch to Difference mode, show A - B

	  MOUSE1: Add new point to the end of the active polygon
	  BACKSPACE: Delete the last point of the active polygon

	Have fun!
	"""
	def __init__(self, runner):
		self.runner = runner
		self.title = "Boolean Operations"


		#self.poly_a = Polygon.from_tuples([(0,0), (4,0), (4,4), (0, 4)])
		#self.poly_b = Polygon.from_tuples([(2,2), (3,6), (1,6)])

		self.poly_a = Polygon()
		self.poly_b = Polygon()

		self.active_poly = True
		self.bool = []
		self.mode = 'i'

		self.fill = True

		self.update_bool()

	def update(self, time_elapsed):
		if self.runner.keys[K_BACKSPACE]:

			self.runner.keys[K_BACKSPACE] = False

			if self.active_poly:
				if self.poly_a.points: del(self.poly_a.points[-1])
			else:
				if self.poly_b.points: del(self.poly_b.points[-1])

			self.update_bool()

		if self.runner.keys[K_SPACE]:
			self.runner.keys[K_SPACE] = False
			self.active_poly = not self.active_poly

		if self.runner.keys[K_u]:
			self.runner.keys[K_u] = False
			self.mode = 'u'
			self.update_bool()

		if self.runner.keys[K_i]:
			self.runner.keys[K_i] = False
			self.mode = 'i'
			self.update_bool()

		if self.runner.keys[K_d]:
			self.runner.keys[K_d] = False
			self.mode = 'd'
			self.update_bool()

		if self.runner.keys[K_f]:
			self.runner.keys[K_f] = False
			self.fill = not self.fill

	def render(self):

		a_color = 0xffffff if self.active_poly else 0xff0000
		b_color = 0xffffff if not self.active_poly else 0x00ff00

		self.draw_poly(self.poly_a, a_color)
		self.draw_poly(self.poly_b, b_color)

		for p in self.bool:
			self.draw_poly(p, 0xffff00)


	def draw_poly(self, poly, color):
		if len(poly) > 1:
			if self.fill and len(poly) > 2:
				pygame.draw.polygon(self.runner.screen, color, poly.as_tuple_list())


			pygame.draw.lines(self.runner.screen, color, True, poly.as_tuple_list())
		elif poly.points:
			pygame.draw.circle(self.runner.screen, color, poly.points[0].as_tuple(), 2)



	def mouse_down(self, pos, button):
		if button == 1:
			if self.active_poly:
				self.poly_a.add_point(Vector(pos[0], pos[1]))
			else:
				self.poly_b.add_point(Vector(pos[0], pos[1]))

			self.update_bool()

	def update_bool(self):
		if len(self.poly_a) > 2 and len(self.poly_b) > 2:
			try:
				self.bool = Polygon.boolean_operation(self.poly_a, self.poly_b, self.mode)
			except IndexError:
				self.bool = []
		else:
			self.bool = []

