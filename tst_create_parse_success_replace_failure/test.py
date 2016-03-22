import test
import squish
import sys
import testData
def main():
    try:
        test.log("Test Case Name: tst_create_parse_success_replace_failure")

        test.log("create parse success replace failure delivery")
    
        create_delivery_data_success = { 
        "serviceOriginName": "Dove UI",
        "callBackEndPoint": None,
        "callBackReferenceId": None,
        "requestTime": None,
        "sourceFile": 'hub://hub-t1/mirriad/storage/QA/GBUV71000779_I_AM_ARROWS_Another Picture Of You_no_P_logo_v2.mov',
        "deliveryFile": 'hub://hub-t1/mirriad/storage/QA/GBUV71000779_I_AM_ARROWS_Another Picture Of You_with_P_logo_v2.mov',
        "assetId": '12230',
        "campaignId": '27120900',
        "deliveryTargetService": 'VEVO',
        "revertOperation": False 
        }
    
        videoISRC = "GBUV71000779" # I am Arrows
        
        data = testData.dataset("s_list_of_webservices.tsv")[0]
            
        hub_status_config_url = testData.field(data, "get_delivery_config_get_url")
        create_delivery_url = testData.field(data, "create_save_delivery_using_post_url")
        get_delivery_status_url = testData.field(data, "get_delivery_status_url")
        manifest_parse_success_replace_failure = "vevo_status\\parse_success_replace_failure\\status-manifest.xml"
        manifest_parse_success = "vevo_status\\parse_success\\status-manifest.xml"
        #manifest_parse_failure = findFile("testdata", "vevo_status\\parse_failure\\status-manifest.xml")
        #manifest_parse_success_replace_failure = findFile("testdata", "vevo_status\\parse_success_replace_failure\\status-manifest.xml")
        
        test.log("manifest_parse_success : " + manifest_parse_success)
        test.log("manifest_parse_success_replace_failure : " + manifest_parse_success_replace_failure)
        '''t01 ftp connection login details'''
        ftp_vevo_host = "ftp.uk.mirriad.com"
        ftp_vevo_user = "t01-vevo"
        ftp_vevo_password = "eMn7s0xs"
        ftp_vevo_port = 21
        ftp_vevo_vevo_user = "TESTVEVO"
        
        x = None
        count = 2 # using count for FTP to transfer the status-manifest file as a trigger
        delivery_id = None
        initial_failure = False
        delivery_stage = None
        source(findFile("scripts", "create_delivery.py"))
        
        delivery_id = create_delivery_first_step(create_delivery_data_success, videoISRC, hub_status_config_url, create_delivery_url, get_delivery_status_url, manifest_parse_success, manifest_parse_success_replace_failure, count, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        squish.snooze(60)
        if(delivery_id or delivery_id != None):
            source(findFile("scripts", "deliverywebservices.py"))
            #wait for 30 seconds here because delivery stage = waiting on confirmation
            squish.snooze(60)
            delivery_stage = check_delivery_status(get_delivery_status_url, delivery_id)
        else:
            test.log("Initial Delivery Failed")
            initial_failure = True
        
        if(delivery_stage == "FAILED" and initial_failure == False):
            test.passes("parse_success_replace_failure is successful")
        else:
            test.fail("parse_success_replace_failure delivery has failed, deliveryStage : ")
    except Exception as e:
        print e
        s = str(e)
        print sys.exc_info()
        test.log(s)
        test.fail("parse_success_replace_failure has failed due to :" + s)
        testdata = testData.create("shared", "status.failed")
        try:
            with open(testdata, "w+") as f:
                test.log("Failed so create a status file")  
        except Exception as e:
            print e
            s = str(e)
            test.log(s)