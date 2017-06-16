

def main():
	with open("hiero.fea") as feaFile:
		content = feaFile.readlines()
	print len(content)

if __name__ == '__main__':
	main()