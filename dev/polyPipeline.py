#!/usr/bin/env python
import getopt, sys
import os
import subprocess

inputFile = ""


def checkSlice(inputFile):
	#need names of output files
	#verifies the output file is readable/writable
	return

def launchSlice(inputString):
	cmd = r'C:\Users\Jackson\Documents\school\CSBS\46X\UltimakerCura3.0\Cura.exe %s' % inputString
	subprocess.call(cmd)
	return

def checkConversion(inputFile):
	#need names of output files
	#verifies the output file is readable/writable
	return

def launchConversion(inputFile):
	print("Please create multiple .stl files using your input file\n")
	#cmd = r'C:\Users\Jackson\Documents\school\CSBS\46X\Chimera1.12\bin\chimera.exe %s' % inputFile
	cmd = r'C:\Users\Jackson\Documents\school\CSBS\46X\Chimera1.12\bin\chimera.exe'
	subprocess.call(cmd)
	return

def launchPrint(inputFile):
	cmd = r'C:\Program Files\Chroma\Chroma.exe'
	subprocess.call(cmd)
	return
	
def validSTL(inputFile):
	#exit(1) if file is invalid
	return 1 #file type


def validPDB(inputFile):
	#exit(1) if file is invalid
        return 2


def fileValidate(inputFile):
	tempType = 0
	ext = inputFile[-4:]
	if(ext[0] == "."):
		ext = ext[-3:]
	if(ext == "pdb" or ext == "PDB"):
		tempType = validPDB(inputFile)
	elif(ext == "stl" or ext == "STL"):
		tempType = validSTL(inputFile)
	else:
		print ("Input file is of invalid type!\n")
		sys.exit(1)
	return tempType


def usage():
	print ("\nPolyChromatic 3D Printing Pipeline\n\nDeveloped by:\n\tJoshua Lioy, Corynna Park, Jackson Wells\n\nUsage:\n\t./polyPipeline.py -i [input file]\n\nFlags:\n\t-h\tdisplayes usage\n\t-i\tto input file\n\t-v\tfor verbose program output\n\n")


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:v", ["help", "input="])
	except getopt.GetoptError as err:
		print (err)
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
		else:
			assert False, "unhandled option"
	if not fileInput:
		print ("\nNo input file specified!\nUse -h to display usage statement\n")
		sys.exit(2)
	else:
		if(verbose):
	                print ("Validating input file\n")
		fileType = fileValidate(inputFile)
	if(verbose):
                print ("File valid!\n")
	if(fileType == 1):
		#STL file input
		#launch slicing software CURA
                if(verbose):
                        print ("Launching CURA\n")
                launchSlice(inputFile)
                if(verbose):
			print ("Launching Chroma\n")
                launchPrint("water.gcode")
		sys.exit(0)
	elif(fileType == 2):
		#PDB files 
		#launch Chimera to convert & split into multiple STLs
		if(verbose):
                        print ("Launching Chimera\n")
		launchConversion(inputFile)
		#launch slicing software CURA
		if(verbose):
                        print ("Launching CURA\n")
		launchSlice("O.stl H.stl")
		if(verbose):
			print ("Launching Chroma\n")
		launchPrint("water.gcode")
		sys.exit(0)
	else:
		sys.exit(0);

if __name__ == "__main__":
    main()

#getopt from python documentation, needs actual citation
