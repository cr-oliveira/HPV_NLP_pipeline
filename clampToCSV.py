# This program gets a directory containing Clamp output files from the user and
# goes through those files, finding the type and location of the report, the diagnosis code,
# the diagnosis, and the HPV diagnosis

import glob
import os

def main():
	# Create the output file
	outputFile = open("reportDiagnoses.csv", "w")

	# Make a list to contain all file names
	allFileNames = []

	# Make 4 lists, aPap, aBiop, cPap, cBiop
	aPapFileNames = [] 
	aBiopFileNames = [] 
	cPapFileNames = [] 
	cBiopFileNames = [] 
	
	# Get the name of the directory containing Clamp output
	directoryName = input("Please enter the path of the directory containging output from Clamp: ")
	if(directoryName.endswith("/") == True):
		directoryNameGlob = directoryName + "*.txt"
	else:
		directoryName += "/"
		directoryNameGlob = directoryName + "*.txt"

	# Create a list of the file names
	allFiles = glob.glob(directoryNameGlob)
	for file in allFiles:
		allFileNames.append(file)
	#print(allFileNames)

	# Add each file name into the correct list
	for fileName in allFileNames:
		reportType = hpvMarker(fileName)
		location = locationFinder(fileName)
		if(reportType == "Pap" and location == "Cervical"):
			cPapFileNames.append(fileName)
		elif(reportType == "Pap" and location == "Anal"):
			aPapFileNames.append(fileName)
		elif(reportType == "Biopsy" and location == "Cervical"):
			cBiopFileNames.append(fileName)
		elif(reportType == "Biopsy" and location == "Anal"):
			aBiopFileNames.append(fileName)
	#print(cPapFileNames)

	# For each list, run the appropriate diagnosis finder and add the info to the output file
	outputFile.write("Report ID,Report Type,Report Location,Diagnosis Code,Diagnosis,HPV Diagnosis" + "\n\n")

	for fileName in cPapFileNames:
		filePath=os.path.basename(fileName)
		fileID, fileExtension=os.path.splitext(filePath)
		dxNumbers, dxStrings = papDiagnosisFinder(fileName)
		outputFile.write(fileID + ",")
		outputFile.write("Pap Smear" + ",")
		outputFile.write("Cervical" + ",")
		outputFile.write(dxNumbers + ",")
		outputFile.write(dxStrings + ",")
		outputFile.write(HPVDiagnosisFinder(fileName))
		outputFile.write("\n") 

	for fileName in aPapFileNames:
		filePath=os.path.basename(fileName)
		fileID, fileExtension=os.path.splitext(filePath)
		dxNumbers, dxStrings = papDiagnosisFinder(fileName)
		outputFile.write(fileID + ",")
		outputFile.write("Pap Smear" + ",")
		outputFile.write("Anal" + ",")
		outputFile.write(dxNumbers + ",")
		outputFile.write(dxStrings + ",")
		outputFile.write(HPVDiagnosisFinder(fileName))
		outputFile.write("\n") 

	for fileName in cBiopFileNames:
		filePath=os.path.basename(fileName)
		fileID, fileExtension=os.path.splitext(filePath)
		outputFile.write(fileID + ",")
		outputFile.write("Biopsy" + ",")
		outputFile.write("Cervical" + ",")
		outputFile.write(str(bxDiagnosisFinder(fileName)) + ",")
		outputFile.write(str(bxNumberToText(bxDiagnosisFinder(fileName))) + ",")
		outputFile.write(HPVDiagnosisFinder(fileName))
		outputFile.write("\n") 

	for fileName in aBiopFileNames:
		filePath=os.path.basename(fileName)
		fileID, fileExtension=os.path.splitext(filePath)
		outputFile.write(fileID + ",")
		outputFile.write("Biopsy" + ",")
		outputFile.write("Anal" + ",")
		outputFile.write(str(bxDiagnosisFinder(fileName)) + ",")
		outputFile.write(str(bxNumberToText(bxDiagnosisFinder(fileName))) + ",")
		outputFile.write(HPVDiagnosisFinder(fileName))
		outputFile.write("\n") 



#################################################################################################
# Return Pap if the report is a pap smear, return Biopsy if the report is a biopsy
#################################################################################################
def hpvMarker(fileName):
	inputFile=open(fileName, "r")
	lines = inputFile.readlines()
	for line in lines:
		lineElements=line.split("\t")
		### semanticType is the annotation type
		semanticType=lineElements[2]
		if (semanticType == "PapMarkerHistory"):
			return("Biopsy")
		if (semanticType == "PapMarker"):
			return("Pap")

	return("Biopsy")



