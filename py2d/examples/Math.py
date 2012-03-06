import pygame
from pygame.locals import *

from py2d.Math import *
import py2d.examples.Main

class Boolean(py2d.examples.Main.Example):

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

