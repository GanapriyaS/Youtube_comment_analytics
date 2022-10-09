from googletrans import Translator
translator = Translator()

# text = 'seekiram sollu'
# text = 'na sanda podum pothum nee alaga irukinga'
# text = 'video massunga epidi shot pannuringa'
text = 'enga vitulayum same samayal tha'
# Detecting the language
print(translator.detect(text))
print(translator.translate(text).text)