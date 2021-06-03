# Gpyts

Gpyts is a library for Google translation and gTTS using Google Translation (API unofficially).

* Its fast, easy and has both async/sync version.
* Supports both Translation and Text to Speech.
* Option for using both api and web scrap.
* Allows multiple endpoint configurations and proxy.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Gpyts.

```bash
pip install https://github.com/Ripeey/Gpyts/archive/refs/heads/main.zip
```

## Usage Async

```python
from gpyts.asyncGpyts import Gpyts

gpyts = Gpyts()

# Using full translation api. Returns all supported parameters listed.
translation = await gpyts.translate("hey, how are you?", to_lang = 'fr')
print("Text is : " + translation.text)

# Convert Text to Speech.
speech = await gpyts.tts("Fine, What about you?", lang = 'fr', slow = True, download = 'tts.mp3')
print("Saved as :" + speech.path)
```

## Usage Sync
Simply import : 
```python
from gpyts.syncGpyts import Gpyts
```
and remove await(s), thats it!

## `Gpyts.`translate
Parameters that could be passed
* **text** - Text to be translated.
* **to_lang** - Target language code.
* **from_lang** (Optional) - Source language code.
* **i_enc** (Optional) - Input encoding.
* **o_enc** (Optional) - Output encoding.
* **web** (Optional) - To use web scrap version.

Translating any text with provided language code to be converted
```python
# Using full translation api. Returns all supported parameters listed.
translation = await gpyts.translate("hey, how are you?", to_lang = 'fr')

print("Text is : " + translation.text)
```
You can also use web scrap mini version by passing `gpyts.translate(..., web = True)`

```python
# Using web mini translation (Scrapped). Returns only translated text.
translation = await gpyts.translate("hey, how are you?", to_lang = 'fr', web = True)
print("Text is : " + translation.text)
```
Result `Translation` object may contain attributes
* **src**  - Detected source language code.
* **text** - Translated text.
* **origin** - Original text.
* **translit** - Transliteration if available.
* **alternative** - Alternative translation list.
* **confidence** - Confidence value of translation.

##  `Gpyts.`tts
Parameters that could be passed
* **text** - Text to be converted.
* **lang** - Target language code.
* **slow** - Slow down the speech speed. Default False.
* **i_enc** (Optional) - Input encoding.
* **download**(Optional) - Could be either a file path or BytesIO object. Default creates `text2speech.mp3` file.

Convert given text to speech
```python
# Same folder as default text2speech.mp3
text2speech = await gpyts.tts("hey, how are you?", lang = 'ja')
print("Saved as : " + translation.file) 

# Different folder (creates if not exists) as default text2speech.mp3
text2speech = await gpyts.tts("hey, how are you?", lang = 'ja', download = './saves/tts/')
print("Saved as : " + translation.file) 

# Custom name
text2speech = await gpyts.tts("hey, how are you?", lang = 'ja', download = './tts.mp3')
print("Saved as : " + translation.file)
```
You can also provide a `BytesIO` buffer object

```python
# Create a ByteIO buffer
from io import BytesIO
buffer = BytesIO()
text2speech = await gpyts.tts("hey, how are you?", lang = 'ja', download = buffer)

# ... Later save it
with open('text2speech.mp3', 'wb') as file:
    file.write(text2speech.file)
```
Result `TextToSpeech` object may contain attributes
* **lang** - Language to which it was converted.
* **text** - Provided original text.
* **file** - File path where it was saved or BytesIO buffer.


## License
[MIT](https://github.com/Ripeey/Gpyts/blob/main/LICENSE)
