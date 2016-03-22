import test
import sys
import squish
import testData
import os
def main():
    
    test.log("Test Case Name: tst_create_queued_delivery")
 
    '''run the script to set the queued delivery'''
    
    # arguments to pass: 1 create a campaign with start date in the past and end date in future and any campaign Id: 84062112
    # arguments to pass: 2 QUEUED -create a campaign with start date in the future and end date in future and any campaign Id: 84062112
    # arguments to pass: 3 create a campaign with start date in the past and end date in past and any campaign Id: 84062112
    test.log("update adbroker database for campaign start and end dates")
    os.system("C:\\utils\\run_update_campaign_dates.bat 2 84062112")
    
    try:
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
        "assetId": '4134',
        "campaignId": '84062112',
        "deliveryTargetService": 'VEVO',
        "revertOperation": False 
        }
        
        videoISRC = "USUV71201410" 
        
        data = testData.dataset("s_list_of_webservices.tsv")[0]
            
        create_delivery_url = testData.field(data, "create_save_delivery_using_post_url")
        get_delivery_status_url = testData.field(data, "get_delivery_status_url")
        
        source(findFile("scripts", "deliverywebservices.py"))

        '''create the delivery'''
        delivery_id = create_save_delivery_using_post_url(create_delivery_url, create_delivery_data)
        squish.snooze(40)
        
        delivery_stage = check_delivery_status(get_delivery_status_url, delivery_id)
        
        if(delivery_id and delivery_id != None and delivery_stage == "QUEUED"):
            
            test.log("delivery successfully created", delivery_id)
            testdata = testData.create("shared", "delivery_ids_for_reverting.tsv")
            dataFile = open(testdata, "w")
            dataFile.write("delivery_id\tvideoISRC\n")
            dataFile.write(delivery_id + "\t" + videoISRC)
            dataFile.close()
            test.log("tsv created")
        else:
            test.fail("delivery id is none or delivery stage is not queued")
    
    except Exception as e:
        print e
        s = str(e)
        print sys.exc_info()
        test.fail("create queued delivery has failed")
        if(s and s!=None):
            test.log(s)
            test.fail("create queued delivery has failed due to :" + s)
        
