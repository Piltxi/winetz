def development (): 
    params = {

        "wine_type_ids[]": "1", 
        "country_codes[]":"it",

        "min_rating" : "4.2",
        "price_range_max": "9",
        } 

    languageList = ["it"]

    return params, languageList

def production (): 
    params = {

        "wine_type_ids[]": "1",
        "country_codes[]":"it",

        "min_rating" : "4.2",
        "price_range_max": "150",
        } 

    languageList = ["it"]

    return params, languageList