#!/usr/bin/env python3

from . import render

class ParseException(Exception):
	pass

class Parser:
	"Main parsing class."
	def __init__(self, tokens):
		self.tokens = tokens
		self.pos = 0
		self.length = len(tokens)

	def end(self):
		return self.pos == self.length

	def peek(self):
		if not self.end():
			return self.tokens[self.pos]

	def next(self, num=1):
		if not self.end():
			self.pos += num

	def _parse_token(self):
		if self.end():
			return None

		# expr
		if self.peek() == "{{":
			self.next()

			expr = render.ExprNode(self.peek())
			self.next()

			if not expr or self.peek() != "}}":
				raise ParseError("error parsing expression")

			self.next()
			return expr
		if self.peek() == "{%":
			self.next()

			if self.end():
				raise ParseException("missing closing {% tag %}")

			tag = self.peek().strip().split()

			# only {% %} -- no information
			if not tag:
				raise ParseException("no type information for {% tag %}")

			self.next()
			if self.peek() != "%}":
				raise ParseException("too many tokens in {% tag %}")

			self.next()

			tp = tag[0]
			args = " ".join(tag[1:])

			if tp == "include":
				args = args.split()

				if len(args) == 1:
					ret = render.IncludeNode(args[0])
					return ret

				raise ParseException("wrong number of arguments to {% include <file> %}")

			elif tp == "for":
				# {% for <var> in <expr> %}
				slen = len('in')
				sep = args.find("in")

				if sep < 0:
					raise ParseException("missing 'in' in {% for <var> in <expr> %}")

				var, expr = args[:sep].strip(), args[sep + slen:].strip()

				block = self._parse_group(["end for"])
				node = render.ForNode(var, expr, block)

				if not self._check_end(["end for"]):
					raise ParseException("missing {% end for %}")

				self.next(3)
				return node
			elif tp == "if":
				# {% if <pred> %}
				if not args:
					raise ParseException("no predicate for 'if' condition")

				predicate = args
				ifblock = self._parse_group(["end if", "else"])
				elseblock = None

				if self._check_end(["else"]):
					elseblock = self._parse_group(["end if"])

				node = render.IfNode(predicate, ifblock, elseblock)

				if not self._check_end(["end if"]):
					raise ParseException("missing {% end if %}")

				self.next(3)
				return node
		# text
		else:
			text = self.peek()
			self.next()
			return render.TextNode(text)

	def _check_end(self, ends):
		if not ends:
			return False

		pos = self.pos

		if self.length - pos < 3:
			return False

		if self.tokens[pos] == "{%":
			pos += 1
			tag = self.tokens[pos].split()
			tag = " ".join([item.strip() for item in tag])

			pos += 1
			if self.tokens[pos] != "%}":
				return False

			return tag in ends

	def _parse_group(self, ends=None):
		groups = []

		while not self.end() and not self._check_end(ends):
			groups.append(self._parse_token())

		groups = [group for group in groups if group]
		return render.GroupNode(groups)

	def parse(self):
		# EBNF for epyc:
		# group = (token)+
		# token = expr
		# token = text
		# expr	= {{ <any python expression> }}
		# text	= <any text>

		return self._parse_group()
