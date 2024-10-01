import hanzidentifier

# Define available song options
song_options = [
    "Selfless",
    "legend_star_him",
    "river_of_oblivion",
    "forward_snow_you",
    "why_not_love",
    "should_all_have_dream",
    "whale",
    "wipe_tear_gentle",
    "within_reach",
    "milky_moon",
    "snow_heart",
    "gang_hao",
    "full_stop",
    "explore_world_camel",
    "simple_beautiful_world",
    "make_own_moon",
    "everything_best_plan",
    "colours",
    "evening_breeze_elf",
    "hot_coffee",
    "rehearse_mirror_rose",
    "passengers",
    "meet_current_you",
    "invisible_puzzle",
]

# checks if word uses roman characters
def is_roman(word):
    accepted_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
    return all([c in accepted_chars for c in word])