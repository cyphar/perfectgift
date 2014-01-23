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
				getnext = "%s = __item__" % self.identifier
				exec(getnext, {"__item__": item}, scope)
			except:
				return None

			ret += self.block.render(scope, path) or ''

		return ret


class LetNode(Node):
	def __init__(self, identifier, expression):
		self.identifier = identifier
		self.expression = expression

	def render(self, scope={}, path="."):
		code = "%s = %s" % (self.identifier, self.expression)

		try:
			exec(code, {}, scope)
		except:
			pass

		return None

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
	def __init__(self, nodes):
		# [(cond, node), ...] in order of
		self.nodes = nodes

	def render(self, scope={}, path="."):
		for condition, node in self.nodes:
			if not condition:
				return node.render(scope, path)

			try:
				cond = eval(condition, {}, scope)
			except:
				cond = False

			if cond:
				return node.render(scope, path)
