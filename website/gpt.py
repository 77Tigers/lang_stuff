from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

# eg: text = "这|是|一|种|折磨| |这|是|一|种|折磨"

def translate_word_in_context(context, word, test=True):
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # + ("-mini" if test else ""),
        messages=[
            {"role": "system", "content": "You are a translator from chinese to english."},
            {"role": "user", "content": 
                #"Translate only the word between *s. Give the ENGLISH only, with no *s. Never give chinese. Translate the word IN CONTEXT. No more than 4 words.\n" + text}
                "Translate the word on the SECOND LINE only. Give the english ONLY, with no *s. If there are multiple meanings, give the one that fits the first line best. If it's a measure word, just write '~' followed by what it measures. Explain your reasoning briefly (translate the sentence) and then put the answer (English) on the last line on its own.\n" + context + "\n" + word
            }
        ],
        temperature = 0.0,
        top_p = 0.1
    )
    temp = completion.choices[0].message.content.lower().replace(word, "").strip() # to be printed for logs
    ans = temp.split("\n")[-1].split(":")[-1].strip()
    print("sentence: " + context)
    print("GPT call: " + temp)

    if len(ans) > 25:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", # + ("-mini" if test else ""),
            messages=[
                {"role": "system", "content": "summarise briefly"},
                {"role": "user", "content": 
                    #"Translate only the word between *s. Give the ENGLISH only, with no *s. Never give chinese. Translate the word IN CONTEXT. No more than 4 words.\n" + text}
                    "Write the translation decided upon and nothing else: \n" + temp
                }
            ],
            temperature = 0.0,
            top_p = 0.1
        )
        temp = completion.choices[0].message.content.lower().replace(word, "").strip() # to be printed for logs
        ans = temp.split("\n")[-1].split(":")[-1].strip()

    return ans