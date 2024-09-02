# the aim of this file is to convert the song lyrics into a chunk-based format to be displayed on the website
from better_google_translate import get_pinyin, translate_text
import gpt
from chinese_english_lookup import Dictionary
from lib import is_roman

import pynlpir
import pickle

# go to files and set encoding = utf-8, or it won't work
d = Dictionary()

CORE = []
with open("core.txt", encoding="utf8") as f:
    CORE = f.read().split("\n")

def add_to_core(word):
    if word not in CORE:
        with open("core.txt", "a", encoding="utf8") as f:
            f.write("\n" + word)
        CORE.append(word)

def get_words(line):
    #kw_extractor = Chinese_Extractor()
    #return kw_extractor.generate_keywords(line, top_k=5, rank_methods="mmr")
    pynlpir.open()
    words = pynlpir.segment(line, pos_tagging=False)
    pynlpir.close()
    return words


def translate_word(word, context, translation):
    # Translate the word to English
    if word in CORE or is_roman(word):
        return ""
    #ans = d.lookup(word)
    #if ans != None and ans:
    if is_roman(word):
        return ""
    return gpt.translate_word_in_context(context, word, translation=translation)

def convert_song_to_chunks(song_lyrics):
    """
    Convert song lyrics to chunks.

    Args:
        song_lyrics (str): Song lyrics to convert.

    Returns:
        list: List of lists of tuples, where each tuple contains the pinyin, Chinese character, and English translation.
    """
    # Split the song lyrics into lines [not used atm]
    lines = song_lyrics #song_lyrics.split('\n')

    # Initialize the list of chunks
    chunks = []

    line_cache = {}

    # Iterate over each line in the song lyrics
    for line in lines:
        line = line.strip()
        if line in line_cache:
            chunks.append(line_cache[line])
            continue

        # Split the line into words
        words = get_words(line)

        # Initialize the list of tuples for the current line
        line_data = []

        #line_pinyin = get_pinyin(line).strip().split(" ")

        line_translation = translate_text(line)

        # Iterate over each word in the line
        for i, word in enumerate(words):
            # Get the pinyin, Chinese character, and English translation for the word
            pinyin = get_pinyin(word) if not is_roman(word) else ""
            # in context trick
            #translation = translate_word(f"{line.strip()}...'{word}' 意味着")
            # translation = translate_word(word)
            # translation = translation.split("'")
            # if len(translation) > 1:
            #     translation = translation[-2].tolower()
            # else:
            #     translation = ""

            translation = translate_word(
                word,
                context=" ".join(words[:i]) + f" *{word}* " + " ".join(words[i+1:]),
                translation=line_translation
            )

            # Append the tuple to the line data
            line_data.append((pinyin, word, translation))

        # Append the line data to the list of chunks
        line_cache[line] = (line_data, line_translation)
        chunks.append((line_data, line_translation))

    return chunks

    # #gpt
    # translated = gpt.translate_words_in_context(gpt_promt[:-1], test=False) # remove trailing newline
    # translated = [line for line in translated.split("\n")]

    # new_chunks = []
    # for i, line in enumerate(chunks):
    #     new_line = []
    #     gpt_line = translated[i].split("|")
    #     if len(gpt_line) != len(line):
    #         print(f"gpt: {gpt_line}\n line: {line}")
    #         for j, word in enumerate(line):
    #             new_line.append((word[0], word[1], translate_word(word[1])))
    #     else:
    #         for j, word in enumerate(line):
    #             print(gpt_line[j])
    #             new_line.append((word[0], word[1], gpt_line[j].split("/")[1]))
    #     new_chunks.append(new_line)

    # return new_chunks

x = None
if __name__ == "__main__":
    song = "passengers"
    with open(f'songs/{song}/lyrics.txt', encoding="utf8") as r:
        inp = r.readlines()
        x = convert_song_to_chunks(inp)
        # pickle x
        with open(f'songs/{song}/chunks.pkl', 'wb') as f:
            pickle.dump(x, f)
