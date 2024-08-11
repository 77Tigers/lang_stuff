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
text_to_translate = """爱着你 也爱着我
这是一种折磨 这是一种折磨

今夜无数的街灯 沿路陪着我
却把我孤独的裂缝 照得更寂寞
如果这是一个梦 注定没结果
那就让它是个梦 醒来就解脱

是否月光太煽情 让我突然变得感性
孤掌难鸣 我孤身却难以安静
睁开眼睛 我们的路无法看清
想闭上眼睛 把一切暂停

当我的世界出现了你 出现了你
我看着自己变得透明 变得透明
怪我对你太执迷
让我变得不像自己

在想念你的寂寞夜里 寂寞夜里
我想把自己变得透明 变得透明
想把你忘得干净
我的心却被你占领

感觉我遇上你 就像绵羊遇上狮子
我徘徊在爱你 还是爱自己的十字
在应该赤裸的时候戴着面具
我对你说的是我听不明白的言语

你是太阳 我的星光 显得多黯淡
你是海洋 你的轻狂 我无从反抗
我越来越擅长 对自己说谎
我想要你的绽放 就把我埋葬

当我的世界出现了你 出现了你
我看着自己变得透明 变得透明
怪我对你太执迷
让我变得不像自己

在想念你的寂寞夜里 寂寞夜里
我想把自己变得透明 变得透明
想把你忘得干净
我的心却被你占领

爱着你 也爱着我
这是一种折磨 这是一种折磨
难道爱着你 就要忘了我
这是一种折磨 这是一种折磨

当我的世界出现了你 出现了你
我看着自己变得透明 变得透明
怪我对你太执迷
让我变得不像自己

在想念你的寂寞夜里 寂寞夜里
我想把自己变得透明 变得透明
想把你忘得干净
我的心却被你占领

爱着你 这是一种折磨 折磨"""

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
