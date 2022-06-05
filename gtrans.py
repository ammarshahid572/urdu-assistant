from googletrans import Translator, constants
from pprint import pprint

translator= Translator()

def utranslation(utext):
    translation = translator.translate(utext)
    return translation.text
if __name__=='__main__':
    print(utranslation("Sab theek hai"))
