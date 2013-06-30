import pygame
from pygame.locals import *

from py2d.Math import *
from py2d.SVG import convert_svg

from examples import Example

class SVGConverter(Example):
	"""SVG Converter Sample

	Polygons are imported from an SVG file created in Inkscape.

	Have fun!
	"""
	def __init__(self, runner):
		self.runner = runner
		self.title = "Polygon Decomposition"

		self.polys = []

		for id, polys in convert_svg("examples/shapes.svg", bezier_max_divisions = None).iteritems():
			self.polys.append(polys)

		self.decomp = []

		self.poly_colors = [ 0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff ]

	def render(self):

		t = Transform.unit() #Transform.move(-22,-700)

		for j, p in enumerate(self.polys):
			for i,h in enumerate(p):
				self.draw_poly(t * h, self.poly_colors[j % len(self.poly_colors)], False)


	def draw_poly(self, poly, color, fill):
		if len(poly) > 1:
			if fill and len(poly) > 2:
				pygame.draw.polygon(self.runner.screen, color, poly.as_tuple_list())

			pygame.draw.lines(self.runner.screen, color, True, poly.as_tuple_list())
		elif poly.points:
			pygame.draw.circle(self.runner.screen, color, poly.points[0].as_tuple(), 2)


