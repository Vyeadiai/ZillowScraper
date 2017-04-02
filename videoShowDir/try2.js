var fs=require('fs');
var path = require('path');
var videoshow = require('videoshow');

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

// videoshow(images, videoOptions)
//   .save('video1.mp4')
//   .on('error', function () {})
//   .on('end', function () {})
  
  
for(var dirName in dirList) {
	if(fs.lstatSync(start_dir + "/" + dirList[dirName]).isDirectory()) {
    	var imageList = fs.readdirSync(start_dir + "/" + dirList[dirName]);
    
    	//If video does not exist---add a check for this later
    	if(true) {
    		var arrayZillowImages = [];
    		for(var image in imageList) {
   				if(path.extname(start_dir + "/" + dirList[dirName] + "/" + imageList[image]) === ".jpg") {
       				arrayZillowImages.push(start_dir + "/" + dirList[dirName] + "/" + imageList[image]);
   				}
   			}
   			videoshow(arrayZillowImages, videoOptions)
			  .save(start_dir + "/" + dirList[dirName] + "/" + dirList[dirName] + ".mp4")
			  .on('error', function () {})
			  .on('end', function () {})
   			
   			//videoshow(arrayZillowImages, videoOptions);
   			//console.log("---!");
   			//console.log(arrayZillowImages);
   			//console.log("---!");
   		}
    }    
}


//console.log(dirList[dirName]);

// 

// 
// var images = [
// 
// ]
// 

// 
// videoshow(images, videoOptions)
//   .audio('song.mp3')
//   .save('video.mp4')
//   .on('start', function (command) {
//     console.log('ffmpeg process started:', command)
//   })
//   .on('error', function (err, stdout, stderr) {
//     console.error('Error:', err)
//     console.error('ffmpeg stderr:', stderr)
//   })
//   .on('end', function (output) {
//     console.error('Video created in:', output)
//   })