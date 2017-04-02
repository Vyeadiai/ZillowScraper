import subprocess
from glob import glob
import os
import json

start_dir = "/Users/testtest/scrapyProjects/zillowImages"


def convertImages(imageList):
	for image in imageList:
		subprocess.call("/usr/local/bin/convert " + image + " -gravity center -background black -extent 1024x782 " + image, shell=True)

print " "
print "================================================"
print "Running script: convertImages.py"
print "================================================"
		
		
dirList = glob(start_dir + '/*')

for dir in dirList:	
	dirName = os.path.basename(dir)
	
	#if the video does not exist in directory, resize the images to a uniform dimensions
	if not os.path.isfile(dir + "/" + dirName + ".mp4"):
		print "=>Converting the images in directory: " + dir
		
		#get all the images 
		imageList = glob(dir + "/*.jpg")
		
		if len(imageList) > 0:
			convertImages(imageList)
			print "=>Done."
		else:
			print "=>No Images found in this directory..."
			
		print " "
	else:
		print "=>Skipping conversion of images in this directory: " + dir
		print "=>A video already exists in this directory, no need to resize images..."
		print " "
		