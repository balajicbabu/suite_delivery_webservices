import requests
import test

def stop_delivery(stop_cancel_delivery, delivery_id):
    
    test.log("stop delivery : " + stop_cancel_delivery + delivery_id)
   
    r = requests.post(stop_cancel_delivery + delivery_id)
    
    print r.status_code
    print r.text
    
    if(r.text):
        test.log("stopped or cancelled the delivery successfully")
    else:
        test.fail("Failed to cancel or stop the delivery")
