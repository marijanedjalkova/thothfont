import os

class Rule:

	def __init__(self, feature_string):
		# skip semicolon at the end
		semicolon_index = feature_string.index(";")
		if semicolon_index != -1:
			feature_string = feature_string[:semicolon_index]
		self.feature_string = feature_string
		self.tokens = self.feature_string.split()
		if (self.tokens[-1]).endswith(";"):
			raise Exception

	def isSUB(self):
		return self.tokens[0] == "sub"

	def context_toVOLT(self): # might need to filter subs only

		# everything on the LHS that is without the prime
		res = ""
		if self.isSUB():
			by_index = self.tokens.index("by")
			needed_tokens = self.tokens[1:by_index]
			prime_index = -1
			for t in needed_tokens:
				if t.endswith("'"):
					prime_index = needed_tokens.index(t)
					break
			if prime_index != -1:
				context_before = needed_tokens[:prime_index]

				context_after = needed_tokens[prime_index+1:]

				if len(context_before) > 0:
					res += "LEFT "
					for b in context_before:
						res += self.token_toVOLT(b)
						res += " "
				if len(context_after) > 0:
					res += "RIGHT "
					for a in context_after:
						res += self.token_toVOLT(a)
						res += " "
		return res

	def getWhatToSub(self):
		# with the prime 
		res = ""
		by_index = self.tokens.index("by")
		needed_tokens = self.tokens[1:by_index]
		for t in needed_tokens:
			if t.endswith("'"):
				return self.token_toVOLT(t[:-1])
		# if we are here then there is all of the LHS
		for t in needed_tokens:
			res += self.token_toVOLT(t)
		return res

	def getWhatToSubWith(self):
		by_index = self.tokens.index("by")
		needed_tokens = self.tokens[by_index+1:]
		res = ""
		for t in needed_tokens:
			res += self.token_toVOLT(t)
		return res

	def token_toVOLT(self, t):
		if t.startswith("<"):
			return "GROUP {} ".format(t[1:-1])
		return "GLYPH {} ".format(t)

	def toVOLT(self):
		if self.isSUB():
			return self.sub_toVOLT()
		return self.pos_toVOLT()
		

	def sub_toVOLT(self):
		# sub svrec.h.nil.mark' hrec.h.333.mark svrec.h.333.mark by svrec.h.666.mark;		

		"""
		SUB GLYPH "Qf" GROUP "controls"
		WITH GROUP "controls"
		END_SUB
		"""
		res = "SUB \n{}".format(self.getWhatToSub())
		res += "WITH {}\n".format(self.getWhatToSubWith())
		res += "END_SUB\n"
		return res

	def pos_toVOLT(self):
		# pos anchor.pos.1000.1000 period' <1000 1000 -1000 0> ;
		"""ATTACH GROUP "quadratBases" GROUP "quadratCartouches"
		TO GROUP "stems0-v" AT ANCHOR "a1"
		END_ATTACH"""

		"""ADJUST_SINGLE GLYPH "mtr" BY POS DX 915 END_POS
		END_ADJUST""" # there are more
		return "" # TODO

class Lookup:

	def __init__(self, name):
		self.name = name
		self.flags = []
		self.rules = []

	def addItem(self, item, isFlag = False):
		if isFlag:
			self.flags.append(item)
		else:
			self.rules.append(item)

	def context_toVOLT(self):
		if len(self.rules) > 0:
			return self.rules[0].context_toVOLT()
		return "" 

	def marks_toVOLT(self):
		return "PROCESS_MARKS ALL" # TODO there are other cases

	def base_toVOLT(self):
		if "IgnoreBaseGlyphs" in self.flags:
			return " "
		return "PROCESS_BASE" 

	def direction_toVOLT(self):
		if "RightToLeft" in self.flags:
			return "DIRECTION RTL"
		return "DIRECTION LTR"

	def isSUB(self):
		if len(self.rules) == 0:
			return False 
		return self.rules[0].isSUB()


	def toVOLT(self):
		direction = self.direction_toVOLT()
		marks = self.marks_toVOLT()
		base = self.base_toVOLT()
		res = ("DEF_LOOKUP \"{}\" {} {} {}\n").format(self.name, base, marks, direction)
		res += "IN_CONTEXT\n"
		res += self.context_toVOLT()
		res += "END_CONTEXT\n"
		if self.isSUB():
			res += "AS_SUBSTITUTION\n"
			for rule in self.rules:
				res += rule.toVOLT() 
			res += "END_SUBSTITUTION\n"
		else:
			res += "AS_POSITION\n"
			for rule in self.rules:
				res += rule.toVOLT() 
			res += "END_POSITION\n"

		return res

class Feature:

	def __init__(self, name):
		self.name = name
		self.lookupNames = []

	def addLookup(self, lookupName):
		self.lookupNames.append(lookupName)

	def get_tag(self):
		return "mkmk"
		# TODO

	def toVOLT(self):
		res = ("DEF_FEATURE NAME \"{}\" TAG \"{}\"\n").format(self.name, self.get_tag())
		lks = ""
		for lookupName in self.lookupNames:
			lks += "LOOKUP \"{}\" ".format(lookupName)
		res += lks
		res += "\n"
		res += "END_FEATURE\n"
		return res 

