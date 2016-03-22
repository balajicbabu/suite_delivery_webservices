import test

def main():
    
    test.log("Test Case Name: tst_get_deliveries_list_for_ui")

    test.log("get deliveries list for UI")
    
    #not using "STARTED" stage anymore
    get_all_deliveries_list_using_post = {
    "serviceOriginName": "test",
    "callBackEndPoint": None,
    "callBackReferenceId": None,
    "requestTime": None,
    "queryParams": {
    "page": "1", # per number
    "perPage": "20", # Maximum 20 per page
    "from": "1970-01-01",
    "to": None, # should be null to get the most recent created delivery
    "sortPropertyName":"created", # sorting by most recently created
    "sortAscending":False
    },
    "assetUuids": None,
    "campaignIds": None,
    "deliveryStages": [
    "CREATED", "SUBMITTED", "IN_PROGRESS",
    "WAITING_ON_CONFIRMATION", "COMPLETE", "FAILED", "CANCELLED",
    "RESTARTED"
    ]
    }
    data = testData.dataset("s_list_of_webservices.tsv")[0]

    get_delivery_status_list_post_url = testData.field(data, "get_delivery_status_list_post_url")

    
    source(findFile("scripts", "deliverywebservices.py"))
    
    '''GET THE LIST OF DELIVERY CARDS TO BE DISPLAYED ON GUI'''
    get_delivery_status_list_post(get_delivery_status_list_post_url, get_all_deliveries_list_using_post)

