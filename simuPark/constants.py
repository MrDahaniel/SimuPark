ARCHETYPES = {
    "Tourist": {
        "AttractionPercentage": 0.6,
        "MinStayTime": 4 * 60,
        "MaxStayTime": 8 * 60,
        "MaxWaitTime": 60,
        "MinWaitTime": 60,
    },
    "Average": {
        "AttractionPercentage": 0.5,
        "MinStayTime": 4 * 60,
        "MaxStayTime": 8 * 60,
        "MaxWaitTime": 50,
        "MinWaitTime": 50,
    },
    "Activity Enjoyer": {
        "AttractionPercentage": 0.2666667,
        "MinStayTime": 1 * 60,
        "MaxStayTime": 5 * 60,
        "MaxWaitTime": 10,
        "MinWaitTime": 10,
    },
    "Attraction Enjoyer": {
        "AttractionPercentage": 0.7407407,
        "MinStayTime": 4 * 60,
        "MaxStayTime": 9 * 60,
        "MaxWaitTime": 70,
        "MinWaitTime": 70,
    },
    "All Day Park": {
        "AttractionPercentage": 0.6,
        "MinStayTime": 8 * 60,
        "MaxStayTime": 12 * 60,
        "MaxWaitTime": 40,
        "MinWaitTime": 40,
    },
    "Relaxed Visitor": {
        "AttractionPercentage": 0.4,
        "MinStayTime": 3 * 60,
        "MaxStayTime": 6 * 60,
        "MaxWaitTime": 25,
        "MinWaitTime": 25,
    },
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
    "DINOSAUR": {
        "Duration": 4,
        "Popularity": 33 * 1800,
        "ServiceRate": 1800,
    },
    "Expedition Everest": {
        "Duration": 4,
        "Popularity": 26 * 1800,
        "ServiceRate": 1800,
    },
    "Flight of Passage": {
        "Duration": 6,
        "Popularity": 98 * 1280,
        "ServiceRate": 1280,
    },
    "Kali River Rapids": {
        "Duration": 10,
        "Popularity": 29 * 1800,
        "ServiceRate": 1800,
    },
    "Kilimanjaro Safaris": {
        "Duration": 20,
        "Popularity": 48 * 3000,
        "ServiceRate": 3000,
    },
    "Na'vi River Journey": {
        "Duration": 5,
        "Popularity": 70 * 1080,
        "ServiceRate": 1080,
    },
    "TriceraTop Spin": {
        "Duration": 2,
        "Popularity": 15 * 800,
        "ServiceRate": 800,
    },
}
