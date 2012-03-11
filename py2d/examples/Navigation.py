import pygame
from pygame.locals import *

from py2d.Math import *
import py2d.examples.Main

from py2d.Navigation import *

class Mesh(py2d.examples.Main.Example):
	"""Navigation mesh generation sample

	Draw a polygon and holes and observe the generated navigation mesh. 
	The generated mesh will be colored light gray with the connectivity shown in cyan.

	You can switch active polygons with the number keys 0-9.
	
	The polygons are numbered as follows:
	  0    The Main Polygon (color: green)
	  1-9  Holes in the Main polygon (color: red)

	The result of the decomposition will be shown in yellow.
	
	Key mappings:

	  0-9: Switch active polygon

	  MOUSE1: Add new point to the end of the active polygon
	  BACKSPACE: Delete the last point of the active polygon

	Have fun!
	"""
	def __init__(self, runner):
		self.runner = runner
		self.title = "Navigation Mesh"

		self.polys = [Polygon() for i in range(10)]
		self.active_poly = 0
	
		self.beginning = None
		self.end = None

		self.debug = False
		self.fill = False

		self.update_mesh()
		self.update_nav()

		self.mouse_pos = None

	def update(self, time_elapsed):
		if self.runner.keys[K_BACKSPACE]:
			
			self.runner.keys[K_BACKSPACE] = False
			
			if self.polys[self.active_poly].points: del(self.polys[self.active_poly].points[-1])

			self.update_mesh()

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

		if self.runner.keys[K_b]:
			self.runner.keys[K_b] = False
			self.beginning = Vector(self.mouse_pos[0], self.mouse_pos[1])
			self.update_nav()

		if self.runner.keys[K_e]:
			self.runner.keys[K_e] = False
			self.end = Vector(self.mouse_pos[0], self.mouse_pos[1])
			self.update_nav()

	def render(self):
		
		self.draw_poly(self.polys[0], 0x00ff00, False)
	
		for h in self.polys[1:]:
			self.draw_poly(h, 0xff0000, False)

		if self.mesh:
			for i, p in enumerate(self.mesh.polygons):
				self.draw_poly(p, 0xcccccc, self.fill)
				if self.fill: self.draw_poly(p, 0x000000, False)

				center = p.get_centerpoint()
				if self.debug: self.runner.screen.blit(self.runner.font.render(str(i), True, (0,0,0)), center.as_tuple())

				for n,dist in p.neighbors.iteritems():
					pygame.draw.line(self.runner.screen, 0x00ff00, center.as_tuple(), n.get_centerpoint().as_tuple(), 3)

		if self.path:
			for a, b in zip(self.path, self.path[1:]):
				pygame.draw.line(self.runner.screen, 0xff0000, a.get_centerpoint().as_tuple(), b.get_centerpoint().as_tuple(), 5)

		if self.beginning:
			pygame.draw.circle(self.runner.screen, 0x00ff00, self.beginning.as_tuple(),2)

		if self.end:
			pygame.draw.circle(self.runner.screen, 0xff0000, self.end.as_tuple(),2)


	def draw_poly(self, poly, color, fill):
		if len(poly) > 1:
			if fill and len(poly) > 2:
				pygame.draw.polygon(self.runner.screen, color, poly.as_tuple_list())
			
			pygame.draw.lines(self.runner.screen, color, True, poly.as_tuple_list())
		elif poly.points:
			pygame.draw.circle(self.runner.screen, color, poly.points[0].as_tuple(),2)



	def mouse_down(self, pos, button):
		if button == 1:

			self.polys[self.active_poly].add_point(Vector(pos[0], pos[1]))

			self.update_mesh()

	def mouse_move(self, pos, rel, buttons):
		self.mouse_pos = pos

	def update_mesh(self):
		self.debug_points = []
		if len(self.polys[0]) > 2:
			
			holes = [h for h in self.polys[1:] if len(h) > 2]

			self.mesh = NavMesh.generate(self.polys[0], holes) 
		else:
			self.mesh = None

		self.update_nav()

	def update_nav(self):

		if self.mesh:
			self.path = self.mesh.get_path(self.beginning, self.end)
		else:
			self.path = None

