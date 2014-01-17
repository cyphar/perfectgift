#!/usr/bin/env python3

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
		if upto < len(template_string) -1 and (template_string[upto:upto+2] == '{{' or template_string[upto:upto+2] == '{%'):
			if upto > 0 and token_start < upto - 1:
				# add HTML token
				tokens.append(template_string[token_start:upto])
				token = template_string[upto:upto+2]
				#print('found token {0} at {1}'.format(token, upto))

			token = template_string[upto:upto+2]
			#print('found token {0} at {1}'.format(token, upto))
			token_start = upto
			tokens.append(template_string[token_start:upto+2])
			upto += 2
			token_start = upto

			if token == '{{':
				upto = find_token(template_string, upto, '}}')
			elif token == '{%':
				upto = find_token(template_string, upto, '%}')

			tokens.append(template_string[token_start:upto])
			token = template_string[upto:upto+2]
			#print('found token {0} at {1}'.format(token, upto))
			tokens.append(template_string[upto:upto+2])
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
	def test_tokeniser(string):
		tokens = tokeniser(string)
		for i, t in enumerate(tokens):
			print('token {0} is {1}'.format(i, t))
		print(tokens)


	template = '''aaa{% include header.html %}
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

	test_tokeniser(template)

