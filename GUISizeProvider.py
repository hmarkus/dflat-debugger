#!/usr/bin/python

class GUISizeProvider:
	def __init__(self):
		pass

	def w(self, w):
		return w * 1280

	def h(self, h):
		return h * 800

	@staticmethod
	def max(x, y):
		return (max(x[0], y[0]), max(x[1], y[1]))

