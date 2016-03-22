import test

def main():
    
    test.log("Test Case Name: tst_campaign_service_call")
    data = testData.dataset("s_list_of_webservices.tsv")[0]

    campaign_service_call = testData.field(data, "campaign_service_call_url")
    campaign_id_data = testData.field(data, "campaign_id")

    source(findFile("scripts", "campaignservicecall.py"))

    get_campaign_service_call(campaign_service_call, campaign_id_data)
