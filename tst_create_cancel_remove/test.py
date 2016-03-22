import test
import testData

def main():

    test.log("Test Case Name: test_create_cancel_remove")
    
    data = testData.dataset("s_list_of_webservices.tsv")[0]
    
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
    
    create_delivery_url = testData.field(data, "create_save_delivery_using_post_url")
    get_delivery_status_url = testData.field(data, "get_delivery_status_url")
    cancel_delivery_url = testData.field(data, "cancel_delivery_using_post_url")
    remove_delivery_url = testData.field(data, "delete_delivery_using_delete_url") 
    success = False
    '''t01 ftp connection login details'''
    ftp_vevo_host = "ftp.uk.mirriad.com"
    ftp_vevo_user = "t01-vevo"
    ftp_vevo_password = "eMn7s0xs"
    ftp_vevo_port = 21
    ftp_vevo_vevo_user = "TESTVEVO"
    
    source(findFile("scripts", "test_create_cancel_remove.py"))
    
    success  = create_cancel_remove_delivery(create_delivery_url, create_delivery_data_success, get_delivery_status_url, cancel_delivery_url, remove_delivery_url, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, success)
    if(success):
        test.passes("test_create_cancel_remove passed")
    else:
        test.fail("test_create_cancel_remove failed")
        testdata = testData.create("shared", "status.failed")
        try:
            with open(testdata, "w+") as f:
                test.log("Failed so create a status file")  
        except Exception as e:
            print e
            s = str(e)
            test.log(s)
        
        

        