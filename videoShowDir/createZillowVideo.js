var fs=require('fs');
var path = require('path');
var videoshow = require('videoshow');
var os = require('os');

var start_dir = "/Users/testtest/scrapyProjects/zillowImages";
var dirList = fs.readdirSync(start_dir);


var videoOptions = {
  fps: 25,
  loop: 5, // seconds
  transition: true,
  transitionDuration: 1, // seconds
  videoBitrate: 1024,
  videoCodec: 'libx264',
  size: '1024x782',
  scale: '1024x782',
  audioBitrate: '128k',
  audioChannels: 2,
  format: 'mp4',
  pixelFormat: 'yuv420p'
}

  

//loop through the images and add text/captions to the array 
function AddCaptionsToImages(arrayZillowImages, jsonObj) {

	var modifiedArrayZillowImages = [];
	var homeAddress = "";
	var homeStats = "";
	var homePrice = "";
	
	//get the address, must have at least first line of address
	if(jsonObj.addressFirstRow.length > 0) {
			homeAddress = jsonObj.addressFirstRow;
		if(jsonObj.addressSecondRow.length > 0) {
			homeAddress += " " + jsonObj.addressSecondRow;
		}
	}
	
	//get the home stats like baths, beds
	if(jsonObj.numBeds.length > 0) {
		homeStats = /*"Bedrooms: " + */jsonObj.numBeds;
	}
	if(jsonObj.numBaths.length > 0) {
		homeStats += /*"/Bathrooms: " + */ " " + jsonObj.numBaths;
	}
	if(jsonObj.sqftOfHome.length > 0) {
		homeStats += /*"/Square Footage: " + */ " " + jsonObj.sqftOfHome;
	}
		
	
	//get the price info
	if(jsonObj.homeSalePrice.length > 0) {
		homePrice = "Price: " + jsonObj.homeSalePrice;
	}
	if(jsonObj.homeEstimatedMortgage.length > 0) {
		homePrice += " Estimated Mortgage: " + jsonObj.homeEstimatedMortgage;
	}
	
	
	//check how many stats we have
	var captionList = [];
	
	if( homeAddress != "")
		captionList.push(homeAddress);
	if( homeStats != "" )
		captionList.push(homeStats);
	if( homePrice != "" )
		captionList.push(homePrice);
		
		
	//if we have any captions to display, modify the image collection 
	if( captionList.length > 0 ) {
		
		var i = 0;
		var modifiedArrayZillowImages = [];
		for( var imagePath in arrayZillowImages)
		{
		 	modifiedArrayZillowImages.push({
    			path:  arrayZillowImages[imagePath],
    			caption: captionList[i]    			
  			});
  					
  			i++;
			
			//loop through the captions, so if there are 3 captions, every three images in the video,
			// the captions will repeat
			if( i > (captionList.length - 1) )
				i = 0;
		}
	}
	else {
		modifiedArrayZillowImages = arrayZillowImages;
	}
		
	return modifiedArrayZillowImages;	
}
		
  
function GetHomeDataFromJSON(zillowImagesPath, arrayZillowImages ) {
	
	var jsonFilePath = zillowImagesPath + "homeData.json";
	
	var modifiedArrayZillowImages = null;
	
	//if JSON file exists get the data and add it to the captions for each image
	if(fs.statSync(jsonFilePath)) {
		console.log(' ');    	
    	console.log('=>Found JSON file in directory: ' + jsonFilePath);    	
        var jsonObj = JSON.parse(fs.readFileSync(jsonFilePath, 'utf8'));
        	
        modifiedArrayZillowImages = AddCaptionsToImages(arrayZillowImages, jsonObj);        	
    }
    else {
        console.log('=>JSON file not found in : ' + jsonFilePath);
    }

	
	return modifiedArrayZillowImages;

}

console.log(' ');
console.log('================================================');
console.log('Running script: createZillowVideo.js');
console.log('================================================');


var uploadedVideosFileName = process.argv[2];


for(var dirName in dirList) {
	if(fs.lstatSync(start_dir + "/" + dirList[dirName]).isDirectory()) {
    	var imageList = fs.readdirSync(start_dir + "/" + dirList[dirName]);
    	
	    	if(! fs.existsSync(start_dir + "/" + dirList[dirName] + "/" + dirList[dirName] + ".mp4")) {
    			var arrayZillowImages = [];
    			for(var image in imageList) {    				
   					if(path.extname(start_dir + "/" + dirList[dirName] + "/" + imageList[image]) === ".jpg") {
       					arrayZillowImages.push(start_dir + "/" + dirList[dirName] + "/" + imageList[image]);
   					}
   				}
   				
   				if( arrayZillowImages.length > 0 ) {
   					console.log('=>Found images images in directory: ' + start_dir + "/" + dirList[dirName]);
   					console.log('=>Modifying the images, adding JSON data onto the images...');
   					console.log(' ');
   				}
   				else {
   					console.log('=>No images found in directory: ' + start_dir + "/" + dirList[dirName]);
					console.log('=>Unable to create video...');
   					console.log(' ');
   					continue;
   				}
   				
   				var modifiedArrayZillowImages = GetHomeDataFromJSON(start_dir + "/" + dirList[dirName] + "/", arrayZillowImages);
   			
   			
   				if(modifiedArrayZillowImages != null) {
   					arrayZillowImages = modifiedArrayZillowImages;
   					console.log('=>Images were modified with JSON data');
   				}
   				else
   				{
   					console.log('=>Images NOT modified, no JSON data found...');
   				}
   			  			
   			   console.log('=>Creating video...');
   			      			   
   				videoshow(arrayZillowImages, videoOptions)
   					.audio("/Users/testtest/scrapyProjects/timecoverspider/timecoverspider/Water_Lily.mp3")
 			  		.save(start_dir + "/" + dirList[dirName] + "/" + dirList[dirName] + ".mp4")
 			  		.on('error', function (err) {
 			  			console.log('=>Error creating video:');
 			  			console.log(start_dir + "/" + dirList[dirName] + "/" + dirList[dirName] + ".mp4");
 			  			console.log('Error: ');
 			  			console.log(err);
 			  			
 			  		}) 			  		
 			  		.on('end', function (output) {
 			  			var videoFileName = output;
 			  		
 			  			console.log('=>Successfully created video:');
 			  			console.log(videoFileName);
 			  			console.log(" ");
 			  			
 			  			fs.appendFile(uploadedVideosFileName, videoFileName + os.EOL, function(err) {
    						if(err) {
        						return console.log(err);
    						}

    					//console.log("The file name was added to");
						});				 
 			  		})
   			}   			
   			else {
   		 		console.log(' ');
	  			console.log('=>The video below already exists, skipping this directory...');  
	  			console.log(start_dir + "/" + dirList[dirName] + "/" + dirList[dirName] + ".mp4"); 	
	  			console.log(' ');	
   			}    
	}
}
