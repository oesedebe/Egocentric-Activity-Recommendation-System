import re

# activity group filter keywords
activity_groups = {
    "Food & Drink": [
        "restaurant",
        "cafe",
        "coffee shop",
        "bakery",
        "bar",
        "brewery",
        "ice cream shop",
        "deli"
    ],

    "Arts & Culture": [
        "museum",
        "art gallery",
        "movie theater",
        "performing arts theater",
        "historical landmark",
        "historical society",
        "cultural center",
        "theater company"
    ],

    "Outdoor & Nature": [
        "park",
        "beach",
        "botanical garden",
        "community garden",
        "nature preserve",
        "hiking area",
        "trail"
    ],

    "Sports & Recreation": [
        "swimming pool",
        "tennis court",
        "golf course",
        "golf club",
        "skating rink",
        "sports complex"
    ],

    "Games & Recreation": [
        "bowling alley",
        "escape room center",
        "arcade",
        "video arcade",
        "amusement park",
        "amusement center",
        "playground",
        "recreation center"
    ],

    "Nightlife & Live Entertainment": [
        "night club",
        "live music venue",
        "music venue",
        "concert hall",
        "comedy club",
        "dance club"
    ],

    "Sightseeing & Attractions": [
        "tourist attraction",
        "scenic spot",
        "observation deck",
        "monument"
    ]
}

exclusions = [
    # for fitness (remove just gyms)
    "gym",
    "fitness center",
    "boxing gym",
    "gymnastics center",

    # RV camping (false pos)
    "rv park",
    "recreational vehicle park",

    # shopping
    "store",
    "shop",
    "shopping mall",
    "supermarket",
    "grocery store",

    # services
    "repair",
    "contractor",
    "supplier",
    "wholesaler",
    "dealer",
    "parking",
    "office",
    "coworking",
    "business center",
    "conference center",
    "warehouse",
    "storage",

    # "venues and weddings (false pos)"
    "wedding venue",
    "banquet hall"
]

# checks for a matching keyword between local label and our keywords

def matches_keyword(text, keyword):
    text = text.lower()
    keyword = keyword.lower()

    pattern = r"\b" + re.escape(keyword) + r"\b"

    return re.search(pattern, text) is not None

# checks for excluded words
def has_exclusion(categories):

    if not isinstance(categories, list):
        return False

    for category in categories:
        for term in exclusions:
            if matches_keyword(category, term):
                return True

    return False


def get_activity_groups(categories):

    if not isinstance(categories, list):
        return []

    matched_groups = []

    for group, keywords in activity_groups.items():

        for category in categories:

            if any(
                matches_keyword(category, keyword)
                for keyword in keywords
            ):
                matched_groups.append(group)
                break

    return matched_groups

# confidence level is determined by how many of the place's keywords match with our list 
def get_confidence(categories):

    if not is_activity(categories):
        return "Not activity"

    match_count = 0

    for category in categories:
        matched = False

        for keywords in activity_groups.values():
            if any(
                matches_keyword(category, keyword)
                for keyword in keywords
            ):
                matched = True
                break

        if matched:
            match_count += 1
    # high confidence if 2 or more keywords matches
    if match_count >= 2:
        return "High"
    # medium confidence if at least 1 keyword matches 
    elif match_count == 1:
        return "Medium"
    # low confidence if no matches, but passed filter
    else:
        return "Low"

def is_activity(categories):

    if not isinstance(categories, list):
        return False

    if has_exclusion(categories):
        return False


    return len(get_activity_groups(categories)) > 0



activity_metadata_v3 = metadata[
    metadata["is_activity_v3"]
].copy()

activity_metadata_v3[
    [
        "name",
        "category",
        "activity_groups_v3",
        "confidence_v3"
    ]
].head(30)
