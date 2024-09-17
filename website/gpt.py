from openai import OpenAI
from dotenv import load_dotenv
import os
import analysis

# Load the .env file
load_dotenv()

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

# eg: text = "这|是|一|种|折磨| |这|是|一|种|折磨"

def translate_word_in_context(context, word, translation):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a translator from chinese to english."},
            {"role": "user", "content": 
                #"Translate only the word between *s. Give the ENGLISH only, with no *s. Never give chinese. Translate the word IN CONTEXT. No more than 4 words.\n" + text}
                "Translate the word on the next line. Context is on the line after. Give the english ONLY, with no *s. If there are multiple meanings, give the one that fits the first line best. Translate the sentence, choose an answer, explain your reasoning and then put the answer (must be English) on the last line on its own." +
                "\nHere is the word: " + word +
                "\nHere is the context for the sentence: " + context +
                "\nHere is the translation of the sentence: " + translation +
                "\nHere is the (long) list of possible meanings, etc:" + analysis.get_defs(word)[0]
                
            }
        ],
        temperature = 0.0,
        top_p = 0.1
    )
    print("==========")
    temp = completion.choices[0].message.content.lower().replace(word, "").strip() # to be printed for logs
    ans = temp.split("\n")[-1].split(":")[-1].strip()
    print("sentence: " + context)
    print("GPT call: " + temp)

    if len(ans) > 15:
        print("RETRYING!!!!!")
        completion = client.chat.completions.create(
            model="gpt-4o-mini", # + ("-mini" if test else ""),
            messages=[
                {"role": "system", "content": "summarise briefly"},
                {"role": "user", "content": 
                    #"Translate only the word between *s. Give the ENGLISH only, with no *s. Never give chinese. Translate the word IN CONTEXT. No more than 4 words.\n" + text}
                    f"Write the (english) translation of the given word (${word}) that was decided upon (do NOT give a sentence) and nothing else. Your output should be a word. Do not include the translation of the sentence, or phrases like 'to' in verbs. Do not include commas or semicolons. Here is your previous output (with too many words):\n" + temp
                }
            ],
            temperature = 0.0,
            top_p = 0.1
        )
        temp = completion.choices[0].message.content.lower().replace(word, "").strip() # to be printed for logs
        ans = temp.split("\n")[-1].split(":")[-1].strip()
        print("NEW ANS: " + ans)

    # remove full stop
    ans = ans.removesuffix(".")

    return ans