import json
import pickle
from lib import *
import converter
import better_google_translate

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

# single characters (frequency and meaning)
single_chars = {}
with open("single_chars.txt", "r", encoding="utf8") as f:
    for line in f:
        line = line.strip().split("\t")
        if len(line) != 6:
            l = line[1]
            # if hanzidentifier.is_simplified(l):
            #     print(line[1] + f" ({line[0]})", end=" ")
            continue
        rank, char, occurences, cum_prob, pinyin, meaning = line
        if hanzidentifier.is_simplified(char):
            single_chars[char] = (pinyin, meaning, cum_prob)

# definitions back side of card
def get_defs(word):
    back_side = ""
    found_single = False
    if word in single_chars:
        back_side += "\n" + single_chars[word][1]
        found_single = True

    lookup_results = converter.d.lookup(word)
    lookup_successful = lookup_results is not None
    if lookup_results is not None:
        defs = lookup_results.definition_entries
        for definition in defs:
            back_side += "\n" + definition.pinyin + " " + ";".join(definition.definitions)
    
    return back_side, found_single, lookup_successful

# TODO: cache the data in a single file for ease of access
if __name__ == "__main__":
    # FREQUENCIES
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
    frequency_pairs = [(tokens[token], token) for token in tokens if token not in converter.CORE and not is_roman(token)]
    frequency_pairs.sort(key=lambda x: x[0], reverse=True)

    # # frequency plot
    # frequency_pairs_cut = frequency_pairs[30:60]
    # plt.bar([pair[1] for pair in frequency_pairs_cut], [pair[0] for pair in frequency_pairs_cut])
    # # set y axis to integers only
    # plt.yticks(np.arange(0, max([pair[0] for pair in frequency_pairs_cut]), 5))
    # plt.show()

    # create a list of suggestions that the flashcards will go through one by one (sorted by a custom metric)
    suggestions = []
    for token in frequency_pairs:
        word = token[1]
        back_side = better_google_translate.get_pinyin(word)

        to_add, found_single, lookup_successful = get_defs(word)
        back_side += to_add
        
        # set score to freuqency of the word
        word_score = token[0]
        match len(word):
            case 1:
                word_score = 5 + (100 - float(single_chars[word][2])) if found_single else 0
            case n:
                scores = [
                    10 + (100 - float(single_chars[c][2])) if c in single_chars else 0.001
                    for c in word
                ]
                word_score = np.prod(scores) ** (1 / len(scores))
                if not lookup_successful:
                    word_score -= 20

        suggestions.append((word, back_side, word_score))
    
    # sort by score (higher is better)
    suggestions.sort(key=lambda x: x[2], reverse=True)
    # filter suggestions by score > 1
    suggestions = [s for s in suggestions if s[2] > 1]

    # TODO: add most popular word in ana

    # load learning_state.json from file
    learning_state = {}
    try:
        with open("learning_state.json", "r") as f:
            learning_state = json.load(f)
    except Exception as e:
        learning_state = {
            "card_deck": []
        }
    
    # add suggestions to learning_state
    learning_state["card_deck"] = [(s[0], s[1]) for s in suggestions]

    # save learning_state.json to file
    with open("learning_state.json", "w") as f:
        json.dump(learning_state, f)
