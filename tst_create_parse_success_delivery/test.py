import test
import sys
import squish
import testData

def main():
    try:
        
        test.log("Test Case Name: tst_create_parse_success_delivery")
        test.log("create parse success delivery")
    
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
        manifest_parse_success_replace_success = "vevo_status\\parse_success_replace_success\\status-manifest.xml"
        manifest_parse_success = "vevo_status\\parse_success\\status-manifest.xml"
        #manifest_parse_success_replace_success = findFile("testdata", "vevo_status\\parse_success_replace_success\\status-manifest.xml")
        #manifest_parse_success = findFile("testdata", "vevo_status\\parse_success\\status-manifest.xml")
        delivery_ftp_path = None
        '''t01 ftp connection login details'''
        ftp_vevo_host = "ftp.uk.mirriad.com"
        ftp_vevo_user = "t01-vevo"
        ftp_vevo_password = "eMn7s0xs"
        ftp_vevo_port = 21
        ftp_vevo_vevo_user = "TESTVEVO"
        
        test.log("manifest_parse_success : " + manifest_parse_success)
        test.log("manifest_parse_success_replace_success : " + manifest_parse_success_replace_success)
        
        x = None
        count = 4 # using count for FTP transfer as a trigger
        delivery_id = None
        delivery_stage = None
        source(findFile("scripts", "create_delivery.py"))
        
        delivery_id = create_delivery_first_step(create_delivery_data_success, videoISRC, hub_status_config_url, create_delivery_url, get_delivery_status_url, manifest_parse_success, manifest_parse_success_replace_success, count, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        squish.snooze(60)

        if(delivery_id or delivery_id != None):
            source(findFile("scripts", "deliverywebservices.py"))
            squish.snooze(60)
            delivery_stage = check_delivery_status(get_delivery_status_url, delivery_id)
            delivery_ftp_path = get_delivery_ftp_path(get_delivery_status_url, delivery_id, count)

        '''remove the delivery as it is on waiting on confirmation, you cannot use the same delivery again
        transfer the file and change the status to completed'''
  
        if(delivery_stage == "WAITING_ON_CONFIRMATION"):
            test.passes("parse_success is successful")
            source(findFile("scripts", "connect_to_ftpserver.py"))
            manifest_parse_success_replace_success = findFile("testdata", manifest_parse_success_replace_success)
            squish.snooze(60)
            copy_to_ftp_server(manifest_parse_success_replace_success, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
            source(findFile("scripts", "deliverywebservices.py"))
            squish.snooze(60)
            delivery_stage = check_delivery_status(get_delivery_status_url, delivery_id)
            if(delivery_stage == "COMPLETE"):
                test.passes("parse_success is successful and parse_success_replace_success is also successful")
            else:
                test.fail("parse_success_replace_success in parse success delivery has failed, deliveryStage : " + delivery_stage)
        elif(delivery_stage == "FAILED"):
            test.fail("Delivery stage is failed after copying parse success file so need not copy parse success replace success file")
        else:
            test.fail("parse_success delivery has failed")
    except Exception as e:
        print e
        s = str(e)
        print sys.exc_info()
        test.log(s)
        test.fail("parse_success has failed due to : " + s)
        testdata = testData.create("shared", "status.failed")
        try:
            with open(testdata, "w+") as f:
                test.log("Failed so create a status file")  
        except Exception as e:
            print e
            s = str(e)
            test.log(s)
