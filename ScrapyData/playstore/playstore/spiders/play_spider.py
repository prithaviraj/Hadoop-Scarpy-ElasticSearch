import scrapy 



class QuotesSpider(scrapy.Spider) :

	name="play"

     

	start_urls = [ 'https://play.google.com/store/apps?hl=en' , ] # main page url

	download_delay = 1.5

	app_count=0

	

	def parse(self , response):

		url = 'https://play.google.com'

		xurl=response.css('div.dropdown-submenu ul li.child-submenu-link-wrapper a.child-submenu-link::attr(href)').extract()

		for url2 in xurl :

			full_url=url+url2  #  categries page url 

			yield scrapy.Request(full_url, callback=self.parse_seemore)

			

	def parse_seemore(self , response): # see more 

		url = 'https://play.google.com'

		xurl=response.css('span a.see-more.play-button.small.id-track-click.apps.id-responsive-see-more::attr(href)').extract()

		for url2 in xurl :

			full_url=url+url2 # see more url 

			yield scrapy.Request(full_url, callback=self.parse_apppage)    

			

	def parse_apppage(self , response):

		url = 'https://play.google.com'

		xurl=response.css('div.details a.title::attr(href)').extract()

		for url2 in xurl :

			full_url=url+url2  # Any particular apps url 

			#print ('\n')
			#print 'App URL :  ',full_url
			#print "App no :",self.app_count

			self.app_count=self.app_count+1

			yield scrapy.Request(full_url, callback=self.parse_details)   # final request end here 	 	

   	

   	global data_clean
   	
   	def data_clean(data,var):
		if var==1 :
			data=data.replace(',','').strip()
			return int(data)	
		elif var==2 :
			data_list=data.split()
			data_float=data_list[1]
			return float(data_float)	
		

	global fetch_data 

	def fetch_data(list1,data_value):

		i=0 #  i for list1 increament 

		for datalist in list1: 

			if datalist==data_value :
				return list1[i+1].strip()
				
			elif (datalist=='Installs' and(data_value=='Installs-minimum' or data_value=='Installs-maximum'))  :
				minmax=data_value.split('-')[1]
				minmaxvalue=list1[i+1].strip().split('-')
				if(minmax=='minimum'):
					return minmaxvalue[0].strip()
				elif(minmax=='maximum'):
					return minmaxvalue[1].strip()
			i=i+1

		else :
				return "None"
            		
	def parse_details(self, response):

           yield {

              'applicationName' : (response.css('div.id-app-title ::text').extract_first()).encode("utf-8") ,
              'publishedBy' : (response.css('div a.document-subtitle.primary span::text').extract_first()).encode("utf-8") ,
              'rating' : data_clean(response.css('div div div.score ::attr(aria-label)').extract_first(),2),
              'downloadBy ' : data_clean((response.css('div span ::attr(aria-label)').extract_first().strip().split(" ")[0]),1),
              'inAppProductsPrice':(fetch_data(response.css('div.meta-info div::text').extract(),'In-app Products')).encode("utf-8"),
			  'urlLink' : response.url ,
			  'availableOn' : ['Android Mobile' , 'Android Device'],
			  'category' : (response.css('div a.document-subtitle.category span::text').extract_first()).encode("utf-8") ,
			  'systemRequirements':['Andorid version  ' + fetch_data(response.css('div.meta-info div::text').extract(),'Requires Android')],
			  
              'version':fetch_data(response.css('div.meta-info div::text').extract(),'Current Version'),
              'updated' : response.css('div.meta-info div::text').extract()[1],
              'installsMinimum':data_clean((fetch_data(response.css('div.meta-info div::text').extract(),'Installs-minimum')),1),
              'installsMaximum':data_clean((fetch_data(response.css('div.meta-info div::text').extract(),'Installs-maximum')),1),

               }


