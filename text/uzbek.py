from espeakng import ESpeakNG
from text.utils.cleaners import uzbek_cleaners
import re 

esng = ESpeakNG()
esng.voice = 'uz'

pattern = r"[,\?\!\:\.]"


def spliter(text: str):

    text = " ".join([tag.replace(",", " ,") if tag[-1] == "," else tag for tag in text.split()])
    text = " ".join([tag.replace(".", " .") if tag[-1] == "." else tag for tag in text.split()])
    text = " ".join([tag.replace("?", " ?") if tag[-1] == "?" else tag for tag in text.split()])
    text = " ".join([tag.replace("!", " !") if tag[-1] == "!" else tag for tag in text.split()])
    text = " ".join([tag.replace(":", " :") if tag[-1] == ":" else tag for tag in text.split()])
    
    return text.split()


# main ipa for uzb
def uzbek_to_ipa2(text):
    
    text = uzbek_cleaners(text=text)
    text = text.replace("j", "jj") 
    text = text.replace("g‘", "gg")
    text = text.replace("o‘", "vvv")
    splited_text = spliter(text)
    g2p_text = " ".join([esng.g2p(tag, ipa=2) if tag not in ",!?:." else tag for tag in splited_text])

    text = g2p_text.replace("jj", "ʥ")   
    text = text.replace("ɡɡ", "ʁ")   
    text = text.replace("sh", "ʃ")  
    text = text.replace("vvv", "ɔʔ") 

    # extra replace

    text = text.replace("ɔʔ", "1")
    text = text.replace("t͡ʃ", "2")
    text = [
        key.replace("1", "ɔʔ") if key == "1" 
        else key.replace("2", "t͡ʃ") if key == "2" 
        else key for key in  text
        ]
    return text
