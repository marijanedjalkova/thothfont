
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
		pass

class Feature:

	def __init__(self, name):
		self.name = name
		self.lookups = []

	def addLookup(self, lookup):
		self.lookups.append(lookup)

	def toVOLT(self):
		pass


def main():
	with open("hiero.fea") as feaFile:
		content = feaFile.readlines()
	features = []
	currentLookup = None
	currentFeature = None
	for line in content:
		tokens = line.split()
		if len(tokens)==0:
			continue
		if not tokens[0] == "feature" and currentFeature is not None:
			# skip that for now
			continue
		if tokens[0] == "feature":
			featureName = tokens[1]
			if currentFeature is not None:
				print "Nested features not allowed"
				raise Exception
			currentFeature = Feature(featureName)
			continue
		if tokens[0] == "lookup":
			lookupName = tokens[1]
			if currentLookup is not None:
				print "Nested lookups not allowed: lookup {}".format(lookupName)
				raise Exception
			currentLookup = Lookup(lookupName)
			continue
		if tokens[0] == "}":
			name = tokens[1][:-1]
			if name == currentFeature.name:
				currentFeature.toVOLT()
				features.append(currentFeature)
				currentFeature = None
			elif name == currentLookup.name:
				feature.addLookup(currentLookup)
				currentLookup = None 
			else:
				print "Unrecognized name: {}".format(name)
				raise Exception 
			continue
		# this is a sub or pos 
		if tokens[0] == "lookupflag":
			flag = tokens[1][:-1]
			currentLookup.addItem(flag, True)



if __name__ == '__main__':
	main()