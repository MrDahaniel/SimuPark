ARCHETYPES = {
    "Tourist": {
        "AttractionPercentage": 0.6,
        "MinStayTime": 5 * 60,
        "MaxStayTime": 10 * 60,
        "MaxWaitTime": 120,
        "MinWaitTime": 30,
    }
}

ACTIVITIES = {
    "Walk15": {"Duration": 15, "Popularity": 5},
    "Walk10": {"Duration": 10, "Popularity": 5},
    "ShopGifts": {"Duration": 30, "Popularity": 5},
    "EatRestaurant": {"Duration": 50, "Popularity": 5},
    "BathroomBreak": {"Duration": 5, "Popularity": 5},
    "TakePictures": {"Duration": 15, "Popularity": 5},
}

ATTRACTIONS = {
    "Dropper": {"Duration": 2, "Popularity": 6, "ServiceRate": 1100},
    "Tornado": {"Duration": 3, "Popularity": 7, "ServiceRate": 1300},
    "BumpCars": {"Duration": 5, "Popularity": 4, "ServiceRate": 1000},
    "SlowRiver": {"Duration": 5, "Popularity": 3, "ServiceRate": 800},
    "StarWarsRide": {"Duration": 3, "Popularity": 6, "ServiceRate": 900},
    "SpaceMountain": {"Duration": 3, "Popularity": 8, "ServiceRate": 1200},
}
