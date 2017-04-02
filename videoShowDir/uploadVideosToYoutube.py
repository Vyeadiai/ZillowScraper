import sys
import subprocess
import os.path
import json
from os.path import basename


def GetVideoTitle(jsonData):
	
	videoTitle = ""
	
	if ( str(jsonData['addressFirstRow']) != ""):
		videoTitle +=  str(jsonData['addressFirstRow'])
	
	if ( str(jsonData['addressSecondRow']) != ""):
		videoTitle +=  " " + str(jsonData['addressSecondRow'])
	
	return videoTitle


def GetVideoDescription(jsonData):
	
	videoDescription = ""
	
	if ( str(jsonData['addressFirstRow']) != ""):
		videoDescription +=  str(jsonData['addressFirstRow']) + '\n'
		
	if ( str(jsonData['addressSecondRow']) != ""):
		videoDescription +=  " " + str(jsonData['addressSecondRow']) + '\n'
		
	if ( str(jsonData['sqftOfHome']) != ""):
		videoDescription +=  "Sqare footage: " + str(jsonData['sqftOfHome']) + '\n'
		
	if ( str(jsonData['numBeds']) != ""):
		videoDescription +=  "Number of Bedrooms: " + str(jsonData['numBeds']) + '\n'
		
	if ( str(jsonData['numBaths']) != ""):
		videoDescription +=  "Number of Bathrooms: " + str(jsonData['numBaths']) + '\n'
		
	if ( str(jsonData['homeSalePrice']) != ""):
		homeSalePrice = str(jsonData['homeSalePrice'])
		modifiedStr = homeSalePrice.replace("$", "\$")
		videoDescription +=  "Sale Price: " + modifiedStr + '\n'
	
	if ( str(jsonData['homeEstimatedMortgage']) != ""):
		homeEstimatedMortgage = str(jsonData['homeEstimatedMortgage'])
		modifiedStr = homeEstimatedMortgage.replace("$", "\$")
		videoDescription +=  "Estimated Mortgage: " + modifiedStr + '\n'
		
	#Add link to property here
	
	return videoDescription
	
	
	
	

def UploadVideoToYoutube(videoFileName):
	
	fileNameWoutExtension = basename(videoFileName)
	videoTitle = os.path.splitext(fileNameWoutExtension)[0]
	videoDescription = "Home For Sale Slideshow"
	
	
	jsonFileExists = os.path.exists(os.path.dirname(videoFileName) + "/homeData.json" )
	
	if jsonFileExists:
		with open(os.path.dirname(videoFileName) + "/homeData.json" , 'r') as f:
			jsonData = json.load(f)
			
			if jsonData is not None:
				
				modifiedVideoTitle = GetVideoTitle(jsonData)
				if modifiedVideoTitle != "":
					videoTitle = modifiedVideoTitle
				
				modifiedVideoDescription = GetVideoDescription(jsonData)
				if modifiedVideoDescription != "":
					videoDescription = modifiedVideoDescription
		
	#print videoTitle
	#print "----------"
	#print videoDescription
	
	subprocess.call("python upload_video.py --file=\"" + videoFileName + "\" --title=\"" + videoTitle + "\" --description=\"" + videoDescription + "\" --keywords=\"home,selling, home for sale, buy home, homes for sale, virtual tour, virtual home tour\" --category=\"22\" --privacyStatus=\"public\" --noauth_local_webserver", shell=True)



print " "
print "================================================"
print "Running script: uploadVideosToYoutube.py"
print "================================================"
print " "

uploadedVideosFileName = sys.argv[1]

print "=>Checking this file for recently uploaded videos: " + uploadedVideosFileName
print " "

with open(uploadedVideosFileName,'r') as f:
	for videoFileName in f:
		videoFileName = videoFileName.rstrip()
		if not videoFileName: 
			continue
		else:
			print "=>Uploading video to youtube: " + videoFileName
			print " "
			UploadVideoToYoutube(videoFileName)