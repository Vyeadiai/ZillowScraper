from scrapy.selector import Selector
from timecoverspider.items import MagazineCover
import datetime
import scrapy
import time
import json
import os
import errno


class CoverSpider(scrapy.Spider):	
	
	name = "pyimagesearch-cover-spider"
	start_urls = ["https://www.zillow.com/homes/"]
	
	
	def parse(self, response):
		homeListItem = response.css('li article div + a::attr(href)').extract()
		
		
		##################this is to get ALL of the homes in zillow, parse each home on the first page, then click Next, and do it again--########
		###request each found on home page
 		for home in homeListItem:
 			yield scrapy.Request( "http://www.zillow.com" + home, self.parse_Each_Home_Page)
 		
 		
 		#Select the next link and scrape the next page
 		nextHref = response.css('li.zsg-pagination-next a::attr(href)').extract_first()
 		if nextHref is not None:
 			yield scrapy.Request( "http://www.zillow.com" + nextHref, self.parse)
		#######################################################################
		
		

		##################this is to test only the first home found--########
		#yield scrapy.Request( "http://www.zillow.com" + homeListItem[1], self.parse_Each_Home_Page)
		#####################################################################


		##################this is to test only the first page found, which currently has about 25 homes--########
		#for home in homeListItem:
		#	yield scrapy.Request( "http://www.zillow.com" + home, self.parse_Each_Home_Page)
		#######################################################################################################
		
		
		
	def parse_Each_Home_Page(self, response):
		###########Get the data from each home-beds ,baths, price etc...###############
		addressFirstRow = response.css('header.zsg-content-header.addr h1::text').extract_first()
		addressSecondRow = response.css('header.zsg-content-header.addr h1 span::text').extract_first()
		homeSalePrice = response.css('div.main-row.home-summary-row span::text').extract_first()
		numBeds = ""
		numBaths = ""
		sqftOfHome = ""
		homeEstimatedMortgage = ""
		
		homeDetails = response.css('header.zsg-content-header.addr h3 span::text').extract()
		for homeDetail in homeDetails:
			if "beds" in homeDetail:
				numBeds = homeDetail
			if "baths" in homeDetail:
				numBaths = homeDetail
			if "sqft" in homeDetail:
				sqftOfHome = homeDetail		
				
		
		listOfSpans = response.css('span.loan-calculator-estimate span::text').extract()
		for spanText in listOfSpans:
			if "$" in spanText:
				homeEstimatedMortgage = spanText
		###########################################################################

		# This is the root folder where all the other home folders will be created
		rootDirectoryZillowImages = "/Users/testtest/scrapyProjects/zillowImages"
		
		if addressFirstRow is None:
			addressFirstRow = "Undisclosed Address" + "{:%B_%d_%Y_%S}".format(datetime.datetime.now())
		
		if addressSecondRow is None:
			addressSecondRow = ""
			
		if homeSalePrice is None:
			homeSalePrice = ""
		
		if homeEstimatedMortgage is None:
			homeEstimatedMortgage = ""
		
		#create the directory name for this home based on its address
		#---stripping all non alpha-numeric and white spaces
		thisHomesDirectoryName = rootDirectoryZillowImages + "/" + \
								"".join(ch for ch in addressFirstRow if ch.isalnum()) + \
								"".join(ch for ch in addressSecondRow if ch.isalnum())
		
		#put this data in a dictionary to be dumped into a JSON file
		jsonDict = {  'homeEstimatedMortgage' : homeEstimatedMortgage,
					  'homeSalePrice' : homeSalePrice,
					  'numBeds' : numBeds,
					  'numBaths' : numBaths,
					  'sqftOfHome' : sqftOfHome,
					  'addressFirstRow' : addressFirstRow,
					  'addressSecondRow' : addressSecondRow }
		
		
		#create the JSON file, put it in the new home folder 
		self.make_sure_path_exists(thisHomesDirectoryName)
		self.convert_To_JSON(jsonDict, thisHomesDirectoryName)
		
		
		#Download all the home images to thisHomesDirectoryName folder
		listItemsImages = response.css('ul.photo-wall-content li.sm-tile div img::attr(href)').extract()		
		for href in listItemsImages:
			hrefModified = href
			if "/p_c" in href:
				hrefModified = href.replace("/p_c/", "/p_f/")
			elif "/p_h" in href:
				hrefModified = href.replace("/p_h/", "/p_f/")
			
			yield MagazineCover(session_path=thisHomesDirectoryName, image_urls=[hrefModified])
			
								

	#save the home details to JSON file					
	def convert_To_JSON(self, jsonDict, thisHomesDirectoryName):
		with open(thisHomesDirectoryName + '/homeData.json', 'w') as outfile:
			json.dump(jsonDict, outfile)
			
	
	#Create the new folder that will hold the images and the JSON file, if it exists ignore the exception		
	def make_sure_path_exists(self, path):
		try:
			os.makedirs(path)
		except OSError as exception:
			if exception.errno != errno.EEXIST:
				raise
