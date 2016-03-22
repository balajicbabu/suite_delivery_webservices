import json
import urllib2
from pprint import pprint
import test
import squish
import testData

def get_list_of_media_families(url, campaign_id):
    test.log("get_list_of_media_families :" + url + campaign_id)
    complete_url = url + campaign_id
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    squish.snooze(10)
    test.log("get_list_of_media_families : " + complete_url)
    #pprint(dict)
      
    number_of_results = dict['numberOfResults']
    media_family_id = None
    if(number_of_results > 0):
        print number_of_results
        count = 0
        for i in range(number_of_results):
            count = count + 1
            dict_of_media_family_id_list = dict['results'][i]
            media_family_id = dict_of_media_family_id_list['id']
            print media_family_id
        test.log("successfully retrieved the no of results :")
        if(number_of_results != count):
            test.fail("assets doesn't match the number of results retrieved")
    else:
        test.fail("No results exist for media family")
    
    if(media_family_id and media_family_id != None):
         test.log("media family id exists : ", media_family_id)
         test.passes("Media family exists")
         return media_family_id
    else:
        test.fail("Failed to retrieve media family id")
        
def get_list_of_assets(url, media_family_id):
    test.log("get_list_of_assets")
    test.log("url : " + url)
    test.log("media_family_id " + media_family_id)
    complete_url = url + media_family_id
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    squish.snooze(10)
    test.log("get_list_of_assets" + complete_url)
    
    number_of_results = dict['numberOfResults']
    print number_of_results
    if(number_of_results > 0):
        count = 0
        print number_of_results
        test.log("successfully retrieved list of assets :")
        for i in range(number_of_results):
            count = count + 1
            assets_list = dict['results'][i]
            asset_id = assets_list['id']
            print asset_id
        if(number_of_results != count):
            test.fail("assets doesn't match the number of results retrieved")
        else:
            test.passes("asset ids exist")
    else:
        test.fail("No results exist for media family to get the list of assets")
        testdata = testData.create("shared", "status.failed")
        try:
            with open(testdata, "w+") as f:
                test.log("Failed so create a status file")  
        except Exception as e:
            print e
            s = str(e)
            test.log(s)

        
    
            
        
