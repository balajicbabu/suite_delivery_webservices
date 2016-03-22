import json
import urllib2
from pprint import pprint
import test
import logging
import testData

def get_campaign_service_call(url,campaign_id):
        
    test.log("get_campaign_service_call: campaignId" + url + campaign_id)
    open = urllib2.urlopen(url)
    dict = json.load(open)
    #pprint(dict)
       
    total_number_of_results = dict['numberOfResults']
    
    if(total_number_of_results > 0):
        test.log("total campaign ids : ")
    else:
        test.fail("No campaign found")
       
    list_of_results = dict['results']
    #count = 0
    if(len(list_of_results) > 0):
        test.passes("Campaign service call returned open campaigns")
    else:
        test.fail("No campaign available ")

            
        
