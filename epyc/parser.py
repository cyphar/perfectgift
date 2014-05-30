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

				block = self._parse_group([["end", "for"]])
				node = render.ForNode(var, expr, block)

				if not self._check_end([["end", "for"]]):
					raise ParseException("missing {% end for %}")

				self.next(3)
				return node

			elif tp == "if":
				# {% if <pred> %}
				if not args:
					raise ParseException("no predicate for 'if' condition")

				predicate = args

				ifblock = self._parse_group([["elif", ...], ["else"], ["end", "if"]])
				blocks = [(predicate, ifblock)]

				while self._check_end([["elif", ...], ["else"]]):
					tokens = self.tokens[self.pos:]

					start, tag, close = tokens[:3]
					tag, *predicate = tag.split()
					predicate = " ".join(predicate)

					self.next(3)
					if self._check_end([["else"]]):
						block = self._parse_group([["end", "if"]])
						blocks += [(None, block)]
						break

					else:
						block = self._parse_group([["elif", ...], ["else"], ["end", "if"]])
						blocks += [(predicate, block)]


				node = render.IfNode(blocks)

				if not self._check_end([["end", "if"]]):
					raise ParseException("missing {% end if %}")

				self.next(3)
				return node

			elif tp == "let":
				# {% let <expr> = <expr> %}

				if "=" not in args:
					raise ParseException("no '=' in {% let <expr> = <expr> %}")

				var, *sep, expr = args.split("=")

				if sep:
					raise ParseException("too many '=' in {% let <expr> = <expr> %}")

				return render.LetNode(var.strip(), expr.strip())

			elif tp == "exec":
				if not args:
					raise ParseException("no arguments to {% exec <expr> %} block")

				return render.ExecNode(args)

		# text
		else:
			text = self.peek()
			self.next()
			return render.TextNode(text)

	def _check_end(self, ends):
		if not ends:
			return False

		pos = self.pos
		tokens = self.tokens[pos:]

		# There are no {% ... %} tags left
		if len(tokens) < 3:
			return False

		start, tag, end = tokens[:3]

		if start != "{%" or end != "%}":
			return False

		# Get tag information.
		tag = tag.split()

		# '...' represents only the part UP TO the '...' is to be matched with the tag information,
		# as opposed to matching everything in the {% ... %} tags, and the rest will be ignored.

		valids = []
		for end in ends:
			full = True
			if ... in end:
				where = end.index(...)
				end = end[:where]
				full = False

			valids.append((end, full))

		for valid, full in valids:
			if valid == tag:
				return True

			if not full:
				section = tag[:len(valid)]
				if valid == section:
					return True

		return False

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
