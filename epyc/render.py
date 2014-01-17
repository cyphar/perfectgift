#!/usr/bin/env python3

import html
import epyc

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

	def render(self, scope={}, path="."):
		raise NotImplementedError("node meta-class cannot be evaluated")


class GroupNode(Node):
	def __init__(self, children):
		self.children = children

	def render(self, scope={}, path="."):
		"Render all children in group."
		ret = ""

		for child in self.children:
			render = child.render(scope, path)
			if render is None:
				render = ""
			ret += str(render)
		return ret


class TextNode(Node):
	def __init__(self, content):
		self.content = content

	def render(self, scope={}, path="."):
		"Render sanitised content"
		return self.content


class IncludeNode(Node):
	def __init__(self, path):
		self.path = path

	def render(self, scope={}, path="."):
		"Return rendered content from file at path"
		return epyc.render(path + "/" + self.path, scope)

class ForNode(Node):
	def __init__(self, identifier, expression, block):
		self.identifier = identifier
		self.expression = expression
		self.block = block

	def render(self, scope={}, path="."):
		ret = ''

		try:
			L = eval(self.expression, {}, scope)
		except:
			return None

		for item in L:
			try:
				getnext = "%s = %r" % (self.identifier, item)
				exec(getnext, {}, scope)
			except:
				return None

			ret += self.block.render(scope, path) or ''

		return ret


class ExprNode(Node):
	def __init__(self, content):
		self.content = content

	def render(self, scope={}, path="."):
		"Return evaluated content or None"
		try:
			val = eval(self.content, {}, scope)
		except:
			return None

		return sanitise(val)


class IfNode(Node):
	def __init__(self, condition, ifnode, elsenode=None):
		self.ifnode = ifnode
		self.elsenode = elsenode
		self.condition = condition

	def render(self, scope={}, path="."):
		try:
			cond = eval(self.condition, {}, scope)
		except:
			return self.elsenode.render(scope, path)

		if cond:
			return self.ifnode.render(scope, path)
		elif self.elsenode:
			return self.elsenode.render(scope, path)
