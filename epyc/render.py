#!/usr/bin/env python3
# epyc: python-like templating langauge (Embedded PYthon Code)
# Copyright (C) 2014 Cyphar
# Copyright (C) 2014 JoshLeeb

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

import html
import epyc

from .scope import Scope

def sanitise(string):
	return html.escape(str(string))


class ParseError(Exception):
	pass


# Node Classes
# Used in the parsing and evaluation to define the syntax tree.
class Node:
	"Node meta-class."
	def __init__(self):
		pass

	def render(self, context={}, path="."):
		raise NotImplementedError("node meta-class cannot be evaluated")


class GroupNode(Node):
	def __init__(self, children):
		self.children = children

	def render(self, context=None, path="."):
		"Render all children in group."

		# Scope this spruce goose.
		context = Scope(parent=context)

		ret = ""
		for child in self.children:
			render = child.render(context, path) or ""
			ret += str(render)

		return ret


class TextNode(Node):
	def __init__(self, content):
		self.content = content

	def render(self, context={}, path="."):
		"Render sanitised content"
		return self.content


class IncludeNode(Node):
	def __init__(self, path):
		self.path = path

	def render(self, context=None, path="."):
		"Return rendered content from file at path"
		return epyc.render(path + "/" + self.path, context)

class ForNode(Node):
	def __init__(self, identifier, expression, block):
		self.identifier = identifier
		self.expression = expression
		self.block = block

	def render(self, context={}, path="."):
		ret = ''

		try:
			L = eval(self.expression, {}, context)
		except:
			return None

		for item in L:
			try:
				getnext = "%s = __item__" % self.identifier
				exec(getnext, {"__item__": item}, context)
			except:
				return None

			ret += self.block.render(context, path) or ''

		return ret


class LetNode(Node):
	def __init__(self, identifier, expression):
		self.identifier = identifier
		self.expression = expression

	def render(self, context={}, path="."):
		code = "%s = %s" % (self.identifier, self.expression)

		try:
			exec(code, {}, context)
		except:
			pass

		return None

class ExprNode(Node):
	def __init__(self, content):
		self.content = content

	def render(self, context={}, path="."):
		"Return evaluated content or None"
		try:
			val = eval(self.content, {}, context)
		except:
			return None

		return sanitise(val)


class ExecNode(Node):
	def __init__(self, content):
		self.content = content

	def render(self, context={}, path="."):
		"Execute a statment. Always returns None."
		try:
			exec(self.content, {}, context)
		except:
			pass


class IfNode(Node):
	def __init__(self, nodes):
		# [(cond, node), ...] in order of
		self.nodes = nodes

	def render(self, context={}, path="."):
		for condition, node in self.nodes:
			if not condition:
				return node.render(context, path)

			try:
				cond = eval(condition, {}, context)
			except:
				cond = False

			if cond:
				return node.render(context, path)
