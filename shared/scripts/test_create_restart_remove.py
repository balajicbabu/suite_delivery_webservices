#import deliverywebservices
#import restart_delivery
import time
#import remove_delete_delivery
import test
import squish

def create_restart_remove_delivery(create_delivery_url, create_failed_delivery_data, check_delivery_status_url, restart_url, remove_delivery_url, success):
    test.log("create_restart_remove_delivery()")
    test.log("create_delivery_url : " + create_delivery_url)
    test.log("check_delivery_status_url : " + check_delivery_status_url)
    test.log("restart_url : " + restart_url)
    test.log("remove_delivery_url : " + remove_delivery_url)

    delivery_id = None
    delivery_stage = None
    
    source(findFile("scripts", "deliverywebservices.py"))

    delivery_id = create_save_delivery_using_post_url(create_delivery_url, create_failed_delivery_data)
    squish.snooze(30);
    if(delivery_id or delivery_id != None):
        delivery_stage = restarting_delivery(check_delivery_status_url, restart_url, delivery_id) 
        source(findFile("scripts", "remove_delete_delivery.py"))
        squish.snooze(30);
        success = remove_delivery(remove_delivery_url, delivery_id,success)
        return success
    else:
        test.fail("delivery id is not created")
        #restart_delivery(restart_url, delivery_id)

def restarting_delivery(check_delivery_status_url, restart_url, delivery_id):
    
    test.log("restarting_delivery()")
    delivery_stage = check_delivery_status(check_delivery_status_url, delivery_id)
    if(delivery_stage == "FAILED"):
       test.log("Delivery successfully failed")
    #restart the failed delivery
       source(findFile("scripts", "restart_delivery.py"))
       delivery_stage = restart_delivery(restart_url, delivery_id)
       if(delivery_stage == "RESTARTED"):
           while(True):
               squish.snooze(10)
               source(findFile("scripts", "deliverywebservices.py"))
               delivery_stage = check_delivery_status(check_delivery_status_url, delivery_id)
               if(delivery_stage == "FAILED"):
                   test.log("Delivery successfully failed")
                   return delivery_stage
        
        
def check_delivery_status(check_delivery_status_url, delivery_id):
    test.log("check_delivery_status()")
    while(True):
        squish.snooze(10)
        source(findFile("scripts", "deliverywebservices.py"))
        delivery_stage = check_delivery_status(check_delivery_status_url, delivery_id)
        test.log(delivery_stage)
        if(delivery_stage == "FAILED"):
            test.log("Delivery successfully failed")
            return delivery_stage
