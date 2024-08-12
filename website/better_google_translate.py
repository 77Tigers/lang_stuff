import time
import os
import requests
from pypinyin import pinyin, Style

# google translate

def translate_text(text):
    if text.strip() == "":
        return " "
    #print("translating: " + text)
    # Args:
    #    text (str): Text to translate.
    #    target_language (str): Language code to translate the text into (e.g., 'es' for Spanish).

    # Returns:
    #    str: Translated text.
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "zh-CN",  # Source language (auto-detect)
        "tl": "en",  # Target language
        "dt": "t",
        "q": text
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

    translated_text = response.json()[0][0][0]
    time.sleep(0.3)
    #print(translated_text)
    return translated_text

# Example usage:
text_to_translate = """我们一同追着心中的梦想
我们试着把
太阳放在手掌
我们彼此笑着岁月的无常
也坚定的做着彼此的那束光

记不得曾跨越过多少风和浪
做你的船桨你是我的翅膀
我们记得对方
青涩的模样
满是骄傲的脸庞
是光融不掉的冰花窗

是你 是你
身后的青春都是你
绘成了我的山川流溪
为我下一场倾盆大雨
淋掉泥泞
把真的自己叫醒

是你 是你
种下满是勇气森林
把披风上的荒寂抹去
让我变成会飞行的鱼
跳出海域
去触摸奇迹

我们一同追着心中的梦想
我们试着把
太阳放在手掌
我们彼此笑着岁月的无常
也坚定的做着彼此的那束光

记不得曾跨越过多少风和浪
做你的船桨你是我的翅膀
我们记得对方
青涩的模样
满是骄傲的脸庞
是光融不掉的冰花窗

是你 是你
身后的青春都是你
绘成了我的山川流溪
为我下一场倾盆大雨
淋掉泥泞
把真的自己叫醒

是你 是你
种下满是勇气森林
把披风上的荒寂抹去
让我变成会飞行的鱼
跳出海域
去触摸奇迹

是你 是你
身后的青春都是你
绘成了我的山川流溪
为我下一场倾盆大雨
淋掉泥泞
把真的自己叫醒

是你 是你
种下满是勇气森林
把披风上的荒寂抹去
让我变成会飞行的鱼
跳出海域
去触摸奇迹"""

def get_pinyin(chinese_text):
    """
    Convert Chinese text to pinyin.

    Args:
        chinese_text (str): Chinese text to convert.

    Returns:
        str: Text in pinyin.
    """
    pinyin_list = pinyin(chinese_text, style=Style.TONE)  # Use TONE3 style to include tone numbers
    pinyin_text = ' '.join(item[0] for item in pinyin_list)
    return pinyin_text

# Example usage:
"""
chinese_text = "你好，世界！"  # "Hello, world!" in Chinese
pinyin_text = get_pinyin(chinese_text)
print(pinyin_text)"""

if __name__ == "__main__":
    for line in text_to_translate.split("\n"):
        try:
            translated_text = translate_text(line)
            pinyin_str = get_pinyin(line)
            print(pinyin_str)
            print(" ".join(list(line.strip())))
            print(translated_text.strip())
            print()
        except:
            print()
