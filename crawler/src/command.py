def development (): 
    params = {

        "wine_type_ids[]": ["1"],
        "country_codes[]":"it",

        "min_rating" : "4.2",
        "price_range_max": "9",

        } 

    languageList = ["it"]

    return params, languageList

def production (): 
    params = {

        "wine_type_ids[]": ["1", "2", "3", "4", "7", "24"],
        "country_codes[]": ["it"],

        "price_range_max": "20",
        } 

    languageList = ["it"]

    return params, languageList