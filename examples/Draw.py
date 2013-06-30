import pygame
from pygame.locals import *

from py2d.Math import *
from examples import Example

class Draw(Example):
	"""Polygon Drawing Sample

	Draw a polygon outline with the mouse.

	Key mappings:

	  MOUSE1: Add new point to the end of the active polygon
	  BACKSPACE: Delete the last point of the active polygon

	Have fun!
	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Simple Drawing"

		self.poly = Polygon()

	def update(self, time_elapsed):
		if self.runner.keys[K_BACKSPACE] and self.poly.points:
			del(self.poly.points[len(self.poly.points)-1])
			self.runner.keys[K_BACKSPACE] = False

	def render(self):

		if len(self.poly) > 1:
			pygame.draw.lines(self.runner.screen, 0xff0000, True, self.poly.as_tuple_list())
		elif self.poly.points:
			pygame.draw.circle(self.runner.screen, 0xff0000, self.poly.points[0].as_tuple(), 2)

	def mouse_down(self, pos, button):
		if button == 1:
			self.poly.add_point(Vector(pos[0], pos[1]))

