# -*- coding: utf-8 -*-
import scrapy
import functools
import re
import json
import functools
from bs4 import BeautifulSoup
import csv 
import re
import unicodedata
import ast
from newzealandvisa.items import NewzealandvisaItem
docs=["Original passport with 6 months validity from date of arrival in New Zealand + Old Passports if any.","Visa Application Forms.","Covering letter mentioning details of travel, applicant and duration of stay.","Hotel Confirmation.","Tour Itinerary.","Air Tickets","IT Returns / Form 16 for last 3 years.","Original personal bank statements for last 6 months with bank seal & sign on each and every page.","International Credit card copy and statements with limits.","Salary Slips for last 03 months if employed","Job Confirmation letter. if employed","Original Leave letter from Employer/School/College.","Company registration proof eg. Shop ACt/MOA/Deed etc. - if self employed.","Retire letter/ pension order - if retired","Student id/ bonafide from school/college - if student","an online application or your completed visitor visa application (form number INZ 1017)","2 colour passport photos","a passport that's valid for at least 3 months after the date you plan to leave NZ","a ticket out of NZ, or enough money to buy one","proof you have enough money to live on while you're in NZ."]
class NZvisa(scrapy.Spider):
      name="nzvisa"

      start_urls=['https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/tools-and-information/tools/office-and-fees-finder']

      def parse(self,response):

        data=response.css('script[type="text/javascript"] ::text').extract()
        data2=data[0].replace('\n','').replace('  ','').replace("null","None").replace("true","True").replace("false","False")
        data3=data2.replace('var off_data_data =','').replace(';// Instantiate API implementationvar off_data_tool = new inz.tools.OFFTool(off_data_data, \'/@@off_ajax\', {"filtersTitle": "Use this tool to find relevant fees and receiving centre information for a visa or employer scheme", "filtersCallToActionLabel": "View fees & Receiving Centre"});','')
        data1=ast.literal_eval(data3)  # data=json.loads(data4)
        citizenship_countries=data1["citizenship_countries"]   #  data  format  {'label': 'Zimbabwe', 'value': 'ZWE'}  len=207  it is useless
        visas_and_schemes=data1["visas_and_schemes"]  # 'productSets': [{  id title 
        residence_countries=data1["residence_countries"]   # {'label': 'Kiribati', 'regions': None, 'value': 'KIR'}  247
        countries=[]

        for data in citizenship_countries :
            countries.append(data["value"])

        for data  in residence_countries :
            country=data["label"]  # label': 'Zimbabwe',
            code=data["value"]  # value': 'KIR
            region=data["regions"]  # 'regions': None,
            
            if code in countries :
                for datadata in visas_and_schemes  :
                    uid=datadata["uid"]   # 6047a8ec183e45909dc8ade7bd56bdaf
                    title=datadata["title"]  #  visit or study
                    productSets=datadata["productSets"]   #  list 

                    for product in productSets :
                        citizenshipRestrictions=product['citizenshipRestrictions']  # list or None
                        groupName=product["groupName"].strip()  # Paper submission
                        selectionLabel=product["selectionLabel"]
                        selectionValues=product["selectionValues"]
                        selectionval=selectionValues
                        if selectionValues==None :
                            selectionval=''
                        #print product
                        #print '\n-------' , selectionval ,'-----------------\n\n\n'
                        value_list=[]
                        for value1 in selectionval :
                            value_list.append(value1["value"])

                        xx=1
                        try :
                            if code in citizenshipRestrictions :
                                xx=0
                        except :
                            a=''

                        if region==None :
                            if xx==0 or citizenshipRestrictions==None :
                                
                                #print url1
                                if value_list==[] :
                                    url1="https://www.immigration.govt.nz/@@off_ajax?uid="+uid+"&citizenship="+code+"&residenceCountry="+code+"&residenceRegion="+"&groupName="+ groupName.replace(' ','%20') +"&selectionValue="
                                    yield scrapy.Request(url1,callback=self.parse_fee,meta={'country':country,'name':title,'region':''})
                                else :
                                    for sel in value_list :
                                        url1="https://www.immigration.govt.nz/@@off_ajax?uid="+uid+"&citizenship="+code+"&residenceCountry="+code+"&residenceRegion="+"&groupName="+ groupName.replace(' ','%20') +"&selectionValue="+sel
                                        yield scrapy.Request(url1,callback=self.parse_fee,meta={'country':country,'name':title,'region':''})

                        else  :
                            for re in region :
                                if xx==0 or citizenshipRestrictions==None :
                                    
                                    #print url1
                                    if value_list==[] :
                                        url1="https://www.immigration.govt.nz/@@off_ajax?uid="+uid+"&citizenship="+code+"&residenceCountry="+code+"&residenceRegion="+re.strip().replace(' ','%20')+"&groupName="+ groupName.replace(' ','%20') +"&selectionValue="
                                        yield scrapy.Request(url1,callback=self.parse_fee,meta={'country':country,'name':title,'region':re })
                                    else :
                                      for sel in value_list :
                                        url1="https://www.immigration.govt.nz/@@off_ajax?uid="+uid+"&citizenship="+code+"&residenceCountry="+code+"&residenceRegion="+"&groupName="+ groupName.replace(' ','%20') +"&selectionValue="+sel
                                        yield scrapy.Request(url1,callback=self.parse_fee,meta={'country':country,'name':title,'region':''})

                            #yield scrapy.Request(url,callback=self.parse_fee,meta={'country':country,'name':name})

                            #https://www.immigration.govt.nz/@@off_ajax?uid=d2f52d21fb084495bafcf87ce8df99d5&citizenship=CHN&residenceCountry=CHN&residenceRegion=Inner%20Mongolia&groupName=Paper%20submission&selectionValue=
      def parse_fee(self,response):
        

        data2=(response.body).replace('\n','').replace('  ','').replace("null","None").replace("true","True").replace("false","False")
        data1=ast.literal_eval(data2)
        if  len(data1) !=3 :

            print response.url
            fees=[]
            imm_fee=''
            try :
                imm_fee= data1['stages'][0]['immigrationCosts']
            except :
                a=''
            if imm_fee!='' and imm_fee!=None:
                unit=imm_fee[0]['currency']
                type1='Immigration costs'
                price=imm_fee[0]['items'][0]['amountFrom'].replace(',','').replace('.','')
                price_f=float(price)
                fees.append({'amount': price_f,'type':type1,'currency':unit})

            pass_fee=''
            try:
                pass_fee= data1['stages'][0]['receivingCentreFees']
            except :
                a=''
            #print pass_fee
            if pass_fee !='' and pass_fee!=None:
               new_cur=pass_fee[0]["currency"]
               new_list=pass_fee[0]["items"]
               for list1 in new_list :
                  price1=list1["amountFrom"].replace(",",'').replace('.','')
                  type2=list1["title"]
                  fees.append({'amount': float(price1),'type':type2,'currency':new_cur})

            amount=''
            time1=''
            try :
                time1=data1['stages'][0]['timeFrames'][0]["value"]
            except :
                a=''
            if time1!='' and time1!=None :
              try :
                time2=time1.split()
                #print time2
                amount=int(time2[0].replace(',','').strip())
                dayss=time2[-1]
                if 'month' in dayss :
                    amount=amount*30
                elif 'week' in payss :
                    amount=amount*7
              except :
                a=''

            item=NewzealandvisaItem()
            visa={}
            visa.update({"image":'https://pinoyontheroad.files.wordpress.com/2014/07/new-zealand-visa.png?w=640'}) 
            visa.update({"type":""})
            visa.update({"name":response.meta["name"]})
            rules=[{"nationality":"" , "destinationCountry":'New Zealand', "region":response.meta['region'], "residenceCountry":response.meta['country'],"travelAllowed":'',"individualBooking":'',"required":True,"maxValidity":"","maxStay":'',"docsRequired":docs,"flightAdvanace":'',"hotelAdvance":'',"fees":fees,"online":"","daysRequired":amount,"onArrival":'',"link":'https://www.immigration.govt.nz/new-zealand-visas/apply-for-a-visa/tools-and-information/tools/office-and-fees-finder'}]
            visa.update({"rules":rules})
            item["visa"]=visa
            yield item
            print item



