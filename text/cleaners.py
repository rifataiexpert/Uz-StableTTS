import re

from text.mandarin import chinese_to_cnm3
from text.japanese import japanese_to_ipa2
from text.uzbek import uzbek_to_ipa2

language_module_map = {"PAD":0, "ZH": 1, "UZ": 2, "JA": 3}

# 预编译正则表达式
ZH_PATTERN = re.compile(r'[\u3400-\u4DBF\u4e00-\u9FFF\uF900-\uFAFF\u3000-\u303F]')
JP_PATTERN = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u31F0-\u31FF\uFF00-\uFFEF\u3000-\u303F]')
UZ_PATTERN = re.compile(r'[a-zA-Z.,!?\'"(){}[\]<>:;@#$%^&*-_+=/\\|~`]+')

CLEANER_PATTERN = re.compile(r'\[(ZH|JA|UZ)\]')

def detect_language(text: str, prev_lang=None):

    if ZH_PATTERN.search(text): return 'ZH'
    if JP_PATTERN.search(text): return 'JA'
    if UZ_PATTERN.search(text): return 'UZ'

    if text.isspace(): return prev_lang  # 若是空格，则返回前一个语言
    return None

# auto detect language using re
def cjke_cleaners4(text: str):

    text = CLEANER_PATTERN.sub('', text)
    pointer = 0
    output = ''
    current_language = detect_language(text[pointer])
    
    while pointer < len(text):
        temp_text = ''
        while pointer < len(text) and detect_language(text[pointer], current_language) == current_language:
            temp_text += text[pointer]
            pointer += 1
        if current_language == 'ZH':
            output += chinese_to_cnm3(temp_text)
        elif current_language == 'JA':
            output += japanese_to_ipa2(temp_text)
        elif current_language == 'UZ':
            output += uzbek_to_ipa2(temp_text)
        if pointer < len(text):
            current_language = detect_language(text[pointer])

    output = re.sub(r'\s+$', '', output)
    output = re.sub(r'([^\.,!\?\-…~])$', r'\1.', output)
    return output

