#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, time  
import argparse       				#arguments parser
from more_itertools import sliced

__doc__="""
ChipMunks, a Chip-seq framework based on the most frequently used tools and workflows.
@requires: U{python 2.7<https://www.python.org/downloads/>} (tested with 2.7.6)
@requires: ...
@requires: ...
@requires: ...
"""

def get_parser():
	"""
	Arguments parser
	@return: arguments list
	@rtype: parser object
	"""

	parser = argparse.ArgumentParser(description=' ChipMunks, a Chip-seq framework based on the most frequently used tools and workflows.')

	parser.add_argument('--auto', action="store", dest='auto',
						type=str, required='--quick' in sys.argv, help='Run framework in default mode')


	parser.add_argument('--manual', action="store", dest='manual',
						type=str, required='--quick' in sys.argv, help='Choose which tools to use for each step of the workflow : \n \
						TRIMMING:\n \
						Trm: Trimmomatic | xxx: Tool \n \
						READS QUALITY CHECKING: \n \
						Fqc: FastQC | Qsr: Quasr \n \
						ALIGNMENT: \n \
						Bbm: BBMap | xxx: Tool \n \
						PEAK CALLING:\n \
						xxx: Tool | xxx: Tool | Ml : Machine learning approach\n\
						ANNOTATION/VISUALISATION:\n\
						Ucs: UCSC genome Browser | xxx : Tool\n\
						FUNCTIONAL ENRICHMENT ANALYSIS:\n\
						xxx: Tool | xxx:Tool')

	parser.add_argument('--advanced', action="store", dest='fast',
						type=str, required='--quick' in sys.argv, help='--manual mode with custom seetings for each tools \n \
						usable with --man and --pro mode.')

	parser.add_argument('--quick', action="store", dest='fast',
						type=str, required=False,
						help='Stop workflow at peak calling step \n \
						usable with all execution modes (i.e --auto , --manual, --advanced')

	parser.add_argument('-breathCov', action="store", dest='breathCov',
						type=int, required=False ,default=95, help='breath coverage threashold (default: 95 percent)')

	parser.add_argument('-deepCov', action="store", dest='deepCov',
						type=int, required=False, default=30, help='deep coverage threashold (default: 30)')

	parser.add_argument('-phred', action="store", dest='phred',
						type=int, required=False, default=30, help='phred score threashold(default: 30)')

	parser.add_argument('-T', action="store", dest='threads', 
						type=int, required=False, default=1, help='maximum number of threads assignable to ChipMunks (default: 1 thread)')

	parser.add_argument('-m', action="store", dest='maxMemory', 
						type=int, required=False, default=4000, help='RAM threashold (Mb) for ChipMunks (default : 4000Mb)')

	parser.add_argument('-w', action="store", dest='workdir', 
						type=str, required=False, default='.', help='working directory (default: current working directory)')

	parser.add_argument('-prefix', action="store", dest='prefix', 
						type=str, default=time.strftime("%d/%m/%Y") + '_' + time.strftime("%H:%M:%S"), help='results path prefix (default : DD/MM/YYYY_h/m/s')


	return parser



def generateCommand(commandShortcut):
	"""
	Generates a string command line from a string shorcut
	@return: command line string
	@rtype: String
	"""
	
	#Corresp dictionnary in order to build commands (for --manual and --adavanced mode) from string shorcuts
	CommandsCorresp = {
		"Trm":"Trimmomatic"+ "+parameters...etc" ,
		"Fqc":"FastQC",
		"Qsr":"Quasr",
		"Bbm":"BBMap",
		"Ml":"...",
		"Usc":"UCSC"
	}

	#Split the shortcut string in substrings of length 3
	CommandsList=list(sliced(commandShortcut, 3))	

	#Converted command line
	cmd=[]

	for command in CommandsList:
		if command in CommandsCorresp:
			cmd.append(CommandsCorresp[command])

	return cmd



def main():	

	##########################################
	#			Initialisation				 #
	##########################################
	
	# Processing time counter
	t0 = time.time()
	
	# Get arguments 
	parser=get_parser()
	
	# Print parser.help if no arguments
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
	
	Arguments=parser.parse_args()	

	# Go to working directory gived by Arguments.workdir
	if(Arguments.workdir != '.'):
		os.chdir(Arguments.workdir)	

	# GLOBAL VARIABLES
	PNAME = Arguments.prefix # Process name
	CWD = os.getcwd() #Current working directory FULL path	
	LOG_FILE = CWD + "/" + PNAME + ".log"
	REPORT_FILE = PNAME + "_report.txt"

	##########################################
	#			Automatic mode				 #
	##########################################
	if(Arguments.auto and not Arguments.manual ):
		#process default mode
		print "auto mode"

	elif(Arguments.manual and not Arguments.auto ):
		print "man mode"
		print generateCommand("TrmFqc")

if __name__ == "__main__":
	main()