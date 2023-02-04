from translate import Translator



abbreviations = {"chinese": "zh",
                "russian": "ru",
                "german": "de",
                "french": "fr",
                "japanese": "ja",
                "korean": "ko",
                "dutch": "nl",
                "hindi": "hi",
                "arabic": "ar",
                "tamil": "ta",
                "romanian": "ro",
                "italian": "it"}


def translate_it(lang, text):
    lang = lang.lower()
    text = text.lower()

    if lang not in abbreviations:
        return ['The language hasn\'t been added yet.', '']
    translator = Translator(to_lang=abbreviations[lang])
    translation = translator.translate(text)

    return [translation, abbreviations[lang]]
