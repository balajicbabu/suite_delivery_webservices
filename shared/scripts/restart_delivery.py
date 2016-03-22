import httplib 
import urllib2
import requests
import test
import time
import json
import squish

def restart_delivery(restart_url, delivery_id):
           
    test.log("restart_delivery : " + restart_url + delivery_id)

    squish.snooze(10)
    r = requests.put(restart_url + delivery_id)
    print r.status_code
    dicts = json.loads(r.text)
    delivery_stage = dicts['deliveryStage'] 
    
    if(delivery_stage == "RESTARTED"):
        test.log("restarted the server")
        return delivery_stage
    else:
        test.fail("Failed to restart the delivery")
    
    
  
