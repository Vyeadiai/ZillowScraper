var videoshow = require('videoshow');

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

var images = [
  'output.jpg',
  'output2.jpg'
]


videoshow(images,videoOptions)
  .save('video1.mp4')
  .on('error', function () {})
  .on('end', function () {})
  
//   videoshow([{
//     path: '1.jpg',
//     caption: 'Hello world as video subtitle'
//   }, {
//     path: '2.jpg',
//     caption: 'This is a sample subtitle',
//     loop: 10 // long caption
//   }])
//   .save('video1.mp4')
//   .on('error', function () {})
//   .on('end', function () {})