#################################################################################################
# Return Cervical if the report is for cervical, return Anal if the report is for anal
#################################################################################################
def locationFinder(fileName):
	inputFile=open(fileName, "r")
	lines = inputFile.readlines()
	for line in lines:
		lineElements=line.split("\t")
		### semanticType is the annotation type
		semanticType=lineElements[2]
		if (semanticType == "AnalMarker"):
			return("Anal")

	return("Cervical") 



#################################################################################################
# Return a list of all diagnoses found in the pap smear
#################################################################################################
def papDiagnosisFinder(fileName):
	inputFile=open(fileName, "r")
	### Each line is an annotation
	lines=inputFile.readlines()
	finalDiagnosesList=[]
	for line in lines:
		lineElements=line.split("\t")
		### semanticType is the annotation type
		semanticType=lineElements[2]
		for i in range(len(semanticType)):
			### If semanticType starts with 1.X, it is a diagnosis
			if (semanticType[i:i+2]=="Dx"):
				### Get the diagnosis and save it to finalDiagnosis
				diagnosisName=semanticType[i+2:len(semanticType)]
				### Get the number from the name
				diagnosisNumber = -1
				if(diagnosisName == "Benign"):
					diagnosisNumber = 0
				elif(diagnosisName == "NIEL"):
					diagnosisNumber = 1
				elif(diagnosisName == "ASCUS"):
					diagnosisNumber = 2
				elif(diagnosisName == "ASCH"):
					diagnosisNumber = 3
				elif(diagnosisName == "LSIL"):
					diagnosisNumber = 4
				elif(diagnosisName == "HSIL"):
					diagnosisNumber = 5
				elif(diagnosisName == "SCC"):
					diagnosisNumber = 6
				elif(diagnosisName == "IN1"):
					diagnosisNumber = 7
				elif(diagnosisName == "IN2"):
					diagnosisNumber = 8
				elif(diagnosisName == "IN23"):
					diagnosisNumber = 9
				elif(diagnosisName == "IN3"):
					diagnosisNumber = 11
				elif(diagnosisName == "AIS"):
					diagnosisNumber = 12
				elif(diagnosisName == "AGC"):
					diagnosisNumber = 15
				elif(diagnosisName == "AEC"):
					diagnosisNumber = 16
				elif(diagnosisName == "UNCAT"):
					diagnosisNumber = 99
				#print("Diagnosis = " + str(diagnosisName) + " : " + str(diagnosisNumber))
				finalDiagnosesList.append(diagnosisNumber)
	#print("finalDiagnosis = " + str(finalDiagnosis))
	if(satisfiabilityFinder(fileName)==False):
		finalDiagnosesList = [14]
	dxStringList = papNumberToText(finalDiagnosesList)
	finalDiagnosesString = ""
	for diagnosis in finalDiagnosesList:
		finalDiagnosesString += str(diagnosis) + " ; "
	finalDiagnosesString = finalDiagnosesString[0:len(finalDiagnosesString) - 2]
	return(finalDiagnosesString, dxStringList)



#################################################################################################
# Return the highest ranking diagnosis
#################################################################################################
def bxDiagnosisFinder(fileName):
	inputFile=open(fileName, "r")
	### Each line is an annotation
	lines=inputFile.readlines()
	finalDiagnosis=[]
	for line in lines:
		lineElements=line.split("\t")
		### semanticType is the annotation type
		semanticType=lineElements[2]
		for i in range(len(semanticType)):
			### If semanticType starts with 1.X, it is a diagnosis
			if (semanticType[i:i+2]=="Dx"):
				### Get the diagnosis and save it to finalDiagnosis
				diagnosisName=semanticType[i+2:len(semanticType)]
				### Get the number from the name
				diagnosisNumber = -1
				if(diagnosisName == "Benign"):
					diagnosisNumber = 0
				elif(diagnosisName == "NIEL"):
					diagnosisNumber = 1
				elif(diagnosisName == "ASCUS"):
					diagnosisNumber = 2
				elif(diagnosisName == "ASCH"):
					diagnosisNumber = 3
				elif(diagnosisName == "LSIL"):
					diagnosisNumber = 4
				elif(diagnosisName == "HSIL"):
					diagnosisNumber = 5
				elif(diagnosisName == "SCC"):
					diagnosisNumber = 6
				elif(diagnosisName == "IN1"):
					diagnosisNumber = 7
				elif(diagnosisName == "IN2"):
					diagnosisNumber = 8
				elif(diagnosisName == "IN23"):
					diagnosisNumber = 9
				elif(diagnosisName == "IN3"):
					diagnosisNumber = 11
				elif(diagnosisName == "AIS"):
					diagnosisNumber = 12
				elif(diagnosisName == "AGC"):
					diagnosisNumber = 15
				elif(diagnosisName == "AEC"):
					diagnosisNumber = 16
				elif(diagnosisName == "UNCAT"):
					diagnosisNumber = 99
				finalDiagnosis.append(diagnosisName)
	### Find the highest ranking diagnosis 
	for diagnosis in finalDiagnosis:
		if(diagnosis=="AIS"):
			return(12)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="SCC"):
			return(6)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="IN3"):
			return(11)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="IN23"):
			return(9)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="IN2"):
			return(8)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="IN1"):
			return(7)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="HSIL"):
			return(5)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="LSIL"):
			return(4)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="ASCH"):
			return(3)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="ASCUS"):
			return(2)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="NIEL"):
			return(1)
	for diagnosis in finalDiagnosis:
		if(diagnosis=="Benign"):
			return(0)
	return 0



