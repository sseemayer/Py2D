"""Py2D example runner. Requires pygame"""


import pygame
from pygame.locals import *

from collections import defaultdict

class ExampleRunner(object):

	def __init__(self):
		pygame.init()

		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption

		self.example = None

		self.running = True

		self.keys = defaultdict(lambda: False)

		self.font = pygame.font.Font(pygame.font.get_default_font(), 12)

		self.show_help = False

	def get_example(self):
		return self._example

	def set_example(self, example):
		self._example = example

		if example == None:
			pygame.display.set_caption("Py2D Examples")
		else:
			pygame.display.set_caption("Py2D Examples - %s (Press F1 for help)" % example.title)

	def del_example(self):
		self.set_example(None)

	example = property(get_example, set_example, del_example)

	def main_loop(self):
		last_time = pygame.time.get_ticks()
		while self.running:

			time = pygame.time.get_ticks()
			time_elapsed = time - last_time
			last_time = time

			self.update(time_elapsed)
			self.render()

			pygame.display.update()

	def update(self, time_elapsed):

		for event in pygame.event.get():
			if event.type in (KEYDOWN, KEYUP):

				if event.key == K_ESCAPE:
					self.running = False
					return

				if event.key == K_F1 and event.type == KEYDOWN:
					self.show_help = not self.show_help

				if not self.show_help:
					self.keys[event.key] = (event.type == KEYDOWN)

			elif event.type == QUIT:
				self.running = False

			elif event.type == MOUSEBUTTONUP and not self.show_help:
				if self._example: self._example.mouse_up(event.pos, event.button)

			elif event.type == MOUSEBUTTONDOWN and not self.show_help:
				if self._example: self._example.mouse_down(event.pos, event.button)

			elif event.type == MOUSEMOTION and not self.show_help:
				if self._example: self._example.mouse_move(event.pos, event.rel, event.buttons)


		if self._example:
			self._example.update(time_elapsed)

	def render(self):

		if self.show_help:
			self.screen.fill(TEXT_BACKGROUND)
			if self._example:
				for l, line in enumerate([s.replace("\t","") for s in self._example.__doc__.split("\n")]):
					surf = self.font.render(line, True, TEXT_COLOR, TEXT_BACKGROUND)
					self.screen.blit(surf, (10, 15 * l + 10) )

		else:

			self.screen.fill(BACKGROUND_COLOR)

			if self._example:
				self._example.render()


	def example_from_string(self, example_name):
		import inspect


		package_name, class_name = example_name.rsplit('.', 1)
		package = __import__(package_name, globals(), locals(), [class_name], 1)

		cls = next((c[1] for c in inspect.getmembers(package, inspect.isclass) if c[0] == class_name))

		return cls(self)

class Example(object):

	def update(self, time_elapsed): pass

	def render(self): pass

	def mouse_move(self, pos, rel, buttons): pass

	def mouse_down(self, pos, button): pass

	def mouse_up(self, pos, button): pass

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BACKGROUND_COLOR = 0x000033

TEXT_BACKGROUND = (16, 16, 16)
TEXT_COLOR = (255,255,255)

import examples.Bezier
import examples.Draw
import examples.FOV
import examples.Logo
import examples.Math
import examples.Navigation
import examples.Pymunk
import examples.SVG

