from ibm_watson import LanguageTranslatorV3, ApiException
import json
import random

# language_translator = LanguageTranslatorV3(
#         version='2018-05-01',
#         iam_apikey="kxVepEKiI2lVF-pv8jxWiSOjDjI_WHslsFxUquukERnK",
#         url="https://gateway-wdc.watsonplatform.net/language-translator/api"
#     )

def translate(tweet, translator, model):
    translation = translator.translate(
        text=tweet,
        model_id=model).get_result()
    return translation['translations'][0]['translation']

def translate_random(tweet):
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        iam_apikey="kxVepEKiI2lVF-pv8jxWiSOjDjI_WHslsFxUquukERnK",
        url="https://gateway-wdc.watsonplatform.net/language-translator/api"
    )

    # Sequence of languages translatable to and from english 
    languages = ['he', 'ar', 'fr', 'es', 'hi', 'hr', 'el', 'hu', 'ja' ]
    random.shuffle(languages)

    # This is the en-lang, lang-en loop per language 
    for i in range(len(languages)-1):
        print(f'Translating through {languages[i]}...')
        model = f'en-{languages[i]}'
        tweet = translate(tweet, language_translator, model)
        model = f'{languages[i]}-en'
        tweet = translate(tweet, language_translator, model)
    
    return tweet

def translate_sequence(tweet):

    # Sequence of directly translatable languages 
    languages = ['it', 'de', 'fr', 'es']

    # This is the simple sequential translation loop 
    languages = ['en'] + languages + ['en'] 
    for i in range(len(languages)-1):
        model = f'{languages[i]}-{languages[i+1]}'
        print(f'model={model}')
        tweet = translate(tweet, language_translator, model)
    
    return tweet

def print_models(translator):
    # Code to print available translation models
    models = translator.list_models().get_result()
    for model in models['models']:
        print(model['model_id'])

def print_languages(translator):
    # Code to print identifiable languages
    languages = translator.list_identifiable_languages().get_result()
    for lang in languages['languages']:
        print(f"{lang['language']} - {lang['name']}")

if __name__ == "__main__":
    # Test tweet
    test_string = "Today I will be visiting Des Moines, Iowa. Come by and say hi!"

    try:
        # Invoke a Language Translator method
        translate_sequence(test_string)
    except ApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
