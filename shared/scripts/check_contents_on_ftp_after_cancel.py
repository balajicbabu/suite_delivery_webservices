
import json
import test
import urllib2
import ftplib  
import sys 
import squish

#there shouldn't be more than 1 file at the end of the transfer, check for submitted, created, in progress,
#deivery path will be created in in_progess stage
def get_delivery_ftp_path(delivery_status_url, delivery_id):
    test.log("get_delivery_ftp_path")
    test.log("delivery_status_url : " + delivery_status_url)
    test.log("delivery_id : " + delivery_id)
    
    complete_url = delivery_status_url + delivery_id
    print complete_url 
    open = urllib2.urlopen(complete_url)
    dict = json.load(open)
    #pprint(dict)
    delivery_stage = dict['deliveryStage'] 
    delivery_path = dict['deliveryPath']
    print delivery_stage
    if(delivery_path or delivery_path != None):
        if(delivery_stage == "CREATED"):
            return delivery_path
        elif(delivery_stage == "SUBMITTED"):
            return delivery_path
        elif(delivery_stage == "STARTED"):
            return delivery_path
        elif(delivery_stage == "IN_PROGRESS"):
            return delivery_path
        elif(delivery_stage == "WAITING_ON_CONFIRMATION"):
            return delivery_path
        elif(delivery_stage == "COMPLETE"):
            return delivery_path 
        elif(delivery_stage == "FAILED"):
            return delivery_path
        elif(delivery_stage == "CANCELLED"):
            return delivery_path
        elif(delivery_stage == "RESTARTED"):
            return delivery_path
    else:
       return delivery_path

# when do you get the delivery ftp path ?? is that in progress stage or submitted stage ?


def check_contents_in_ftp_server(ftp_delivery_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password):
    test.log("check_contents_in_ftp_server")
    test.log("ftp_delivery_path : " + ftp_delivery_path)
    squish.snooze(60)

    files = []
    
    squish.snooze(60)

    try:
        session = ftplib.FTP(ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        #print session
        session.cwd(ftp_delivery_path) # Change working directory 
        files = session.nlst()
        print files
        for filename in files:
            print filename
            if(len(files) == 3):
                test.fail("files are transferred to FTP server even though we have cancelled the delivery")
                return False
            elif(len(files) > 3):
                test.fail("no of files in the FTP server are more than 3 ")
                return False
            elif(len(files) < 3):
                test.passes("no of files in the FTP server are less than 3 ")
                return True
        session.quit()
    except Exception as e:
        print e
        s = str(e)
        print sys.exc_info()
        test.log("exception due to :" + s)
        test.fail("check_contents_in_ftp_server")

         
