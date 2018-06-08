from django.shortcuts import render
from .braille_translators import alphaToBraille, brailleToAlpha

def braille_viewer(request):
    text = "This is how they see the world."
    text_braille = alphaToBraille.translate(text)
    print(text_braille)
    braille_text = brailleToAlpha.retranslate(text_braille)
    print(braille_text)
    num = len(text_braille)
    return render(request, 'index.html',
                  {'range': range(num), 'text': braille_text, 'text_braille': text_braille})

# Powered by Braille-Translator(https://github.com/LazoCoder/Braille-Translator)
