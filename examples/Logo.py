import pygame

from examples import Example, SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import *

from py2d.Math import *

class Logo(Example):
	"""Logo Sample

	You should see a bouncing, rotating Py2D logo that is made up of polygons. Spiffy!

	This demo also shows you how to use Transform objects to modify your poly points.
	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Welcome"

		# get dimensions of multi-polygon list by strategically selected letters :)
		p = PY2D_LOGO[0][0]
		y = PY2D_LOGO[1][0]
		d = PY2D_LOGO[-1][0]

		self.w = d.right - p.left
		self.h = y.bottom - p.top
		self.time = 0

		self.colors = [0xFF0000, 0xFFCC00, 0x00FF00, 0xFFFF00, 0xFF00FF, 0x00FFFF]

	def update(self, time_elapsed):

		self.time = (self.time + time_elapsed)
		scale = abs( math.sin(self.time * 0.001 ) * 8 ) + 1
		rot = math.sin(self.time * 0.0003) * (math.pi / 6)

		# first transform logo to be centered at 0,0. then rotate, scale, finally position at center of screen
		self.transform = Transform.move(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) * Transform.scale(scale,scale) * Transform.rotate(rot) * Transform.move(-self.w/2, -self.h/2)

	def render(self):
		for polys, color in zip(PY2D_LOGO, self.colors):
			for poly in polys:
				points = [(p.x, p.y) for p in [ self.transform * v for v in poly.points ]]
				pygame.draw.lines(self.runner.screen, color, True, points)

class Opaque(Example):
	"""Logo (Convex decomposition) sample

	You should see a bouncing, rotating Py2D logo that is made up of polygons. Spiffy!

	This demo also shows you how to use Transform objects to modify your poly points plus how to decompose concave polygons with holes into convex parts.

	Key mappings:

	  F: Toggle polygon fill

	"""

	def __init__(self, runner):
		self.runner = runner
		self.title = "Welcome"

		# get dimensions of multi-polygon list by strategically selected letters :)
		p = PY2D_LOGO[0][0]
		y = PY2D_LOGO[1][0]
		d = PY2D_LOGO[-1][0]

		self.w = d.right - p.left
		self.h = y.bottom - p.top
		self.time = 0

		self.colors = [0xFF0000, 0xFFCC00, 0x00FF00, 0xFFFF00, 0xFF00FF, 0x00FFFF]

		self.logo = [ Polygon.convex_decompose(letter[0], letter[1:]) for letter in PY2D_LOGO ]

		self.fill = False

	def update(self, time_elapsed):

		self.time = (self.time + time_elapsed)
		scale = abs( math.sin(self.time * 0.001 ) * 8 ) + 1
		rot = math.sin(self.time * 0.0003) * (math.pi / 6)

		# first transform logo to be centered at 0,0. then rotate, scale, finally position at center of screen
		self.transform = Transform.move(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) * Transform.scale(scale,scale) * Transform.rotate(rot) * Transform.move(-self.w/2, -self.h/2)

		if self.runner.keys[K_f]:
			self.runner.keys[K_f] = False
			self.fill = not self.fill

	def render(self):
		for polys, color in zip(self.logo, self.colors):
			for poly in polys:
				points = [(p.x, p.y) for p in [ self.transform * v for v in poly.points ]]
				pygame.draw.polygon(self.runner.screen, color, points, 0 if self.fill else 1)

PY2D_LOGO = [

	[ # P
		Polygon.from_pointlist([Vector(0.002860, 27.997820),Vector(0.002860, -0.002180),Vector(10.842860, -0.002180),Vector(13.272860, 1.517820),Vector(15.122860, 3.677820),Vector(16.322860, 6.367820),Vector(16.722870, 9.477820),Vector(16.312850, 12.637820),Vector(15.082850, 15.557820),Vector(13.052850, 17.947820),Vector(10.242850, 19.517820),Vector(5.402850, 19.517820),Vector(5.402850, 27.997820)]),
		Polygon.from_pointlist([Vector(5.402850, 4.797820),Vector(5.402850, 14.797820),Vector(8.962850, 14.797820),Vector(10.612850, 12.577820),Vector(11.162860, 9.517820),Vector(10.562860, 6.717820),Vector(9.202860, 4.797820),Vector(5.402860, 4.797820)])
	],
	[ # y
		Polygon.from_pointlist([Vector(18.972850, 16.757820),Vector(18.972850, 7.557820),Vector(24.292850, 7.557820),Vector(24.292850, 16.797820),Vector(24.642850, 19.987820),Vector(25.692850, 22.597820),Vector(26.872850, 22.597820),Vector(28.052850, 22.597820),Vector(29.042840, 20.007820),Vector(29.372850, 16.797820),Vector(29.372850, 7.557820),Vector(34.692850, 7.557820),Vector(34.692850, 16.477820),Vector(33.892850, 21.757820),Vector(31.372850, 26.917820),Vector(28.692850, 31.277820),Vector(27.172850, 33.117820),Vector(25.092850, 33.997820),Vector(18.772850, 33.997820),Vector(18.772850, 29.797820),Vector(23.092850, 29.797820),Vector(24.492850, 28.957820),Vector(25.652850, 27.237820),Vector(25.892850, 26.797820),Vector(23.132850, 26.797820),Vector(20.092850, 22.597820),Vector(18.972850, 16.757820)])
	],
	[ # 2
		Polygon.from_pointlist([Vector(37.002850, 23.997820),Vector(44.962850, 5.077820),Vector(43.978940, 4.797820),Vector(37.842840, 4.797820),Vector(37.842840, -0.002180),Vector(46.482840, -0.002180),Vector(48.871540, 1.657820),Vector(49.949240, 4.319720),Vector(48.162840, 11.117820),Vector(42.762840, 23.357820),Vector(49.762840, 23.357820),Vector(49.762840, 27.997820),Vector(37.002840, 27.997820)])
	] ,
	[ # D
		Polygon.from_pointlist([Vector(52.812840, 27.997820),Vector(52.812840, -0.002180),Vector(64.412840, -0.002180),Vector(68.672840, 5.937820),Vector(70.092840, 13.677820),Vector(68.762840, 21.557820),Vector(64.772840, 27.997820)]),
		Polygon.from_pointlist([Vector(58.252850, 23.357820),Vector(61.852850, 23.357820),Vector(63.612850, 19.277820),Vector(64.292850, 13.957820),Vector(63.702840, 8.527820),Vector(61.932840, 4.797820),Vector(58.252840, 4.797820),Vector(58.252840, 23.357820)])
	]
]
