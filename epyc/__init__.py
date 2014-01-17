#!/usr/bin/env python3

import os
from . import tokeniser
from . import parser

def render(fname, scope={}):
	with open(fname) as f:
		content = f.read()
	return _render(content, scope, os.path.dirname(fname))

def _render(content, scope={}, path="."):
	return parser.Parser(tokeniser.tokenise(content)).parse().render(scope, path)
