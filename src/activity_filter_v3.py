import re

# broad activity group filter keywords
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

# exclusion rules to disqualify places 
exclusions = [
    "gym",
    "fitness center",
    "boxing gym",
    "gymnastics center",
    "rv park",
    "recreational vehicle park",
    "store",
    "shop",
    "shopping mall",
    "supermarket",
    "grocery store",
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
    "wedding venue",
    "banquet hall"
]

# return true if a keyword appears 
def matches_keyword(text, keyword):
    text = text.lower()
    keyword = keyword.lower()

    pattern = r"\b" + re.escape(keyword) + r"\b"

    return re.search(pattern, text) is not None

# return true if an exclusion term is found
def has_exclusion(categories):

    if not isinstance(categories, list):
        return False

    for category in categories:
        for term in exclusions:
            if matches_keyword(category, term):
                return True

    return False

# returns all broad groups that matched keywords
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

# counts the number of categories of a place that matched a keyword 
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

    if match_count >= 2:
        return "High"

    elif match_count == 1:
        return "Medium"
 
    else:
        return "Low"

# checks if a place is an activity, returns True/False 
def is_activity(categories):

    if not isinstance(categories, list):
        return False

    if has_exclusion(categories):
        return False


    return len(get_activity_groups(categories)) > 0
