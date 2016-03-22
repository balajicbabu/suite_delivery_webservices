import test
import testData
import urllib2
import json
# import time
#import datetime
# import sys
#from time import gmtime, strftime
import squish
import os

def main(): 
    
    test.log("Test Case Name: tst_bulk_start_queued_deliveries")
    data = testData.dataset("s_list_of_webservices.tsv")[0]
    start_queued_deliveries_get = testData.field(data, "start_queued_deliveries_get_call")
    
    #revert_delivery_with_id_put = testData.field(data, "revert_delivery_with_id_put_call")
    #revert_all_deliveries_get = testData.field(data, "revert_all_deliveries_get_call")
    
    get_delivery_status_url = testData.field(data, "get_delivery_status_url")


    data = testData.dataset("delivery_ids_for_reverting.tsv")[0]
    delivery_id = testData.field(data, "delivery_id")  
    videoISRC = testData.field(data, "videoISRC")
    
    
    data = testData.dataset("ftp_login_details.tsv")[0]
    ftp_vevo_host = testData.field(data, "ftp_vevo_host")  
    ftp_vevo_user = testData.field(data, "ftp_vevo_user")  
    ftp_vevo_password = testData.field(data, "ftp_vevo_password")  
    # ftp_vevo_port = testData.field(data, "ftp_vevo_port")  
    # ftp_vevo_vevo_user = testData.field(data, "ftp_vevo_vevo_user")  
        
    #manifest_parse_success_replace_success = "vevo_status\\parse_success_replace_success\\status-manifest.xml"

    test.log("get_delivery_status_url: " + get_delivery_status_url)
    test.log("delivery_id: " + delivery_id) 
    test.log("videoISRC: " + videoISRC) 
    
    manifest_parse_success_replace_success = findFile("testdata", "vevo_status\\parse_success_replace_success\\status-manifest.xml")

    squish.snooze(30)
    start_queued_deliveries(start_queued_deliveries_get)
    delivery_stage = check_delivery_status_until_waiting_on_confirmation(get_delivery_status_url, delivery_id)
    ftp_transfer(get_delivery_status_url, delivery_id,delivery_stage, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, manifest_parse_success_replace_success)

def start_queued_deliveries(queued_deliveries_url):
    
    test.log("queued_deliveries_url" + queued_deliveries_url) 
    open = urllib2.urlopen(queued_deliveries_url)
    response_code = open.getcode()
    dict = json.load(open)
    
    request_status = dict['requestStatus'] 
    
    if(response_code == 200 and request_status == "OK"):
        test.log("started queued deliveries, response returned 200 and status is OK")
    else:
        test.log("request_status is not found")
        test.fail("response_code: " + response_code)

def check_delivery_status_until_waiting_on_confirmation(get_delivery_status_url, delivery_id):
    
    test.log("check delivery status " + delivery_id)
    complete_url = get_delivery_status_url + delivery_id
    source(findFile("scripts", "deliverywebservices.py"))
    delivery_stage = None
    squish.snooze(30)

    while(True):    
        squish.snooze(60)
        complete_url = get_delivery_status_url + delivery_id
        print complete_url 
        open = urllib2.urlopen(complete_url)
        dict = json.load(open)
        delivery_stage = dict['deliveryStage']
        test.log("delivery_stage : " + delivery_stage)
        if(delivery_stage == "WAITING_ON_CONFIRMATION"):
            return delivery_stage
        elif(delivery_stage == "FAILED"):
            test.fail("delivery stage is failed")
            return delivery_stage
        
def ftp_transfer(get_delivery_status_url, delivery_id,delivery_stage, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, local_manifest_file_path):
    
    test.log("ftp_transfer : ")
    test.log("get_delivery_status_url : " + get_delivery_status_url)
    test.log("delivery_id : " + delivery_id)
    test.log("delivery_stage : " + delivery_stage)
    test.log("delivery_stage : " + local_manifest_file_path)
    
    
    if(delivery_stage == "WAITING_ON_CONFIRMATION"):
        # get the ftp path and transfer parse success replace success file
        source(findFile("scripts", "connect_to_ftpserver.py"))
        complete_url = get_delivery_status_url + delivery_id

        ftp_delivery_path = get_delivery_ftp_path_complete_url(complete_url)
        check_contents_in_ftp_server_and_download_manifest(ftp_delivery_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        squish.snooze(30)
        copy_to_ftp_server(local_manifest_file_path, ftp_delivery_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        squish.snooze(90)
        delivery_stage = check_delivery_status_with_complete_url(complete_url)
        if(delivery_stage == "COMPLETE"):
            test.passes("Queued Delivery successfully completed")
            #change the flight end date to 30 seconds from now
            os.system("C:\\utils\\run_update_campaign_end_dates.bat 84062112")

        else:
            test.log("Queued Delivery failed : " + complete_url)
            test.fail("Queued Delivery failed : " + delivery_stage)
    else:
        test.fail("queued delivery has failed to complete the delivery")

    
    
    
    
    
    
    
