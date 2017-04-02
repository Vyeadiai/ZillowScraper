
source /Users/testtest/scrapyProjects/timecoverspider/timecoverspider/venv/bin/activate

mkdir /Users/testtest/scrapyProjects/timecoverspider/timecoverspider/UploadedVideos

file_name=uploadedVideos
current_time=$(date "+%d_%m_%Y")
new_file_name=/Users/testtest/scrapyProjects/timecoverspider/timecoverspider/UploadedVideos/$file_name.$current_time.txt

touch $new_file_name

cd /Users/testtest/scrapyProjects/timecoverspider/timecoverspider

scrapy runspider /Users/testtest/scrapyProjects/timecoverspider/timecoverspider/spiders/coverspider.py

python /Users/testtest/scrapyProjects/videoShowDir/convertImages.py

#cd /Users/testtest/scrapyProjects/videoShowDir/

/usr/local/bin/node /Users/testtest/scrapyProjects/videoShowDir/createZillowVideo.js $new_file_name

python /Users/testtest/scrapyProjects/videoShowDir/uploadVideosToYoutube.py $new_file_name



