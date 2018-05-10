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

def launchSliceWindows(inputString):       	#Method for launching Windows slicing software
        cmd = '%s %s' % (inputString,curaDir)
        subprocess.call(cmd,shell=True)
        return

def launchConversionWindows(inputFile):       	#Method for launching Windows conversion software
        cmd = "%s %s" % (inputFile,chimDir)
        subprocess.call(cmd,shell=True)
        return

def launchPrintWindows():                   	#Method for launching Windows printing software
        cmd = "%s" % chroDir         		#create cmd string with wait flag to hold execution
        subprocess.call(cmd,shell=True)
        return

def launchSliceOSX(inputString):		#Method for launching OSX slicing software
	cmd = 'open -W %s -a %s' % (inputString,curaDir)
	subprocess.call(cmd,shell=True)
	return

def launchConversionOSX(inputFile):		#Method for launching OSX conversion software
	cmd = "open -W %s -a %s" % (inputFile,chimDir)
	subprocess.call(cmd,shell=True)
	return

def launchPrintOSX():				#Method for launching OSX printing software
	cmd = "open -W -a %s" % chroDir		#create cmd string with wait flag to hold execution
	subprocess.call(cmd,shell=True)
	return
	
def validSTL(inputFile):			#method for validation of STL files
	if not os.path.isfile(inputFile):	#checks readability
		print ("File Does Not Exist!\n")	
		sys.exit(1)
	return 1 #file type


def validPDB(inputFile):			#method for PDB file validation
	if not os.path.isfile(inputFile):	#checks readability
                print ("File Does Not Exist!\n")
                sys.exit(1)
	endFlag = 0				#flag for detection of required file syntax
	regexp = re.compile(r'[A-Za-z0-9.-]')
	f = open(inputFile, "r")
	for line in f:				#loop over the file
		if "END" in line:		#if END is found
			endFlag = 1
		elif not (regexp.search(line)):	#if invalid characters are found
			print("Invalid File Format!\n")
			sys.exit(2)
	if endFlag:
		return 2
	else:					#if no END was found
		print("Invalid File Format!\n")
		sys.exit(2)


def fileValidate(inputFile):			#method that manages validation
	tempType = 0
	ext = inputFile[-4:]		#get extension from file name
	if(ext[0] == "."):
		ext = ext[-3:]
	if(ext == "pdb" or ext == "PDB"):
		tempType = validPDB(inputFile)	#validate the PDB file
	elif(ext == "stl" or ext == "STL"):
		tempType = validSTL(inputFile)  #validate the STL file
	else:					#if file is not PDB or STL
		print ("Invalid File Type!\n")
		sys.exit(1)
	return tempType


def usage():		#method for outputing usage information
	print ("\nPolyChromatic 3D Printing Pipeline\n\nDeveloped by:\n\tJoshua Lioy, Corynna Park, Jackson Wells\n\nUsage:\n\tpython polyPipeline.py [Optional Flags] [-w or -m]  -i [input file]\n\nFlags:\n\t-h\tdisplayes usage\n\t-i\tto input file\n\t-v\tfor verbose program output\n\t-w\tsets operating system to Windows\n\t-m\tsets operating system to OSX\n\n")


def readConfiguration():				#method for parsing the configuration file
	global chimDir,chroDir,curaDir		
	f = open("paths.conf","r") 
	for line in f:				#loop over config file
		if "Chimera:" in line:	
			chimDir = line.rstrip()
			chimDir = chimDir[8:]
		elif "Cura:" in line:			#store location information
			curaDir = line.rstrip()
			curaDir = curaDir[5:]	
		elif "Chroma:" in line:	
			chroDir = line.rstrip()
			chroDir = chroDir[7:]		
	f.close()
	return


def main():
	readConfiguration() 		#parses and stores information from paths.conf
	try:				#sematically identical to getopt in C
		opts, args = getopt.getopt(sys.argv[1:], "hi:vwm", ["help", "input="]) #possible input flags
	except getopt.GetoptError as err:
		print (err)
		usage()
		sys.exit(2)
	verbose = False
	fileInput = False
	OS = -1
	for o, a in opts:
		if o == "-v":
			verbose = True			#prints execution information
		elif o in ("-h", "--help"):
			usage()				#prints usage statement
			sys.exit()	
		elif o in ("-i", "--input"):
			inputFile = a			#supplies the input file
			fileInput = True
		elif o == "-w":				#flag for windows users
			OS = 1
		elif o == "-m":				#flag for Mac users
			OS = 2
		else:					#unknown flags handled here
			assert False, "unhandled option"
	if not fileInput:				#checking that input was made
		print ("\nNo input file specified!\n\nUse -h to display usage statement\n")	
		sys.exit(2)
	else:	#input was supplied
		if(verbose):
	                print ("Validating input file\n")
		fileType = fileValidate(inputFile)		#validate input file
	if(verbose):
                print ("File valid!\n")
	if(fileType == 1):			#if the input file is in STL format
		if(verbose):
			print ("Launching CURA\n")
		if(OS == 1):
			launchSliceWindows(inputFile)		
		elif(OS == 2):
			launchSliceOSX(inputFile)
		else:
			print ("Failure to supply an operating system type!\n")
			sys.exit(2)
		if(verbose):
			print ("Launching Chroma\n")
		if(OS == 1):
                        launchPrintWindows()
                elif(OS == 2):
                        launchPrintOSX()
                else:
                        print ("Failure to supply an operating system type!\n")
                        sys.exit(2)
		sys.exit(0)	
	elif(fileType == 2):			#if the input file is in PDB format
		if(verbose):
			print ("Launching Chimera\n")
		if(OS == 1):
                        launchConversionWindows(inputFile)
                elif(OS == 2):
                        launchConversionOSX(inputFile)
                else:
                        print ("Failure to supply an operating system type!\n")
                        sys.exit(2)
		if(verbose):
			print ("Launching CURA\n")
		if(OS == 1):
                        launchSliceWindows("")
                elif(OS == 2):
                        launchSliceOSX("")
                else:
                        print ("Failure to supply an operating system type!\n")
                        sys.exit(2)
		if(verbose):
			print ("Launching Chroma\n")
		if(OS == 1):
                        launchPrintWindows()
                elif(OS == 2):
                        launchPrintOSX()
                else:
                        print ("Failure to supply an operating system type!\n")
                        sys.exit(2)
		sys.exit(0)
	else:					#handling cases where fileType value is unknown
		sys.exit(0);

if __name__ == "__main__":
    main()

#getopt from python documentation, needs actual citation
