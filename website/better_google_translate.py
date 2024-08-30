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
text_to_translate = """橘色是牵着你的手心
红色是你留下的唇印
绿色是陪你看的风景
黄色是陪你数的星星
灰色是你离开的背影
蓝色是他从此的心情
黑色是你沉默的回应
白色是他世界的伶仃
查克靠近 一再靠近
却看不清从前熟悉的表情
你的倒影 如此的清晰
他却只看到亲密的光线和影
曾经浪漫是随便一间餐厅
感动是并着肩的安静
回忆是夜空里闪烁的流星
现实是当它殒落大地
查克靠近 一再靠近
你的美丽只是线条的分明
一句到底 爱情的距离
是心若远了 轮廓再也看不清
你让我看到
光伴随的阴影
笑锐化的哭泣
爱与恨的接近
梦和现实的分明
我终于睁开眼睛"""

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
