import json
import urllib2
from pprint import pprint
import test
#import connect_to_ftpserver
import time
import squish
import testData

def get_delivery_config_get_url(url):
        
        test.log("get_delivery_config_get_url : " + url)
        open = urllib2.urlopen(url)
        dict = json.load(open)
        #pprint(dict)
        
        list_of_hubs = dict['availableHubs']
        
        if(len(list_of_hubs) > 0):
            for hub in list_of_hubs:
                test.log("hub :", hub)
                if(hub == "hub-t1"):
                    test.log("hub exists", hub)
        else:
            test.fail("No Hubs available ")
            
        list_of_delivery_targets = dict['deliveryTargets']
        if(len(list_of_delivery_targets) > 0):
            for delivery_target in list_of_delivery_targets:
                test.log("delivery delivery_target : ", delivery_target)
                if(delivery_target == "VEVO"):
                    test.log("delivery_target exists", delivery_target)
        else:
            test.fail("No Delivery targets available ")
        
def get_delivery_status_list_post(url, get_deliveries_data):
    
    test.log("get_delivery_status_list_post_url : " + url)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(get_deliveries_data))
    dict = json.load(response)
    #pprint(dict)
    
    number_of_results = dict['numberOfResults'] 

    if(number_of_results > 0):
        print number_of_results
        test.log("successfully retrieved the no of deliveries :")
    else:
        test.fail("No delivery results exist")
        testdata = testData.create("shared", "status.failed")
        try:
            with open(testdata, "w+") as f:
                test.log("Failed so create a status file")  
        except Exception as e:
            print e
            s = str(e)
            test.log(s)  
    
def create_save_delivery_using_post_url(url, create_delivery_data):
     
    test.log("create_save_delivery_using_post_url")
    test.log("url : " + url)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(create_delivery_data))
    dict = json.load(response)
    #pprint(dict)
    if(dict['errorList'] and dict['errorList'] != None):
        test.log("Cannot create the delivery")
        test.fail("Duplicate delivery cannot be created")        
    else:    
        deliveryStage = dict['delivery']['deliveryStage'] 
    
        if(deliveryStage == "CREATED"):
            test.log("deliveryStage successfully created ")    
        delivery_id = dict['delivery']['id']
        if(delivery_id and delivery_id!=None):
            test.log("Delivery_id created : " + delivery_id)
        return delivery_id

def check_delivery_status(url, delivery_id):
    test.log("check_delivery_status")
    test.log("url : " + url)
    test.log("delivery_id : " + delivery_id)
    complete_url = url + delivery_id
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    #pprint(dict)
    
    delivery_stage = dict['deliveryStage'] 
    print delivery_stage
    
    if(delivery_stage == "CREATED"):
        test.log("delivery is created : ")
    elif(delivery_stage == "QUEUED"):
        test.log("delivery is Queued : ")    
    elif(delivery_stage == "SUBMITTED"):
        test.log("delivery is submitted : ")
    elif(delivery_stage == "STARTED"):
        test.log("delivery is started in delivery service : ")
    elif(delivery_stage == "IN_PROGRESS"):
        test.log("delivery is in progress - which hits orchestration(FTP Transferring of files): ")
    elif(delivery_stage == "WAITING_ON_CONFIRMATION"):
        test.log("delivery is waiting on confirmation (Waiting for Manifest file to arrive after FTP is done) ")
    elif(delivery_stage == "COMPLETE"):
        test.log("deliveryStage is successfully completed : ")
    elif(delivery_stage == "FAILED"):
        test.log("delivery is failed : ")
    elif(delivery_stage == "CANCELLED"):
        test.log("delivery has been cancelled by user : ") 
    elif(delivery_stage == "RESTARTED"):
        test.log("delivery has been restarted : ") 
    else:
        test.fail("deliveryStage failed to update the status : ")
    
    return delivery_stage


def check_delivery_status_with_complete_url(complete_url):
    test.log("check_delivery_status_with_complete_url")
    test.log("complete_url " + complete_url)
    
    #complete_url = url + delivery_id
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    #pprint(dict)
    
    delivery_stage = dict['deliveryStage'] 
    print delivery_stage
    
    if(delivery_stage == "CREATED"):
        test.log("delivery is created : ")
    elif(delivery_stage == "QUEUED"):
        test.log("delivery is queued : ")    
    elif(delivery_stage == "SUBMITTED"):
        test.log("delivery is submitted : ")
    elif(delivery_stage == "STARTED"):
        test.log("delivery is started in delivery service : ")
    elif(delivery_stage == "IN_PROGRESS"):
        test.log("delivery is in progress - which hits orchestration(FTP Transferring of files): ")
    elif(delivery_stage == "WAITING_ON_CONFIRMATION"):
        test.log("delivery is waiting on confirmation (Waiting for Manifest file to arrive after FTP is done) ")
    elif(delivery_stage == "COMPLETE"):
        test.log("deliveryStage is successfully completed : ")
    elif(delivery_stage == "FAILED"):
        test.log("delivery is failed : ")
    elif(delivery_stage == "CANCELLED"):
        test.log("delivery has been cancelled by user : ") 
    elif(delivery_stage == "RESTARTED"):
        test.log("delivery has been restarted : ") 
    else:
        test.fail("deliveryStage failed to update the status : ")
    
    return delivery_stage
    
    
def get_delivery_ftp_path(url, delivery_id, count):
    test.log("get_delivery_ftp_path")
    test.log("url" + url)
    test.log("delivery_id" + delivery_id)
    while(True):
        squish.snooze(30)
        complete_url = url + delivery_id
        print complete_url 
        open = urllib2.urlopen(complete_url)
        dict = json.load(open)
        #pprint(dict)
        delivery_stage = dict['deliveryStage'] 
        delivery_path = dict['deliveryPath']
        print delivery_stage
    
        if(delivery_stage == "WAITING_ON_CONFIRMATION"):
                return delivery_path
        elif(delivery_stage == "COMPLETE"):
                return delivery_path 
        elif(delivery_stage == "FAILED"):
            return "NOTHING_TO_DO_ON_FAILED"
        elif(delivery_stage == "CANCELLED"):
            return "NOTHING_TO_DO_ON_CANCELLED"
        
def get_delivery_ftp_path_complete_url(complete_url):
    test.log("get_delivery_ftp_path")
    test.log("url" + complete_url)
    while(True):
        squish.snooze(30)
        print complete_url 
        open = urllib2.urlopen(complete_url)
        dict = json.load(open)
        delivery_path = dict['deliveryPath']
        test.log("delivery_path: " + delivery_path)
        return delivery_path
        
    
def check_revert_status_with_complete_url(complete_url):
    
    test.log("check_revert_status_with_complete_url: " + complete_url)
    test.log("list of revert stages : REVERTED,REVERTING,REVERT_FAILED,UNREVERTABLE,UNREVERTABLE_DUPLICATE,UNREVERTABLE_NO_SOURCE,UNREVERTED")
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    revert_stage = dict['revertStage'] 
    print revert_stage
    #test.log("revert stage is : " + revert_stage)    
    return revert_stage 

def get_latest_revert_id_with_complete_url(complete_url):
    
    test.log("get_latest_revert_id_with_complete_url: " + complete_url)
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    latest_revert_id = dict['latestRevertId'] 
    print latest_revert_id
    #test.log(" latest_revert_id is : " + latest_revert_id)    
    return latest_revert_id    
    
    
    
    
