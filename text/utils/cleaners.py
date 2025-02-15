import re
from unidecode import unidecode
from .number_norm import normalize_numbers
from .transliterate import transliterate

_whitespace_re = re.compile(r"\s+")
_fullstop_re = re.compile(r"(\,|\.|\!|\?){2,}")
_newline_re = re.compile(r"(\\n){2,}")
_simbols_re = re.compile(r"[^A-Za-z0-9,|\.|?|\-|\‘|\s|#|@|$|*|=|+|%|/]")
_apostrophe_re = re.compile(
    r"[\‘|’|ʼ|`|´|ʹ|ʻ|ʽ|ʾ|ʿ|ˈ|ˊ|ʹ|΄|՚|᾽|᾿|‘|‛|′|‵|Ꞌ|ꞌ|＇|‘|']")
_punctuations_re = re.compile(r"[!|(|)|:|?]")
_c_symbol_re = re.compile(r"(c.)")
_main_symbol_re = re.compile(r"[#|@|$|*|=|+|%|\-|/]")
_websites_re = re.compile(r"(https://.\w+.\w+|http://.\w+.\w+|\
https://www.\w+.\w+|http://www.\w+.\w+)")
_wtf_re = re.compile(r"(\,\.)")


def expand_numbers(text):
    return normalize_numbers(text)


def lowercase(text):
    return text.lower()


def replace_punctuations(text):
    return re.sub(_punctuations_re, ". ", text)


def replace_apostrophe(text):
    return re.sub(_apostrophe_re, "‘", text)


def collapse_symbols(text):
    return re.sub(_simbols_re, "", text)


def collapse_whitespace(text):
    return re.sub(_whitespace_re, " ", text)


def collapse_fullstop(text):
    return re.sub(_fullstop_re, text[len(text)-1], text)


def collapse_newline(text):
    return re.sub(_fullstop_re, "", text)


def convert_to_ascii(text):
    return unidecode(text)


def basic_cleaners(text):
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text


def transliteration_cleaners(text):
    text = convert_to_ascii(text)
    text = lowercase(text)
    text = collapse_whitespace(text)
    return text

def replace_c(text):
    if text.group(0)[1] != "h":
        return "k"+text.group(0)[1]
    else:
        return text.group(0)


def replace_main_symbols(text):
    symbol = text.group(0)
    if symbol == "#":
        return " hashtag "
    elif symbol == "@":
        return " elektron kuchukcha "
    elif symbol == "$":
        return " dollar "
    elif symbol == "*":
        return "yulduzcha "
    elif symbol == "=":
        return " teng "
    elif symbol == "+":
        return " qo‘shuv "
    elif symbol == "%":
        return " foiz "
    elif symbol == "/":
        return " drop "
    elif symbol == "-":
        return "-"


def replace_matematical_q(text):
    symbol = text.group(0)
    if symbol[1:] == "=?":
        return symbol.replace("=?", " teng nechchi")
    else:
        return symbol.replace("=", " teng ")


def replace_website_symbols(text):
    word = text.group(0)
    if "http://" in word and "www" not in word:
        word = word.replace("http://", " echtiitiipii ikki nuqta drop drop ")
        return word.replace(".", " nuqta ")
    elif "https://" in word and "www" not in word:
        word = word.replace(
            "https://", " echtiitiipiiess ikki nuqta drop drop ")
        return word.replace(".", " nuqta ")
    elif "http://" in word and "www" in word:
        word = word.replace("http://", " echtiitiipii ikki nuqta drop drop ")
        word = word.replace("www", " uch dabllyu")
        return word.replace(".", " nuqta ")
    elif "https://" in word and "www" in word:
        word = word.replace(
            "https://", " echtiitiipiiess ikki nuqta drop drop ")
        word = word.replace("www", " uch dabllyu")
        return word.replace(".", " nuqta ")


def replace_matematical_symbols(text):
    symbol = text.group(0)
    if symbol.count("+") == 1:
        return symbol.replace("+", " qo‘shuv ")
    elif symbol.count("-") == 1 and symbol.count("=") == 1:
        return symbol.replace("-", " ayirilgan ")
    elif symbol.count("-") == 1 and symbol.count("=") == 0:
        return symbol.replace("-", " tiire ")
    elif symbol.count("*") == 1:
        return symbol.replace("*", " ko‘paytirish ")
    elif symbol.count("/") == 1:
        return symbol.replace("/", " bo‘lingan ")


def non_uzbek(text):
    return text.replace("w", "v")


allowed_characters = "‘.!?:,abcdefghijklmnopqrstuvwxyz "

def remove_disallowed_chars(text):
    text = ''.join([char for char in text if char in allowed_characters])
    return text

def uzbek_cleaners(text):
    text = transliterate(text, "latin")
    text = expand_numbers(text)
    text = replace_apostrophe(text)
    text = re.sub(_websites_re, replace_website_symbols, text)
    text = re.sub(_main_symbol_re, replace_main_symbols, text)
    text = collapse_symbols(text)
    text = lowercase(text)
    text = re.sub(_c_symbol_re, replace_c, text)
    text = collapse_whitespace(text)
    text = collapse_fullstop(text)
    text = collapse_newline(text)
    text = re.sub(_wtf_re, ". ", text)
    text = remove_disallowed_chars(text=text)

    return text
