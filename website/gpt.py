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

default = """爱/love|着/ing|你/you| |也/also|爱/love|着/ing|我/I
这/this|是/is|一/a|种/sort|折磨/torture| |这/this|是/is|一/a|种/sort|折磨/torture

今夜/tonight|无数/countless|的/’s|街灯/streetlights| |沿/along|路/road|陪/with|着/ing|我/I
却/but|把/put|我/I|孤独/lonely|的/’s|裂缝/crack| |照/shine|得/make|更/more|寂寞/lonely
如果/if|这/this|是/is|一个/a|梦/dream| |注定/destined|没/no|结果/result
那/then|就/just|让/make|它/it|是/is|个/a|梦/dream| |醒来/wake|就/just|解脱/release

是否/whether|月光/moonlight|太/too|煽情/sentimental| |让/make|我/I|突然/suddenly|变/get|得/get|感性/sensitive
孤掌难鸣/alone| |我/I|孤身/alone|却/but|难以/hard|安静/quiet
睁/open|开/open|眼睛/eyes| |我们/we|的/’s|路/road|无法/cannot|看/see|清/clear
想/think|闭/close|上/up|眼睛/eyes| |把/put|一切/everything|暂停/pause

当/when|我/I|的/’s|世界/world|出现/appear|了/了|你/you| |出现/appear|了/了|你/you
我/I|看/look|着/ing|自己/self|变/get|得/get|透明/transparent| |变/get|得/get|透明/transparent
怪/blame|我/I|对/to|你/you|太/too|执迷/obsessed
让/make|我/I|变/get|得/get|不/not|像/like|自己/self

在/in|想念/miss|你/you|的/’s|寂寞/lonely|夜里/night| |寂寞/lonely|夜里/night
我/I|想/think|把/put|自己/self|变/get|得/get|透明/transparent| |变/get|得/get|透明/transparent
想/think|把/put|你/you|忘/forget|得/get|干净/clean
我/I|的/’s|心/heart|却/but|被/be|你/you|占领/occupied
爱/love|着/ing|你/you"""

def translate_word_in_context(text, test=True):
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # + ("-mini" if test else ""),
        messages=[
            {"role": "system", "content": "You are a translator and give no explanations and get straight to the point."},
            {"role": "user", "content": 
             "Translate only the word between *s. Give the ENGLISH only, with no *s. Never give chinese. Translate the word IN CONTEXT. No more than 4 words.\n" + text}
        ],
        temperature = 0.0,
        top_p = 0.1
    )
    ans = completion.choices[0].message.content.lower()
    print("sentence: " + text)
    print("GPT call: " + ans)
    return ans