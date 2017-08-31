# -*- coding: utf-8 -*-
import scrapy
import functools
import re
import json
import functools
from bs4 import BeautifulSoup
import csv 
import time 
from utoorides.items import UtoorideItem
from datetime import datetime
list1=[]
index1=[]

class Easy(scrapy.Spider):
      name="utoorides"
      start_urls=["http://utoorides.com/ratecard.html",]
      ii=0
      def parse(self,response):
        soup = BeautifulSoup(response.body, "html.parser")
        a=soup.find_all("div",{"class":"rate-detail-block"})
        new_list=[a[0],a[3],a[6]]
        cites=['Chennai','Hyderabad','Bangalore']
        list1=['COMPACT', 'SEDAN', 'SUV']
        phones=[' 044-46467676','080-46464747','040-46468686']
        ttt=0
        for data in new_list :
            city=cites[ttt]
            phone=phones[ttt]
            ttt=ttt+1
            final_data=data.find_all("tr")  #   service type 
            type1=final_data[1].text.split('\n')
            type1= filter(None,type1)
        	#print type1
            #print type1 # service type
            #print filter(None,final_data[2].text.split('\n')) #  base  fare
            base_fare=filter(None,final_data[2].text.split('\n'))
            #print filter(None,final_data[3].text.split('\n')) #  ride time fare
            ride_fare=filter(None,final_data[3].text.split('\n'))
            #print filter(None,final_data[4].text.split('\n')) #  distance fare
            dic_fare=filter(None,final_data[4].text.split('\n'))

            for i in range(len(type1)) :

                  item=UtoorideItem()                
                  item["url"]=response.url
                  item["website"]="http://utoorides.com/index.html"
                  item["geonameid"]=""
                  item["company"]="Utoorides"
                  item["logo"]="http://utoorides.com/images/logo.png"
                  item["country"]="India"
                  item["city"]=city
                  hh=''
                  mm='' 
                  currency='INR'
                  serv=type1[i]
                  service_format={"serviceName":serv,"serviceLogo":''}
                  item["services"]=service_format

                  #print 'kkk'
                  #print type1[i]
                  #print base_fare[i+1].encode("utf-8").replace('*','').strip().replace('₹','')
                  #print ride_fare[i+1].encode("utf-8").replace('*','').strip().replace('₹','')
                  #print dic_fare[i+1].encode("utf-8").replace('*','').strip().replace('₹','')

                  Base_fare=float(base_fare[i+1].encode("utf-8").replace('*','').strip().replace('₹',''))  # base  fare
                  #print   Base_fare                
                  Ride_fare=float(ride_fare[i+1].encode("utf-8").replace('*','').strip().replace('₹',''))
                  #print Ride_fare
                  Dic_fare=float(dic_fare[i+1].encode("utf-8").replace('*','').strip().replace('₹',''))
                  #print  Dic_fare

                  priceAfterbaseFare=[]
                  priceAfterbaseFare.append({"distance":float(1),"amount":Dic_fare,"currency":currency,"unit":'Km'})
                  before_price='' # Fare/km before Threshold (₹)  new new 
                  fare_dic=''                  
                  price_format={"timeBasedPricing":[{"startTime":{"hh":'',"mm":''},"endTime":{"hh":'',"mm":''},"baseFare":{"currency":currency,"amount":Base_fare,"distance":'',"unit":" "},"waitingfare":{"currency":'',"amount":'',"unit":"",'time':1},"unitPricing":[{"currency":'',"amount":'',"unit":""}],"cancellationFee":{"currency":'',"amount":''},"minimumFare":{"currency":'',"amount":''},"serviceFee":{"currency":'',"amount":''}
    ,"priceAfterbaseFare":priceAfterbaseFare ,"rideTimeFare":{"currency":currency,"amount":Ride_fare ,"unit":"Minute"} ,"fareBeforeThreshold":{"currency":'',"amount":'' ,"unit":""} ,"airportFare":{"currency":"","amount":""} ,"maximumFare":{"currency":"","amount":""} }]}

                  item["price"]=price_format

                  appUrl_format = {"playStore":"https://play.google.com/store/apps/details?id=com.utoo.customer&hl=en",
        "appleAppStore":"https://itunes.apple.com/in/app/utoo/id1112893564?mt=8",
        "microsoft":"",
        "blackberry":""}
                  item["appUrl"]=appUrl_format

                  bookingViaphone_format =  {"availability":'',"phoneNum":''}
                  item["bookingViaphone"]=bookingViaphone_format


                  item["luggageCapacity"]=''



                  item["typeofvehicle"]=3  # #1:bike/cycle,2:auto,3:car
                  typeofcar=''
                  max_seat=''
                  if serv == "SEDAN" :
                    typeofcar=2 
                    max_seat=4
                  if serv=="SUV"  :
                    typeofcar=3
                    max_seat=6
                  if serv=="COMPACT":
                    typeofcar=1
                    max_seat=4
                  item["typeofcar"]=typeofcar # #1:hatchback,2:sedan,3:SUV,4:luxury
                  seatingCapacity_format = {"min":1,"max":max_seat}
                  item["seatingCapacity"]=seatingCapacity_format
                  item["childFriendly"]=''
                  item["wheelChairAssistance"]='' 
                  item["surgePricing"]=False
                  item["timestamp"]=int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
                  item["email"]="support@utoo.cab"
                  item["phone"]=phone
                  yield item   
                  print item        
