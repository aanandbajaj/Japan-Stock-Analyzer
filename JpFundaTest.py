import requests
from googletrans import Translator

# Replace with your actual API key
api_key = "190071e01e2aa3a43185aa83f348d80d8f3e524a"

# URL for the API call
url = "https://www.jp-funda.com/api/jp/securities_code/list/7203"

# Set up the headers
headers = {
    "Authorization": f"Token {api_key}"
}

# Make the API request
response = requests.get(url, headers=headers)

# Print the API response content
print("Original Japanese Data:\n", response.text)

japToEnglishLookup = {}
translator = Translator()


def translate_nested_keys(obj, translator, src_lang, dest_lang):
    if isinstance(obj, dict):
        translated_obj = {}
        for key, value in obj.items():
            translated_key = translator.translate(key, src=src_lang, dest=dest_lang).text
            if isinstance(value, dict):
                translated_value = translate_nested_keys(value, translator, src_lang, dest_lang)
            else:
                translated_value = value
            translated_obj[translated_key] = translated_value
        return translated_obj
    elif isinstance(obj, list):
        translated_list = []
        for item in obj:
            translated_item = translate_nested_keys(item, translator, src_lang, dest_lang)
            translated_list.append(translated_item)
            print(translated_item)
        return translated_list
    else:
        return obj

# Check if the request was successful
if response.status_code == 200:
    data_list = response.json()
    translated_data = translate_nested_keys(data_list, translator, 'ja', 'en')
    print(translated_data)



