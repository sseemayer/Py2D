import pygame
from pygame.locals import *

from py2d.FOV import *
from py2d.Math import *
from examples import Example, SCREEN_WIDTH, SCREEN_HEIGHT

class FOV(Example):
	"""Field of View Example

	Move your mouse and watch how the obstacles affect the field of view

	Have fun!
	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Field of View"

		center = Vector( SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

		## create circle of boxes around center
		box = [Vector(-15, -2), Vector(15,-2), Vector(15,2), Vector(-15,2), Vector(-15,-2)]
		self.obstructors = [ [ Transform.move( center.x, center.y ) * Transform.rotate(phi) * Transform.move(100,0) * p for p in box ] for phi in [i * 2.0 * math.pi / 16 for i in range(16)]]

		#self.obstructors = [ [ Vector(100,100), Vector(220, 100), Vector(220,120), Vector(100,120), Vector(100,100) ] ]

		self.eye = center
		self.debug = False


		self.vision = Vision(self.obstructors, self.debug)


	def update(self, time_elapsed):
		self.fov = self.vision.get_vision(self.eye, VISION_RADIUS, Polygon.regular(self.eye, VISION_RADIUS, VISION_POINTS))

	def render(self):
		if len(self.fov) > 3:
			pygame.draw.polygon(self.runner.screen, 0xFFFF66, self.fov.as_tuple_list())
			pygame.draw.polygon(self.runner.screen, 0xFFFFFF, self.fov.as_tuple_list(), 1)

		for obs in self.obstructors:
			pygame.draw.lines(self.runner.screen, 0xFF0000, True, [ p.as_tuple() for p in obs ])

		if self.debug:
			for p, c in self.vision.debug_points:
				pygame.draw.ellipse(self.runner.screen, c, pygame.Rect(p.x - 2, p.y - 2, 4, 4))

			for c, ls in self.vision.debug_linesegs:
				pygame.draw.lines(self.runner.screen, c, False, [ p.as_tuple() for p in ls])

		pygame.draw.ellipse(self.runner.screen, 0x000000, pygame.Rect(self.eye.x - 2, self.eye.y - 2, 4,4))

	def mouse_move(self, pos, rel, buttons):
		# add 0.01 to avoid colinearity
		self.eye = Vector(pos[0]+0.01, pos[1]+0.01)


VISION_RADIUS = 300
VISION_POINTS = 16
