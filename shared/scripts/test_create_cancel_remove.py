#import deliverywebservices
#import restart_delivery
import time
#import remove_delete_delivery
import test
#import stop_cancel_delivery
#import check_contents_on_ftp_after_cancel
import squish

def create_cancel_remove_delivery(create_delivery_url, create_delivery_data_success, check_delivery_status_url, cancel_delivery_url, remove_delivery_url, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password, success):
    test.log("create_cancel_remove_delivery")
    test.log("create_delivery_url : " + create_delivery_url)
    test.log("check_delivery_status_url : " + check_delivery_status_url)
    test.log("cancel_delivery_url : " + cancel_delivery_url)
    test.log("remove_delivery_url : " + remove_delivery_url)

    delivery_id = None
    delivery_stage = None
    source(findFile("scripts", "deliverywebservices.py"))
    delivery_id = create_save_delivery_using_post_url(create_delivery_url, create_delivery_data_success)
    source(findFile("scripts", "remove_delete_delivery.py"))
    squish.snooze(10)
    if(delivery_id or delivery_id != None):
        cancelling_delivery(check_delivery_status_url, cancel_delivery_url, delivery_id, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)      
        success = remove_delivery(remove_delivery_url, delivery_id,success)
        test.log("delivery removed so returning success : ")
        return success
    else:
        test.fail("delivery id is not created")
        return success

def cancelling_delivery(check_delivery_status_url, cancel_delivery_url, delivery_id, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password):
    test.log("cancelling delivery")
    files_on_ftp = False
    delivery_stage = check_delivery_status(check_delivery_status_url, delivery_id)
    if(delivery_stage == "CREATED" or delivery_stage == "SUBMITTED" or delivery_stage == "STARTED" or delivery_stage == "IN_PROGRESS"):
       test.log("Delivery successfully cancelled")
    #cancel the delivery
       print delivery_stage
       source(findFile("scripts", "stop_cancel_delivery.py"))
       delivery_stage = stop_delivery(cancel_delivery_url, delivery_id)
       squish.snooze(30)
       delivery_stage = check_delivery_status_until_cancelled(check_delivery_status_url, delivery_id)
        
       source(findFile("scripts", "check_contents_on_ftp_after_cancel.py"))

       delivery_ftp_path = get_delivery_ftp_path(check_delivery_status_url, delivery_id)
       if(delivery_ftp_path or delivery_ftp_path != None):
           files_on_ftp = check_contents_in_ftp_server(delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
           if(files_on_ftp):
               test.passes("File transfer has been successfully cancelled and contents has been checked on FTP")
       elif(delivery_stage == "CANCELLED"):
           test.log("Delivery Cancelled")
           test.passes("Delivery has been successfully cancelled")
       else:
           test.fail("Failed to cancel delivery")
    return

        
def check_delivery_status(check_delivery_status_url, delivery_id):
        test.log("check delivery status")
        source(findFile("scripts", "deliverywebservices.py"))

        delivery_stage = check_delivery_status(check_delivery_status_url, delivery_id)
        test.log(delivery_stage)
        return delivery_stage
    
def check_delivery_status_until_cancelled(check_delivery_status_url, delivery_id):
        test.log("check_delivery_status_until_cancelled")
        source(findFile("scripts", "deliverywebservices.py"))

        while(True):
            delivery_stage = check_delivery_status(check_delivery_status_url, delivery_id)
            test.log(delivery_stage)
            if(delivery_stage == "CANCELLED"):
                return delivery_stage
            elif (delivery_stage == "FAILED"):
                test.fail("Delivery cancel failed")
                return delivery_stage
            
