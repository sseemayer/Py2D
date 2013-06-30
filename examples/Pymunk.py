"""Py2D + pymunk examples

Please ensure that you have pymunk version 2.1.0 or greater installed to run these demos!
"""

import pygame
from pygame.locals import *

from py2d.Math import *
from examples.Logo import PY2D_LOGO
from examples import Example, SCREEN_WIDTH, SCREEN_HEIGHT

try:
	import pymunk as pm
	import pymunk.constraint as pmc




	class LogoPhysics(Example):
		"""Logo (physics) sample

		Create Py2D logos and watch them move.

		Key mappings:

		L: Create a new Py2D logo
		F: Toggle polygon fill

		"""

		def __init__(self, runner):
			self.runner = runner
			self.title = "Py2D with Pymunk physics"

			# get dimensions of multi-polygon list by strategically selected letters :)
			p = PY2D_LOGO[0][0]
			y = PY2D_LOGO[1][0]
			d = PY2D_LOGO[-1][0]

			self.w = d.right - p.left
			self.h = y.bottom - p.top

			self.colors = [0xFF0000, 0xFFCC00, 0x00FF00, 0xFF00FF, 0x00FFFF]

			transform = Transform.move(SCREEN_WIDTH / 2, 10) * Transform.scale(5,5) * Transform.move(-self.w / 2 - p.left, -self.h / 2 - p.top)
			logo_scaled = [ [ Polygon.from_pointlist([ transform * p for p in poly]) for poly in letter ] for letter in PY2D_LOGO]

			self.logo_polys = [ Polygon.convex_decompose(letter[0], letter[1:]) for letter in logo_scaled]

			self.fill = False

			self.space = pm.Space()
			self.space.gravity = (0,9.81)
			self.space.damping = 0.9

			tray = pm.Body()
			tray_left = pm.Segment(pm.Body(), (0,0), (0,SCREEN_HEIGHT), 5)
			tray_right = pm.Segment(pm.Body(), (SCREEN_WIDTH,0), (SCREEN_WIDTH,SCREEN_HEIGHT), 5)
			tray_bottom = pm.Poly(pm.Body(), [(0,SCREEN_HEIGHT/2), (SCREEN_WIDTH,SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])

			tray_bottom.elasticity = 0
			tray_bottom.friction = 1

			self.space.add_static(tray_left, tray_right, tray_bottom)


			self.letters = []

		def make_logo(self):

			#"""
			for letter in range(len(self.logo_polys)):
				self.letters.append([])

				mass = 100
				body = pm.Body(mass, 30000)

				cps = [p.get_centerpoint() for p in self.logo_polys[letter]]
				cp_x = sum((p.x for p in cps)) / len(self.logo_polys[letter])
				cp_y = sum((p.y for p in cps)) / len(self.logo_polys[letter])

				body.position = cp_x, cp_y

				self.space.add(body)

				for poly in self.logo_polys[letter]:

					pt = Polygon.from_tuples([(v.x - cp_x, v.y - cp_y) for v in poly])
					verts = [(v.x, v.y) for v in pt]

					shape = pm.Poly(body, verts)
					shape.elasticity = 0.1

					self.letters[letter].append( (pt, body) )
					self.space.add(shape)

			"""
			self.letters = []
			for i in range(6):
				verts = [(-10,-10), (10,-10), (10,10), (-10,10)]
				b = pm.Body(100, pm.moment_for_box(100,20,20))
				b.position = (30 + 50 * i, 100)
				s = pm.Poly(b, verts)
				s.elasticity = 0
				self.space.add(b,s)
				self.letters.append([ ( Polygon.from_tuples(verts), b ) ])
			""" # """


		def update(self, time_elapsed):

			self.space.step(time_elapsed / 1000.0)

			if self.runner.keys[K_f]:
				self.runner.keys[K_f] = False
				self.fill = not self.fill

			if self.runner.keys[K_l]:
				self.runner.keys[K_l] = False
				self.make_logo()

		def render(self):
			pygame.draw.polygon(self.runner.screen, 0x000000, [(0,SCREEN_HEIGHT/2), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])

			for polys, color in zip(range(len(self.letters)), self.colors):
				for poly, body in self.letters[polys]:
					t = Transform.move(body.position.x, body.position.y) * Transform.rotate(body.angle)


					points = [(t * p).as_tuple() for p in poly.points ]
					pygame.draw.polygon(self.runner.screen, color, points, 0 if self.fill else 1)
					#pygame.draw.ellipse(self.runner.screen, 0xffffff, (body.position.x, body.position.y, 2,2))

except ImportError:
	pass