class Group:

	def __init__(self, name, items = []):
		self.name = name 
		self.items = items 

	def addItem(self, item):
		self.items.append(item)

	def toVOLT(self):
		"""DEF_GROUP "cartouches"
		 ENUM GROUP "quadratBases" GROUP "quadratCartouches" END_ENUM
		END_GROUP"""
		res = "DEF_GROUP \"{}\"\n".format(self.name)
		res += "ENUM "
		for item in self.items:
			# TODO can be groups, too(?)
			res += "GLYPH \"{}\" ".format(item)
		res += "END_ENUM\n"
		res += "END_GROUP\n"
		return res
	

def file_to_features():
	# TODO might need to not only return
	# features but also more than that

	with open("hiero.fea") as feaFile:
		content = feaFile.readlines()
	groups = []
	features = []
	lookups = []
	currentLookup = None
	currentFeature = None
	for i in range(len(content)):
		line = content[i]
		tokens = line.split()
		if len(tokens)==0:
			continue
		if tokens[0] == "markClass":
			endtokens = tokens 
			j = i + 1
			while not endtokens[-1].endswith(";"):
				# read next line, add to tokens 
				endtokens = content[j].split() 
				tokens.extend(endtokens) 
				j += 1
			# no need to add anything else 
			# can now create a group
			groups.append(parseGroup(tokens))
			continue
		if not tokens[0] == "feature" and currentFeature is None:
			# skip that for now, that's the header, might be groups
			continue
		if tokens[0] == "feature":
			if currentFeature is not None:
				print "Nested features not allowed"
				raise Exception
			currentFeature = Feature(tokens[1])
			continue
		if tokens[0] == "lookup":
			if currentLookup is not None:
				print "Nested lookups not allowed"
				raise Exception
			currentLookup = Lookup(tokens[1])
			continue
		if tokens[0] == "}":
			name = tokens[1][:-1]
			if name == currentFeature.name:
				features.append(currentFeature)
				currentFeature = None
			elif name == currentLookup.name:
				currentFeature.addLookup(name)
				lookups.append(currentLookup)
				currentLookup = None 
			else:
				print "Unrecognized name: {}".format(name)
				raise Exception 
			continue
		if tokens[0] == "lookupflag":
			flag = tokens[1][:-1]
			currentLookup.addItem(flag, True)
			continue
		currentLookup.addItem(Rule(line))
	# data ready at this point
	res = {'groups': groups, 'features': features, 'lookups':lookups}
	# TODO might need to add more	
	return res

def parseGroup(tokens):
	openIndex = tokens.index("[")
	closeIndex = tokens.index("]")
	items = tokens[openIndex+1: closeIndex]
	name = tokens[-1][1:-1]
	return Group(name, items)

def define_glyphs(data, result_file):
	if 'glyphs' in data:
		for glyph in data['glyphs']:
			pass
		# TODO not in our fea file so skip

def define_scripts(data, result_file):
	if 'scripts' in data: 
		for script in data['scripts']:
			result_file.write(("DEF_SCRIPT NAME \"{}\" TAG \"{}\"\n").format(script['name'], script['tag']))
			if 'langs' in script:
				for lang in script['langs']:
					result_file.write(("DEF_LANGSYS NAME \"{}\" TAG \"{}\"\n").format(lang['name'], lang['tag']))
					# in the dict, only need to name the features 
					write_feature_definitions_VOLT(lang, result_file)
					result_file.write("END_LANGSYS\n")
			result_file.write("END_SCRIPT\n")
	else:
		# TODO might actually create a default script if none are defined
		write_feature_definitions_VOLT(data, result_file)

def write_feature_definitions_VOLT(data, result_file):
	if 'features' in data:
		for feature in data['features']:
			feature_stringified = feature.toVOLT()
			result_file.write(feature_stringified)


def define_groups(data, result_file):
	if 'groups' in data:
		for entry in data['groups']:
			stringified = entry.toVOLT()
			result_file.write(stringified)

def define_lookups(data, result_file):
	if 'lookups' in data:
		for lookup in data['lookups']:
			stringified = lookup.toVOLT()
			result_file.write(stringified)


def define_anchors(data, result_file):
	if 'anchors' in data:
		for entry in data['anchors']:
			pass
			# TODO not in our fea file so skip

def define_PPEM(data, result_file):
	if 'ppem' in data:
		for entry in data['ppem']:
			pass
			# TODO not in our fea file so skip

def define_CMAP(data, result_file):
	if 'cmap' in data:
		for entry in data['cmap']:
			pass
			# TODO not in our fea file so skip

def create_output(data):
	with open("projfile.vtp", "w") as result_file:
		define_glyphs(data, result_file)
		define_scripts(data, result_file)
		define_groups(data, result_file)
		define_lookups(data, result_file)
		define_anchors(data, result_file)
		define_PPEM(data, result_file)
		define_CMAP(data, result_file)


def main():
	data = file_to_features()
	create_output(data)


if __name__ == '__main__':
	main()