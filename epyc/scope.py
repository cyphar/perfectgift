#!/usr/bin/env python3
# epyc: python-like templating langauge (Embedded PYthon Code)
# Copyright (C) 2014 Cyphar

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Scope Class
# Used to allow for global and local variable separation.
class Scope(dict):
	'''
	A dict-like scoping object, resolving global and local variables.
	It chiefly allows for global and local scope separation.
	'''
	def __init__(self, items=None, parent=None):
		self.items = items or {}
		self.parent = parent

	def __repr__(self):
		return "Scope(items={!r}, parent={!r})".format(self.items, self.parent)

	def __str__(self):
		return "Scope(items={!r}, parent={!r})".format(self.items, self.parent)

	def __getitem__(self, key):
		if key in self.items:
			return self.items[key]

		if self.parent:
			return self.parent[key]

		raise KeyError("no such variable in current scope")

	def __setitem__(self, key, value):
		if self.parent and key in self.parent:
			self.parent[key] = value
		else:
			self.items[key] = value

	def __contains__(self, key):
		if key in self.items:
			return True

		if self.parent:
			return key in self.parent

		return False

	def __len__(self):
		size = len(self.items)

		if self.parent:
			size += len(self.parent)

		return size

	def __bool__(self):
		return True
