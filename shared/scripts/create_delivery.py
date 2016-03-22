#import filemanipulationservice
#import connect_to_ftpserver
#import read_manifest_xml
#import deliverywebservices
import test
import time
import urllib2
import json
import squish

def create_delivery_first_step(create_delivery_data, videoISRC, hub_status_config_url, create_delivery_url, get_delivery_status_url, local_manifest_file_path_parse_success, local_manifest_file_path, count, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password):
    
    #delivery_stage = None
    #local_manifest_file_path_success = "C:\\tmp\\vevo_status\\parse_success\\status-manifest.xml"
    test.log("create_delivery_first_step")
    test.log("videoISRC : " + videoISRC)
    test.log("hub_status_config_url : " + hub_status_config_url)
    test.log("create_delivery_url : " + create_delivery_url)
    test.log("get_delivery_status_url : " + get_delivery_status_url)
    test.log("local_manifest_file_path : " + local_manifest_file_path)

    if(local_manifest_file_path_parse_success != None):
        test.log("local_manifest_file_path_parse_success in create delivery first step : " + local_manifest_file_path_parse_success)
    else:
        test.log("local_manifest_file_path_parse_success is None for parse failure delivery")

    delivery_ftp_path = None
    manifest_file_path = None
    video_text = None
    first_step_pass = False
    
    source(findFile("scripts", "deliverywebservices.py"))

    '''check the status of delivery hub'''
    get_delivery_config_get_url(hub_status_config_url)
      
    '''create the delivery'''
    delivery_id = create_save_delivery_using_post_url(create_delivery_url, create_delivery_data)
               
    '''check the delivery status and get the ftp delivery path'''
    if(delivery_id and delivery_id != None):
       delivery_ftp_path = get_delivery_ftp_path(get_delivery_status_url, delivery_id, count)
       test.log("Delivery FTP Path: " + delivery_ftp_path)
    else:
       test.fail("No delivery Id returned : or duplicate delivery")
    
    source(findFile("scripts", "connect_to_ftpserver.py"))
       
    if(delivery_ftp_path != "NOTHING_TO_DO_ON_FAILED" and delivery_ftp_path != "NOTHING_TO_DO_ON_CANCELLED"):
        '''connect to FTP and download the manifest path to the local machine'''
        if(delivery_ftp_path and delivery_ftp_path != None):
           manifest_file_path = check_contents_in_ftp_server_and_download_manifest(delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        else:
           test.fail("No delivery path returned from FTP :")
        source(findFile("scripts", "read_manifest_xml.py"))

        '''check the contents in the manifest xml file'''
        if(manifest_file_path and manifest_file_path != None):
           video_text = parsexml(manifest_file_path)
        else:
           test.fail("No manifest_file_path in local machine returned :")
            
        '''compare the original video ISRC code with the one in the manifest.xml file'''
        if(video_text and video_text != None):
            if(videoISRC == video_text):
               first_step_pass = True
               test.log("Video ISRC code in manifest xml matches with the original ISRC code")
               #delivery_status = copy_local_manifest_to_ftp(first_step_pass, ftp_delivery_path, local_manifest_file_path, get_delivery_status_url)
               #return delivery_status
            else:
               test.fail("Video ISRC code in the manifest xml doesn't match the original ISRC code")
               test.log(video_text)
               
    elif(delivery_ftp_path == "NOTHING_TO_DO_ON_CANCELLED"):
        test.log("delivery FTP path returns nothing to do status on cancelled")
        test.log("Delivery stage is cancelled")
        #success
    else:
       test.log("Failed to get delivery_ftp_path and deliver correct files into FTP server") 
       test.fail("Delivery stage is Failed so the delivery has been failed")

    
    if(first_step_pass):
        first_step_pass = False
        test.log("calling copy local manifest file to FTP")
        delivery_id = copy_local_manifest_to_ftp(delivery_ftp_path, local_manifest_file_path_parse_success, local_manifest_file_path, get_delivery_status_url, delivery_id, count, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        return delivery_id
    else:
        test.fail("First step FTP transfer has failed")
        return delivery_id
    

def copy_local_manifest_to_ftp(delivery_ftp_path, local_manifest_file_path_parse_success, local_manifest_file_path, get_delivery_status_url, delivery_id, count, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password):
        
    test.log("copy_local_manifest_to_ftp")
    test.log("delivery_ftp_path : " + delivery_ftp_path)
    test.log("local_manifest_file_path : " + local_manifest_file_path)
    test.log("get_delivery_status_url : " + get_delivery_status_url)
    test.log("delivery_id : " + delivery_id)

    local_manifest_file_path = findFile("testdata", local_manifest_file_path)
    if(local_manifest_file_path_parse_success != None):
        local_manifest_file_path_parse_success = findFile("testdata", local_manifest_file_path_parse_success)
        
    #manifest_parse_success = findFile("testdata", "vevo_status\\parse_success\\status-manifest.xml")
    
    while(True):
        squish.snooze(60)
        complete_url = get_delivery_status_url + delivery_id
        print complete_url 
        open = urllib2.urlopen(complete_url)
        dict = json.load(open)
        delivery_stage = dict['deliveryStage']
        test.log("delivery_stage : " + delivery_stage)
        if(delivery_stage == "WAITING_ON_CONFIRMATION"):
            test.log("status is waiting on confirmation so copy the status-manifest.xml")
            if(count == 1):
                copy_to_ftp_server(local_manifest_file_path_parse_success, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
                squish.snooze(10)
                open = urllib2.urlopen(complete_url)
                dict = json.load(open)
                delivery_stage = dict['deliveryStage']
                if(delivery_stage == "WAITING_ON_CONFIRMATION"):
                    copy_to_ftp_server(local_manifest_file_path, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
                elif(delivery_stage == "FAILED"):
                    test.fail("Delivery stage is failed after copying parse success file")
                else:
                    test.fail("Delivery completed after transferring parse success file but not before transfer of parse success replace success manifest file")
            elif(count == 2):
                copy_to_ftp_server(local_manifest_file_path_parse_success, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
                squish.snooze(10)
                open = urllib2.urlopen(complete_url)
                dict = json.load(open)
                delivery_stage = dict['deliveryStage']
                if(delivery_stage == "WAITING_ON_CONFIRMATION"):
                    copy_to_ftp_server(local_manifest_file_path, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
                elif(delivery_stage == "FAILED"):
                    test.fail("Delivery stage is failed after copying parse success file")
                else:
                    test.fail("Delivery completed after transferring parse success file but not before transfer of parse success replace success manifest file")
            elif(count == 3):
                copy_to_ftp_server(local_manifest_file_path, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
            elif(count == 4):
                copy_to_ftp_server(local_manifest_file_path_parse_success, delivery_ftp_path, ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        else:
            test.fail("Delivery Stage failed before transferring status-manifest file, need not copy manifest files : " + delivery_stage)     
        
        return delivery_id
           
