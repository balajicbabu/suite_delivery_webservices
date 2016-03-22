import json
import urllib2
from pprint import pprint
import test
import sys

def get_list_of_files_folders_from_hub(url, hub):
    test.log("get_list_of_files_folders_from_hub")
    test.log("url : " + url)
    complete_url = url + hub
    print complete_url 
    data = None  
    
    try:
        dict = post_url_data(complete_url, data)
        #pprint(dict)
        files = dict['files']
        #pprint(files)
        new_data_dict = None
        if(len(files) > 0):
            print len(files)
            for i in range(len(files)):
                new_data_dict = dict['files'][i]
                folder = new_data_dict['folder']
                if(folder):
                    print folder
                    print new_data_dict
                    break
            if(new_data_dict and new_data_dict != None):
                dict = post_url_data(complete_url, new_data_dict)
                print dict
                return new_data_dict
        else:
            test.fail("No folders or files exist")

    except Exception as e:
        test.fail("get_list_of_files_folders_from_hub")
        print e
        s = str(e)
        print sys.exc_info()
        test.log(s)
    
   

def get_list_of_files_folders_from_parent_folder_in_hub(url, hub, json_data):
    test.log("get_list_of_files_folders_from_parent_folder_in_hub")
    test.log("url : " + url)
    complete_url = url + hub + "/parent"
    print complete_url 
    dict = post_url_data(complete_url, json_data)
    files = dict['files']
    new_data_dict = None
    if(len(files) > 0):
            print len(files)
    else: 
        test.fail("no files exist in parent folder including the child file")

def post_url_data(url, data):
    test.log("post_url_data")
    test.log("url : " + url)
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    dict = json.load(response)
    return dict
            
        
