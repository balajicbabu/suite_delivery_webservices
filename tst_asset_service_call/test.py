import test

def main():
    
    test.log("Test Case Name: tst_asset_service_call")
    data = testData.dataset("s_list_of_webservices.tsv")[0]

    source(findFile("scripts", "test_create_restart_remove.py"))
    
    asset_service_to_get_list_of_mediafamilies_url = testData.field(data, "asset_service_to_get_list_of_mediafamilies_url")
    asset_service_to_get_list_of_assets_url = testData.field(data, "asset_service_to_get_list_of_assets_url")
    campaign_id_data = testData.field(data, "campaign_id")
    
    source(findFile("scripts", "assetservicecall.py"))
    
    media_family_id = get_list_of_media_families(asset_service_to_get_list_of_mediafamilies_url, campaign_id_data)
    get_list_of_assets(asset_service_to_get_list_of_assets_url, media_family_id)