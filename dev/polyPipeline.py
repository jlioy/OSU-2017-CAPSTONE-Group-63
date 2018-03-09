#!/usr/bin/env python
# coding=UTF-8
import getopt, sys
import os
import subprocess
import re

inputFile = ""
chimDir = ""
curaDir = ""
chroDir = "" 

def launchSlice(inputString):
	cmd = '%s %s' % (curaDir,inputString)
	subprocess.call(cmd)
	return

def launchConversion(inputFile):
	cmd = "%s %s" % (chimDir,inputFile)
	subprocess.call(cmd)
	return

def launchPrint():
	subprocess.call(chroDir)
	return
	
def validSTL(inputFile):
	if not os.path.isfile(inputFile):
		print ("File Does Not Exist!\n")	
		sys.exit(1)
	regexp = re.compile(r'[A-Za-z0-9.-+]')
        f = open(inputFile, "r")
        for line in f:
                if not (regexp.search(line)):
                        print("Invalid File Format!\n")
                        sys.exit(2)
	return 1 #file type


def validPDB(inputFile):
	if not os.path.isfile(inputFile):
                print ("File Does Not Exist!\n")
                sys.exit(1)
	endFlag = 0
	regexp = re.compile(r'[A-Za-z0-9.-]')
	f = open(inputFile, "r")
	for line in f:
		if "END" in line:
			endFlag = 1
		elif not (regexp.search(line)):
			print("Invalid File Format!\n")
                	sys.exit(2)
	if endFlag:
		return 2
	else:
		print("Invalid File Format!\n")
		sys.exit(2)


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
		print ("Invalid File Type!\n")
		sys.exit(1)
	return tempType


def usage():
	print ("\nPolyChromatic 3D Printing Pipeline\n\nDeveloped by:\n\tJoshua Lioy, Corynna Park, Jackson Wells\n\nUsage:\n\t./polyPipeline.py -i [input file]\n\nFlags:\n\t-h\tdisplayes usage\n\t-i\tto input file\n\t-v\tfor verbose program output\n\n")


def readConfiguration():
	global chimDir,chroDir,curaDir
	f = open("paths.conf","r") 
	for line in f:	
		if "Chimera:" in line:	
			chimDir = line.rstrip()
			chimDir = chimDir[8:]
		elif "Cura:" in line:
			curaDir = line.rstrip()
			curaDir = curaDir[5:]	
		elif "Chroma:" in line:	
			chroDir = line.rstrip()
			chroDir = chroDir[7:]
	f.close()
	return


def main():
	readConfiguration()
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
		print ("\nNo input file specified!\n\nUse -h to display usage statement\n")
		sys.exit(2)
	else:
		if(verbose):
	                print ("Validating input file\n")
		fileType = fileValidate(inputFile)
	if(verbose):
                print ("File valid!\n")
	if(fileType == 1):
		if(verbose):
			print ("Launching CURA\n")
		launchSlice(inputFile)
		if(verbose):
			print ("Launching Chroma\n")
		launchPrint()
		sys.exit(0)
	elif(fileType == 2):
		if(verbose):
			print ("Launching Chimera\n")
		launchConversion(inputFile)
		if(verbose):
			print ("Launching CURA\n")
		launchSlice("")
		if(verbose):
			print ("Launching Chroma\n")
		launchPrint()
		sys.exit(0)
	else:
		sys.exit(0);

if __name__ == "__main__":
    main()

#getopt from python documentation, needs actual citation
