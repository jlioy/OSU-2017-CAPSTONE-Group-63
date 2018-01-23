#!/usr/bin/env python
import getopt, sys

inputFile = ""

def sendDirect(inputFile):
	#sends output to printer via direct USB connection
	#check if printing
	return

def sendNetwork(inputFile):
	#sends output to printer via LAN connection
	#check if printing
	#add to queue
	return

def isPrinting():
	#check if printer is currently in use
	return


def checkSlice(inputFile):
	#verifies the output file is readable/writable
	return

def launchSlice(inputFile):
	return

def checkConversion(inputFile):
	#verifies the output file is readable/writable
	return

def launchConversion(inputFile):
	return

def validSTL(inputFile):
	#exit(1) if file is invalid
	return 1 #file type


def validCIF(inputFile):
	#exit(1) if file is invalid
        return 2


def validPDB(inputFile):
	#exit(1) if file is invalid
        return 3


def valid3MF(inputFile):
	#check for color information
	#exit(1) if file is invalid
        return 4


def validWRL(inputFile):
	#check for color information
	#exit(1) if file is invalid
        return 5


def fileValidate(inputFile):
	tempType = 0
	ext = inputFile[-4:]
	if(ext[0] == "."):
		ext = ext[-3:]
	if(ext == "cif" or ext == "CIF"):
		tempType = validCIF(inputFile)
	elif(ext == "pdb" or ext == "PDB"):
		tempType = validPDB(inputFile)
	elif(ext == "3mf" or ext == "3MF"):
		tempType = valid3MF(inputFile)
	elif(ext == "wrl" or ext == "WRL"):
		tempType = validWRL(inputFile)
	elif(ext == "stl" or ext == "STL"):
		tempType = validSTL(inputFile)
	else:
		print "Input file is of invalid type!\n"
		sys.exit(1)
	return tempType


def usage():
	print "\nPolyChromatic 3D Printing Pipeline\n\nDeveloped by:\n\tJoshua Lioy, Corynna Park, Jackson Wells\n\nUsage:\n\t./polyPipeline.py -i [input file]\n\nFlags:\n\t-h\tdisplayes usage\n\t-i\tto input file\n\t-v\tfor verbose program output\n\t-d\tfor direct file transfer to printer\n\t-n\tfor network file transfer to printer\n\n"


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:vnd", ["help", "input=","network","direct"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)
	verbose = False
	network = False
	direct = False
	fileInput = False
	for o, a in opts:
	        if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-i", "--input"):
			inputFile = a
			fileInput = True
		elif o in ("-d", "--direct"):
			if(network == False):
				direct  = True
		elif o in ("-n", "--network"):
			if(direct == False):
				network = True
		else:
			assert False, "unhandled option"
	if not fileInput:
		print "\nNo input file specified!\nUse -h to display usage statement\n"
                sys.exit(2)
	else:
		if(verbose):
	                print "Validating input file\n"
		fileType = fileValidate(inputFile)
	if(verbose):
                print "File valid!\n"
	if(fileType == 1):
		#STL file input
		#ignore files of this type??
		sys.exit(0)
	elif(fileType > 1 and fileType < 4):
		#PDB or CIF file input
		#launch PyMol to convert & color file
		if(verbose):
                        print "Launching PyMol\n"
		#launch slicing software CURA
		if(verbose):
                        print "Launching CURA\n"
		if(direct):
			sendDirect(inputFile)
		elif(network):
			sendNetwork(inputFile)
	elif(fileType > 3 and fileType < 6):
		#3MF or WRL file input
		#launch slicing software CURA
		if(verbose):
                        print "Launching CURA\n"
		if(direct):
			sendDirect(inputFile)
		elif(network):
			sendNetwork(inputFile)
	else:
		sys.exit(0);

if __name__ == "__main__":
    main()

#getopt from python documentation, needs actual citation
