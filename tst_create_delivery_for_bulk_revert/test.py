import test
import sys
import squish
import testData
import os
import json
import urllib2
def main():
    
    test.log("Test Case Name: tst_create_delivery_for_bulk_revert")
 
    '''run the script to set the delivery'''
    
    # arguments to pass: 1 create a campaign with start date in the past and end date in future and any campaign Id: 84062112
    # arguments to pass: 2 QUEUED -create a campaign with start date in the future and end date in future and any campaign Id: 84062112
    # arguments to pass: 3 create a campaign with start date in the past and end date in past and any campaign Id: 84062112
    test.log("update adbroker database for campaign start and end dates")
    os.system("C:\\utils\\run_update_campaign_dates.bat 1 12735523")
    
    test.log("create successful delivery")
    delivery_id = None
    delivery_stage = None
    create_delivery_data = { 
        "serviceOriginName": "Dove UI",
        "callBackEndPoint": None,
        "callBackReferenceId": None,
        "requestTime": None,
        "sourceFile": 'hub://hub-t1/mirriad/storage/QA/GBUV71000779_I_AM_ARROWS_Another Picture Of You_no_P_logo_v2.mov',
        "deliveryFile": 'hub://hub-t1/mirriad/storage/QA/GBUV71000779_I_AM_ARROWS_Another Picture Of You_with_P_logo_v2.mov',
        "assetId": '6287',
        "campaignId": '12735523',
        "deliveryTargetService": 'VEVO',
        "revertOperation": False 
    }
        
    videoISRC = "USUV71100201" 
    #os.system("C:\\utils\\run_update_campaign_end_dates.bat 12735523")

        
    data = testData.dataset("s_list_of_webservices.tsv")[0]
            
    create_delivery_url = testData.field(data, "create_save_delivery_using_post_url")
    get_delivery_status_url = testData.field(data, "get_delivery_status_url")
       
    
    data = testData.dataset("ftp_login_details.tsv")[0]
    ftp_vevo_host = testData.field(data, "ftp_vevo_host")  
    ftp_vevo_user = testData.field(data, "ftp_vevo_user")  
    ftp_vevo_password = testData.field(data, "ftp_vevo_password")  
    
    local_manifest_file_path = findFile("testdata", "vevo_status\\parse_success_replace_success\\status-manifest.xml")

    squish.snooze(30)
    delivery_id = create_delivery_and_save_delivery_id_to_tsv(create_delivery_url, create_delivery_data,videoISRC)
    squish.snooze(30)
    delivery_stage = check_delivery_status_until_waiting_on_confirmation(get_delivery_status_url, delivery_id)
    ftp_transfer(get_delivery_status_url, delivery_id, delivery_stage, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, local_manifest_file_path)

        
def create_delivery_and_save_delivery_id_to_tsv(create_delivery_url, create_delivery_data,videoISRC):   
    
    source(findFile("scripts", "deliverywebservices.py"))

    '''create the delivery'''
    delivery_id = create_save_delivery_using_post_url(create_delivery_url, create_delivery_data)
    squish.snooze(40)
         
    if(delivery_id and delivery_id != None):
            
        test.log("delivery successfully created", delivery_id)
        testdata = testData.create("shared", "delivery_ids_for_bulk_reverting.tsv")
        dataFile = open(testdata, "w")
        dataFile.write("delivery_id\tvideoISRC\n")
        dataFile.write(delivery_id + "\t" + videoISRC)
        dataFile.close()
        test.log("tsv created")
        return delivery_id
    else:
        test.fail("delivery id is none")
    
            
def check_delivery_status_until_waiting_on_confirmation(get_delivery_status_url, delivery_id):
    
    test.log("check delivery status " + delivery_id)
    complete_url = get_delivery_status_url + delivery_id
    source(findFile("scripts", "deliverywebservices.py"))
    delivery_stage = None
    #ftp_file_path = None
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
        
def ftp_transfer(get_delivery_status_url, delivery_id, delivery_stage, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, local_manifest_file_path):
    
    test.log("ftp_transfer : ")
    test.log("get_delivery_status_url : " + get_delivery_status_url)
    test.log("delivery_id : " + delivery_id)
    test.log("delivery_stage : " + delivery_stage)
    test.log("local_manifest_file_path : " + local_manifest_file_path)
    
    
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
            # change the flight end date to 30 seconds from now
            os.system("C:\\utils\\run_update_campaign_end_dates.bat 12735523")
            test.passes("Delivery successfully completed")
        else:
            test.log("Delivery failed : " + complete_url)
            test.fail("Delivery failed : " + delivery_stage)
    else:
        test.fail("delivery has failed to complete the delivery")        
