import requests
import test

def remove_delivery(remove_delivery_url, delivery_id,success):
    
    test.log("remove_delivery : " + remove_delivery_url + delivery_id)
    r = requests.delete(remove_delivery_url + delivery_id)
    #print r.status_code
    #print r.text
    
    if(r.text):
        test.log("removed the delivery card successfully")
        success = True
        return success
    else:
        test.fail("Failed to remove the delivery card")
    
    return success
