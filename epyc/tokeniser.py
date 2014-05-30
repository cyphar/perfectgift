#!/usr/bin/env python3
# epyc: python-like templating langauge (Embedded PYthon Code)
# Copyright (C) 2014 Peter Brock

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

def find_token(string, upto, token):
	# search for }} if not found then throw exception
	for i in range(upto, len(string)-1):
		# iterate through until token controls
		# looking for {{ or {%
		if string[i:i+2] == token:
			# found string
			return i
	raise Exception('Tokeniser failed to find matching end token! Start token {} at {} missing end token {}'.format(string[upto-2:upto], upto - 2, token))

def tokenise(template_string):
	# return a list of tokens
	tokens = []
	upto = 0 # sting index
	token_start = upto
	token_found = False

	while upto < len(template_string):
		#print(upto, template_string[upto])
		#iterate through until token controls
		# looking for {{ or {%
		if (upto < len(template_string)-1) and (template_string[upto:upto+2] in ['{{', '{%', '{#']):
			if upto > 0 and token_start < upto - 1:
				# add HTML token
				tokens.append(template_string[token_start:upto])
				token = template_string[upto:upto+2]
				#print('found token {0} at {1}'.format(token, upto))

			token = template_string[upto:upto+2]
			#print('found token {0} at {1}'.format(token, upto))
			upto += 2
			token_start = upto
			if token == '{{':
				upto = find_token(template_string, upto, '}}')
			elif token == '{%':
				upto = find_token(template_string, upto, '%}')
			elif token == '{#':
				upto = find_token(template_string, upto, '#}')

			if token != '{#':
				tokens.append(token)
				tokens.append(template_string[token_start:upto])
				token = template_string[upto:upto+2]
				#print('found token {0} at {1}'.format(token, upto))
				tokens.append(token)
			upto += 2
			token_start = upto
		else:
			upto += 1
	if upto > 0 and token_start < upto - 1:
		# add HTML token
		tokens.append(template_string[token_start:upto])
		token = template_string[upto:upto+2]
		#print('found token {0} at {1}'.format(token, upto))
	return tokens

if __name__ == "__main__":
	def test_tokenise(string):
		tokens = tokenise(string)
		for i, t in enumerate(tokens):
			print('token {0} is {1}'.format(i, t))
		print(tokens)


	template = '''aaa{#comment#}aaa{% include header.html %}
	<token id='profile'>
	<h1>{{ person.name }}</h1>
	<ul id='friends-list'>
	{% for f in person.friends %}
	<li class='friend'>
	{{ f.name.title() }} {{ f.age }} {% if f.gender == 'M' %}Male{% else %}Female{% end if %}
	</li>
	{% end for %}
	</ul>
	</token>
	{% include footer.html %}
	<p>the end</p>'''

	test_tokenise(template)

