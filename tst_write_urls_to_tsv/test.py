
import test
import testData
import os

def main():
    
    test.log("Test Case Name: tst_write_urls_to_tsv")

    test.log("removing the waiting on confirmation deliveries")
    os.startfile("C:\\utils\\run_remove_awaiting_deliveries.bat")
           
    test.log("writing the web service urls to TSV file")
    
    server_name = "t01"

    get_delivery_config_get_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/config"
    create_save_delivery_using_post_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/deliver"
    get_delivery_status_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/delivery/"

    
    get_delivery_status_list_post_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/query"
    
    restart_delivery_using_put_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/restart/"
    delete_delivery_using_delete_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/remove/"
    cancel_delivery_using_post_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/cancel/"
 
    campaign_service_call_url = "https://" + server_name + "-adbroker.mirriad.com/catalogue/services/api/campaign/list/open"
    
    
    asset_service_to_get_list_of_mediafamilies_url = "https://" + server_name + "-adbroker.mirriad.com/catalogue/services/api/mediafamily/equal/campaign/"
    asset_service_to_get_list_of_assets_url = "https://" + server_name + "-adbroker.mirriad.com/catalogue/services/api/media/equal/mediafamily/"
    
    get_all_files_folders_from_hub_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/files/list/"
    get_all_files_folders_of_parent_in_hub_url = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/files/list/"
    
    start_queued_deliveries_get_call = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/bulk/start/"
    
    revert_delivery_with_id_put_call = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/revert/"
    
    revert_all_deliveries_get_call = "https://" + server_name + "-services.mirriad.com/delivery-web-service/api/bulk/revert/"
    
    campaign_id = "27120900"
    '''asset_id = "12914"'''

  
    testdata = testData.create("shared", "s_list_of_webservices.tsv")
    dataFile = open(testdata, "w")
    dataFile.write("get_delivery_config_get_url\tget_delivery_status_list_post_url\tcreate_save_delivery_using_post_url\trestart_delivery_using_put_url\tdelete_delivery_using_delete_url\tcancel_delivery_using_post_url\tcampaign_service_call_url\tget_delivery_status_url\tcampaign_id\tasset_service_to_get_list_of_mediafamilies_url\tasset_service_to_get_list_of_assets_url\tget_all_files_folders_from_hub_url\tget_all_files_folders_of_parent_in_hub_url\tstart_queued_deliveries_get_call\trevert_delivery_with_id_put_call\trevert_all_deliveries_get_call\n")
    dataFile.write(get_delivery_config_get_url + "\t" + get_delivery_status_list_post_url + "\t" 
                   + create_save_delivery_using_post_url + "\t" + restart_delivery_using_put_url + "\t" + 
                   delete_delivery_using_delete_url + "\t" + cancel_delivery_using_post_url + "\t" + campaign_service_call_url + "\t" + 
                   get_delivery_status_url + "\t" + campaign_id + "\t" + asset_service_to_get_list_of_mediafamilies_url + "\t" + 
                   asset_service_to_get_list_of_assets_url + "\t" + get_all_files_folders_from_hub_url + "\t" + get_all_files_folders_of_parent_in_hub_url + "\t"
                   + start_queued_deliveries_get_call + "\t" + revert_delivery_with_id_put_call + "\t" + revert_all_deliveries_get_call)
    dataFile.close()
    test.log("Finished writing the urls to TSV file")
    
    test.log("writing the ftp_login_details to TSV file")

    '''t01 ftp connection login details'''
    ftp_vevo_host = "ftp.uk.mirriad.com"
    ftp_vevo_user = "t01-vevo"
    ftp_vevo_password = "eMn7s0xs"
    ftp_vevo_port = 21
    ftp_vevo_vevo_user = "TESTVEVO"
    
    testdata = testData.create("shared", "ftp_login_details.tsv")
    dataFile = open(testdata, "w")
    dataFile.write("ftp_vevo_host\tftp_vevo_user\tftp_vevo_password\tftp_vevo_vevo_user\n")
    dataFile.write(ftp_vevo_host + "\t" + ftp_vevo_user + "\t" 
                   + ftp_vevo_password + "\t" + 
                   ftp_vevo_vevo_user)
    dataFile.close()
    test.log("Finished writing the ftp_login_details to TSV file")
    





