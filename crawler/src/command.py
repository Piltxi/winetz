def development (): 
    params = {

        "wine_type_ids[]": ["1", "2"],
        "country_codes[]":"it",

        "min_rating" : "4.2",
        "price_range_max": "9",
        } 

    languageList = ["it", "en"]

    return params, languageList

def production (): 
    params = {

        "wine_type_ids[]": ["1", "2", "3", "4", "7", "24"],
        "country_codes[]": ["it", "fr"],

        "min_rating" : "4.0",
        "price_range_max": "150",
        } 

    languageList = ["it", "fr", "de", "en"]

    return params, languageList