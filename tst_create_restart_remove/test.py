import test
import testData
def main():
    test.log("Test Case Name: test_create_restart_remove")
    
    data = testData.dataset("s_list_of_webservices.tsv")[0]
    
    create_failed_delivery_data = { 
    "serviceOriginName": "Dove UI",
    "callBackEndPoint": None,
    "callBackReferenceId": None,
    "requestTime": None,
    "sourceFile": 'hub://hub-t1/mirriad/storage/QA/MP4.mp4',
    "deliveryFile": 'hub://hub-t1/mirriad/storage/QA/MP41.mp4',
    "assetId": '10006',
    "campaignId": '10450402',
    "deliveryTargetService": 'VEVO',
    "revertOperation": False 
    }
    
    create_delivery_url = testData.field(data, "create_save_delivery_using_post_url")
    get_delivery_status_url = testData.field(data, "get_delivery_status_url")
    restart_delivery_url = testData.field(data, "restart_delivery_using_put_url")
    remove_delivery_url = testData.field(data, "delete_delivery_using_delete_url") 
    success = False
    
    source(findFile("scripts", "test_create_restart_remove.py"))

    success = create_restart_remove_delivery(create_delivery_url, create_failed_delivery_data, get_delivery_status_url, restart_delivery_url, remove_delivery_url, success)
    
    if(success):
        test.passes("test_create_restart_remove delivery passed")
    else:
        test.fail("test_create_restart_remove delivery failed")
        testdata = testData.create("shared", "status.failed")
        try:
            with open(testdata, "w+") as f:
                test.log("Failed so create a status file")  
        except Exception as e:
            print e
            s = str(e)
            test.log(s)      