#################################################################################################
# Return Positive for a positive HPV diagnosis, Negative for a negative HPV diagnosis,
# HPV Mentioned if the word HPV is in the report but the diagnosis couldn't be found
# HPV Not Found if the word HPV is not in the report 
#################################################################################################
def HPVDiagnosisFinder(fileName):
	inputFile=open(fileName, "r")
	### Each line is an annotation
	lines=inputFile.readlines()
	diagnosesFound=0
	finalDiagnosis=[]
	for line in lines:
		lineElements=line.split("\t")
		### semanticType is the annotation type
		semanticType=lineElements[2]
			### If semanticType starts with 1.X, it is a diagnosis
		if (semanticType=="HPVPositive" or semanticType=="HPVNegative"):
			diagnosisName=semanticType[3:len(semanticType)]
			return(diagnosisName)
	for line in lines:
		lineElements=line.split("\t")
		### semanticType is the annotation type
		semanticType=lineElements[2]
		if (semanticType=="HPV"):
			return("HPV Mentioned")
	return("HPV Not Found")



#################################################################################################
# Return True if the report is satisfiable, return False if not
#################################################################################################
def satisfiabilityFinder(fileName):
	inputFile=open(fileName, "r")
	lines=inputFile.readlines()
	diagnosesFound=0
	for line in lines:
		#print(line)
		lineElements=line.split("\t")
		#for element in lineElements:
			#print(element)
		semanticType=lineElements[2]
		if(semanticType=="UNSAT"):
			#print("Unsatisfiable")
			return False
	#print("Satisfiable")
	return True



#################################################################################################
# Take a list of dx codes and return the text diagnosis 
#################################################################################################
def papNumberToText(dxList):
	dxStringList = []
	dxStrings = ""
	for dx in dxList:
		if(dx == 0):
			dxStringList.append("Benign")
		elif(dx == 1):
			dxStringList.append("NIEL")
		elif(dx == 2):
			dxStringList.append("ASCUS")
		elif(dx == 3):
			dxStringList.append("ASCH")
		elif(dx == 4):
			dxStringList.append("LSIL")
		elif(dx == 5):
			dxStringList.append("HSIL")
		elif(dx == 6):
			dxStringList.append("SCC")
		elif(dx == 7):
			dxStringList.append("CIN 1")
		elif(dx == 8):
			dxStringList.append("CIN 2")
		elif(dx == 9):
			dxStringList.append("CIN 2/3")
		elif(dx == 11):
			dxStringList.append("CIN 3")
		elif(dx == 12):
			dxStringList.append("AIS")
		elif(dx == 15):
			dxStringList.append("AGC")
		elif(dx == 16):
			dxStringList.append("AEC")
		elif(dx == 14):
			dxStringList.append("Unsatisfactory")
		elif(dx == -1):
			dxStringList.append("Not Found")
		elif(dx == 99):
			dxStringList.append("Uncategorizable")
	for dx in dxStringList:
		dxStrings += dx + " ; "
	dxStrings = dxStrings[0:len(dxStrings) - 2]
	return dxStrings



#################################################################################################
# Take a dx code and return the text diagnsois
#################################################################################################
def bxNumberToText(dx):
	if(dx == 0):
		dxString = "Benign"
	elif(dx == 1):
		dxString = "NIEL"
	elif(dx == 2):
		dxString = "ASCUS"
	elif(dx == 3):
		dxString = "ASCH"
	elif(dx == 4):
		dxString = "LSIL"
	elif(dx == 5):
		dxString = "HSIL"
	elif(dx == 6):
		dxString = "SCC"
	elif(dx == 7):
		dxString = "CIN 1"
	elif(dx == 8):
		dxString = "CIN 2"
	elif(dx == 9):
		dxString = "CIN 2/3"
	elif(dx == 11):
		dxString = "CIN 3"
	elif(dx == 12):
		dxString = "AIS"
	elif(dx == 15):
		dxString = "AGC"
	elif(dx == 16):
		dxString = "AEC"
	elif(dx == 14):
		dxString = "Unsatisfactory"
	elif(dx == -1):
		dxString = "Not Found"
	elif(dx == 99):
		dxString = "Uncategorizable"

	return dxString


main()
