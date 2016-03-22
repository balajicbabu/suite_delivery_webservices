import test
import testData
import requests
import squish
import json
import urllib2

def main():
    
    test.log("Test Case Name: tst_revert_delivery")
    
    data = testData.dataset("s_list_of_webservices.tsv")[0]
    get_delivery_status_url = testData.field(data, "get_delivery_status_url")
    revert_delivery_url = testData.field(data, "revert_delivery_with_id_put_call")

    data = testData.dataset("delivery_ids_for_reverting.tsv")[0]
    parent_delivery_id = testData.field(data, "delivery_id")  
    videoISRC = testData.field(data, "videoISRC")
    
    test.log(" get_delivery_status_url : " + get_delivery_status_url)  
    test.log(" revert_delivery_with_id : " + revert_delivery_url) 
    test.log(" delivery_id : " + parent_delivery_id)
    test.log(" videoISRC: " + videoISRC)
    
    data = testData.dataset("ftp_login_details.tsv")[0]
    ftp_vevo_host = testData.field(data, "ftp_vevo_host")  
    ftp_vevo_user = testData.field(data, "ftp_vevo_user")  
    ftp_vevo_password = testData.field(data, "ftp_vevo_password")  
    
    manifest_parse_success_replace_success = findFile("testdata", "vevo_status\\parse_success_replace_success\\status-manifest.xml")

    #latest_revert_id = "ff80808147da5cc80147e9c872f00172"
    latest_revert_id = revert_delivery(revert_delivery_url, get_delivery_status_url, parent_delivery_id)
    if(latest_revert_id and latest_revert_id!=None):
        delivery_stage = check_delivery_status_until_waiting_on_confirmation(get_delivery_status_url, latest_revert_id)
        ftp_transfer(get_delivery_status_url, parent_delivery_id, latest_revert_id, delivery_stage, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, manifest_parse_success_replace_success)
    else:
        test.fail("latest revert id is null or doesn't exist")

def revert_delivery(url, get_delivery_status_url, delivery_id):
    
    test.log("revert_delivery : " + url + delivery_id)

    squish.snooze(10)
    response = requests.put(url + delivery_id)
    squish.snooze(30)

    print response.status_code
    test.log("response code : " + str(response.status_code))
    if(response.status_code == 200):
        test.passes("Revert delivery initiated: ")
    else:
        test.fail("Revert delivery initiating failed")
   
    snooze(40)
    
    complete_url = get_delivery_status_url + delivery_id

    source(findFile("scripts", "deliverywebservices.py"))
    revert_stage = check_revert_status_with_complete_url(complete_url)
    latest_revert_id = get_latest_revert_id_with_complete_url(complete_url)

    if(revert_stage == "REVERTING" and latest_revert_id != None and latest_revert_id):
        test.log("Reverting the delivery")
        return latest_revert_id
    else:
        test.fail("Failed to Revert the delivery")
        

def check_delivery_status_until_waiting_on_confirmation(get_delivery_status_url, latest_revert_id):
    
    test.log("check delivery status " + latest_revert_id)
    complete_url = get_delivery_status_url + latest_revert_id
    source(findFile("scripts", "deliverywebservices.py"))
    delivery_stage = None
    #ftp_file_path = None
    
    while(True):    
        squish.snooze(60)
        complete_url = get_delivery_status_url + latest_revert_id
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
   
        
def ftp_transfer(get_delivery_status_url, parent_delivery_id, latest_revert_id, delivery_stage, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, local_manifest_file_path):
    
    test.log("ftp_transfer : ")
    test.log("get_delivery_status_url : " + get_delivery_status_url)
    test.log("latest_revert_id : " + latest_revert_id)
    test.log("delivery_stage : " + delivery_stage)
    test.log("delivery_stage : " + local_manifest_file_path)
    test.log("list of revert stages : REVERTED,REVERTING,REVERT_FAILED,UNREVERTABLE,UNREVERTABLE_DUPLICATE,UNREVERTABLE_NO_SOURCE,UNREVERTED")

    
    if(delivery_stage == "WAITING_ON_CONFIRMATION"):
        # get the ftp path and transfer parse success replace success file
        source(findFile("scripts", "connect_to_ftpserver.py"))
        
        complete_url_of_parent = get_delivery_status_url + parent_delivery_id
        complete_url = get_delivery_status_url + latest_revert_id

        ftp_delivery_path = get_delivery_ftp_path_complete_url(complete_url)
        check_contents_in_ftp_server_and_download_manifest(ftp_delivery_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        squish.snooze(30)
        copy_to_ftp_server(local_manifest_file_path, ftp_delivery_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        squish.snooze(60)
        test.log("waiting for 60 more seconds :")
        squish.snooze(60)
        delivery_stage = check_delivery_status_with_complete_url(complete_url)
        revert_stage_of_parent = check_revert_status_with_complete_url(complete_url_of_parent)  # REVERTED
        revert_stage = check_revert_status_with_complete_url(complete_url)  # UNREVERTABLE

        if(delivery_stage == "COMPLETE" and revert_stage == "UNREVERTABLE" and revert_stage_of_parent == "REVERTED"):
            test.passes("Delivery successfully Reverted")
            test.log("revert_stage: " + revert_stage)
            test.log("revert_stage_of_parent: " + revert_stage_of_parent)
        else:
            test.log("delivery_stage: " + delivery_stage)
            test.log("revert_stage: " + revert_stage)
            test.log("revert_stage_of_parent: " + revert_stage_of_parent)
            test.log("Reverting Delivery failed : " + complete_url)
            test.fail("Reverting Delivery failed : " + delivery_stage)
    else:
        test.fail("Reverting delivery has failed to complete the delivery")


    
