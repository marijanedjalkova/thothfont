

def main():
	with open("hiero.fea") as feaFile:
		content = feaFile.readlines()
	inFeature = False
	inLookup = False
	featureName = ""
	lookupName = ""
	for line in content:
		tokens = line.split()
		if len(tokens)==0:
			continue
		if not tokens[0] == "feature" and not inFeature:
			print "skipping {}".format(line)
			continue
		# if not line.startswith("lookup") and not inLookup:
		# 	print "2 skipping {}".format(line)
		# 	continue
		if tokens[0] == "feature":
			featureName = tokens[1]
			if inFeature:
				print "Nested features not allowed"
				raise Exception
			inFeature = True
			print featureName
			continue
		if tokens[0] == "lookup":
			lookupName = tokens[1]
			if inLookup:
				print "Nested lookups not allowed: lookup {}".format(lookupName)
				raise Exception
			inLookup = True
			continue
		if tokens[0] == "}":
			name = tokens[1][:-1]
			print "NAME END {}".format(name)
			if name == featureName:
				# end of feature 
				inFeature = False 
				print "end of ft {}".format(featureName)
			elif name == lookupName:
				inLookup = False 
			else:
				print "Unrecognized name: {}".format(name)
				raise Exception 
			continue
		# this is a sub or pos 




if __name__ == '__main__':
	main()