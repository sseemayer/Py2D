import pygame
from pygame.locals import *

from py2d.Bezier import *
from py2d.Math import *

SELECTION_DISTANCE = 20

from examples import Example

class Cubic(Example):
	"""Cubic Bezier curve sample

	Draw around end and control points of the bezier curve.

	Key mappings:
	  MOUSE1: Drag points

	Have fun!
	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Cubic Beziers"

		self.p1 = Vector(200,400)
		self.p2 = Vector(400,400)
		self.c1 = Vector(500,50)
		self.c2 = Vector(100,50)


		self.points = ( ('P1', (255,0,0), self.p1),
				('P2', (255,0,0), self.p2),
				('C1', (0,255,0), self.c1),
				('C2', (0,255,0), self.c2) )

		self.sel_point = None

	def update(self, time_elapsed):
		pass

	def render(self):

		pygame.draw.line(self.runner.screen, 0x006600, self.p1.as_tuple(), self.c1.as_tuple())
		pygame.draw.line(self.runner.screen, 0x006600, self.p2.as_tuple(), self.c2.as_tuple())

		for label, color, pos in self.points:
			self.draw_point(pos, color, label)

		bezier = [self.p1] + flatten_cubic_bezier(self.p1, self.p2, self.c1, self.c2) + [self.p2]

		pygame.draw.lines(self.runner.screen, 0xffffff, False, [p.as_tuple() for p in bezier], 2)

		if self.sel_point:
			pygame.draw.ellipse(self.runner.screen, 0xfff00, pygame.Rect( (self.sel_point.x - 4, self.sel_point.y - 4), (8,8)) , 1)

	def draw_point(self, p, color, label=None):
		pygame.draw.ellipse(self.runner.screen, color, pygame.Rect(p.as_tuple(), (2,2)))
		if label:
			self.runner.screen.blit(self.runner.font.render(label, False, color), p.as_tuple())

	def mouse_down(self, pos, button):
		if button == 1:
			mouse = Vector(*pos)

			nearest = min(self.points, key=lambda p: (p[2]-mouse).length)

			if (nearest[2] - mouse).length_squared <= SELECTION_DISTANCE:
				self.sel_point = nearest[2]
			else:
				self.sel_point = None

	def mouse_move(self, pos, rel, buttons):
		if buttons[0] and self.sel_point:
			self.sel_point.x, self.sel_point.y = pos


class Quadratic(Example):
	"""Quadratic Bezier curve sample

	Draw around end and control points of the bezier curve.

	Key mappings:
	  MOUSE1: Drag points

	Have fun!
	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Quadratic Beziers"

		self.p1 = Vector(200,400)
		self.p2 = Vector(400,400)
		self.c = Vector(300,50)


		self.points = ( ('P1', (255,0,0), self.p1),
				('P2', (255,0,0), self.p2),
				('C', (0,255,0), self.c) )

		self.sel_point = None

	def update(self, time_elapsed):
		pass

	def render(self):

		pygame.draw.line(self.runner.screen, 0x006600, self.p1.as_tuple(), self.c.as_tuple())
		pygame.draw.line(self.runner.screen, 0x006600, self.p2.as_tuple(), self.c.as_tuple())

		for label, color, pos in self.points:
			self.draw_point(pos, color, label)

		bezier = [self.p1] + flatten_quadratic_bezier(self.p1, self.p2, self.c) + [self.p2]

		pygame.draw.lines(self.runner.screen, 0xffffff, False, [p.as_tuple() for p in bezier], 2)

		if self.sel_point:
			pygame.draw.ellipse(self.runner.screen, 0xfff00, pygame.Rect( (self.sel_point.x - 4, self.sel_point.y - 4), (8,8)) , 1)

	def draw_point(self, p, color, label=None):
		pygame.draw.ellipse(self.runner.screen, color, pygame.Rect(p.as_tuple(), (2,2)))
		if label:
			self.runner.screen.blit(self.runner.font.render(label, False, color), p.as_tuple())

	def mouse_down(self, pos, button):
		if button == 1:
			mouse = Vector(*pos)

			nearest = min(self.points, key=lambda p: (p[2]-mouse).length)

			if (nearest[2] - mouse).length_squared <= SELECTION_DISTANCE:
				self.sel_point = nearest[2]
			else:
				self.sel_point = None

	def mouse_move(self, pos, rel, buttons):
		if buttons[0] and self.sel_point:
			self.sel_point.x, self.sel_point.y = pos

