import pickle
import converter
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

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
]

# TODO: cache the data in a single file for ease of access
if __name__ == "__main__":
    tokens = {}
    for song in song_options:
        with open(f'songs/{song}/chunks.pkl', 'rb') as f:
            song_data = pickle.load(f)
        for (line, meaning) in song_data:
                for chunk in line:
                    if chunk[1] not in tokens:
                        tokens[chunk[1]] = 1
                    else:
                        tokens[chunk[1]] += 1
    frequency_pairs = [(tokens[token], token) for token in tokens if token not in converter.CORE]
    frequency_pairs.sort(key=lambda x: x[0], reverse=True)
    #for pair in frequency_pairs:
    #    print(f"{pair[1]}: {pair[0]}")
    # plot a barchart
    frequency_pairs_cut = frequency_pairs[:30]
    plt.bar([pair[1] for pair in frequency_pairs_cut], [pair[0] for pair in frequency_pairs_cut])
    # set y axis to integers only
    plt.yticks(np.arange(0, max([pair[0] for pair in frequency_pairs_cut]), 5))
    plt.show()


