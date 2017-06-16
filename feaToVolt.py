import os
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

	def toVOLT(self):
		direction = "RTL" if "RightToLeft" in self.flags else direction = "LTR"
		marks = "ALL"
		base = "PROCESS_BASE" # possibly empty string
		res = ("DEF_LOOKUP \"{}\" {} PROCESS_MARKS {} DIRECTION {}\n").format(feature.name, base, marks, direction)
		res += "IN_CONTEXT\n"
		# TODO possibly
		res += "END_CONTEXT\n"
		if self.isSUB():
			res =+ "AS_SUBSTITUTION\n"
			for rule in self.rules:
				pass
				# TODO
			res += "END_SUB\n"
		else:
			res += "AS_POSITION\n"
			for rule in self.rules:
				pass
				# TODO
			res += "END_POSITION\n"

		retun res

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
		res = ("DEF_FEATURE NAME \"{}\" TAG \"{}\"\n").format(feature.name, self.get_tag())
		lks = ""
		for lookupName in self.lookupNames:
			lks += "LOOKUP \"{}\" ".format(lookupName)
			res += lks
			res += "\n"
		res += "END_FEATURE\n"
		return res
	

def file_to_features():
	# TODO might need to not only return
	# features but also more than that

	with open("hiero.fea") as feaFile:
		content = feaFile.readlines()
	features = []
	currentLookup = None
	currentFeature = None
	for line in content:
		tokens = line.split()
		if len(tokens)==0:
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
				currentFeature.addLookup(currentLookup)
				currentLookup = None 
			else:
				print "Unrecognized name: {}".format(name)
				raise Exception 
			continue
		if tokens[0] == "lookupflag":
			flag = tokens[1][:-1]
			currentLookup.addItem(flag, True)
		currentLookup.addItem(line)
	# data ready at this point
	res = {'features': features}
	# TODO might need to add more	
	return res

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
					if 'features' in lang:
						for feature in lang['features']:
							feature_stringified = feature.toVOLT()
							result_file.write(feature_stringified)
					result_file.write("END_LANGSYS\n")
			result_file.write("END_SCRIPT\n")

def define_groups(data, result_file):
	if 'groups' in data:
		for entry in data['groups']:
			pass
			# TODO maybe

def define_lookups(data, result_file):
	if 'features' in data:
		for feature in data['features']:
			stringified = feature.toVOLT()
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