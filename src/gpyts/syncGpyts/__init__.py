#!/usr/bin/python3

#MIT License
#Copyright (c) 2021 Ripe

import requests, random, json, time, os, io, re
from .. import config, errors
from typing import Union, List
from .. types import Translation, TextToSpeech

class Gpyts():
	"""Gpyts is a library for Google translation and gTTS using Google Translation API.

	"""
	def __init__(self,  tld: Union[str, List[str]] = None, endpoint: Union[str, List[str]] = None, client: str = None, minimal: bool = False, labled: bool = True, proxy: str = None) -> None:
		"""Configuration for Service Url and Client.
		
		Note:
			Provide tld, endpoint, client only if you know valid combination of values.
			
			Example of tld(s):
				co.uk, tl
			Example of endpoint(s):
				translate.google.com, client0.google.com, translate.googleapis.com
			Example of client(s):
				gtx, t

			Either use `tld` or `endpoint`, it wont work together. Just `tld` is required for most part even thats optional too.
		
		Args:
			tld (str | List[str], Optional): Custom tld's you can provide like `com` or `co.uk`.
			endpoint (str | List[str], Optional): Custom endpoint url to be used (random choosed if multiple provided) than default `endpoint`.
			client (str, Optional) : Custom client to be used than default `client`.
			labled (bool, Optional): Method return either labled or indexed json to be used than default `method`.
			proxy (str, optional)  : Proxy to be used like `http://user:pass@ip:port`.

		"""
		self.__ioses  = None
		self.__tld    = tld or ''
		self.endpoint = config.tdlpoint if tld else endpoint or config.endpoint
		self.client   = client or config.client
		self.__method = config.method[int(minimal)]
		self.__labled = int(labled)
		self.proxy    = {re.match(r'^(http|https)://',proxy).group(1) : proxy} if proxy and re.match(r'^(http|https)://',proxy) else None

	def translate(self, text: str, to_lang: str, from_lang: str = 'auto', i_enc: str = 'UTF-8', o_enc: str = 'UTF-8', web: bool = False) -> Translation:
		"""Translate given text to target langauge.
		
		Args:
			text (str): Text to be translated.
			to_lang (str): Target language code to be translated.
			from_lang (str, Optional): Source langauge code to be translated.
			i_enc (str, Optional): Input encoding.
			o_enc (str, Optional): Onput encoding.
			web (bool, Optional) : Uses (scrap) mini version of google translate web instead of api.
		
		Returns:
			Translation (obj): Result class object of translation.

		Raises:
			FloodError: If google translation api gives http 503.
			ConfigError: If `endpoint` or `client` is invalid.
			InvalidLanguage: If given `to_lang` or `from_lang` is an unlisted language code.
		
		"""
		
		cfgvar = {
			'q' : text,
			'hl' : 'en',
			'sl' : from_lang,
			'tl' : to_lang,
			'dt' : ['t','at','rm'],
			'ie' : i_enc,
			'oe' : o_enc,
			'sp' : 'pbmt',
			'dj' : self.__labled,
			'client' : self.client
		}
		result = self.__request('https://{endpoint}{tld}/{method}'.format(
				endpoint = random.choice(self.endpoint) if type(self.endpoint) == list else self.endpoint,
				tld = random.choice(self.__tld) if type(self.__tld) == list else self.__tld,
				method   = 'm' if web else '%s_a/%s' % (config.key[1], self.__method)
			),
			var   = self.__isvalid(cfgvar), 
			proxy = self.proxy
		)
		return Translation(self.__parsets(result) if web else json.loads(result))
	
	def tts(self, text: str, lang: str, download: Union[str, bool, io.BytesIO] = './', slow: bool = False,  i_enc: str = 'UTF-8') -> TextToSpeech:
		"""Converts given Text to speech in target langauge.
		
		Args:
			text (str): Text to be converted.
			lang (str): Target language code to be converted.
			download (str, Optional) : Downloads to a specified path.
			slow (bool, Optional) : Slow down the speech.
			i_enc (str, Optional): Input encoding.
			
		Returns:
			TextToSpeech (obj): Result class object of tts.

		Raises:
			FloodError: If google translation api gives http 503.
			ConfigError: If `endpoint` or `client` is invalid.
			InvalidLanguage: If given `lang` is an unlisted language code.
		
		"""

		cfgvar = {
			'q' : text,
			'ie' : i_enc,
			'hl' : 'en',		
			'tl' : lang,
			'client': self.client or 'tw-ob',
			'ttsspeed': 1.-slow or .3,
			'total' : 1,
            'idx': 0,
		}
		result = self.__request('https://{endpoint}{tld}/{method}'.format(
				endpoint = random.choice(self.endpoint) if type(self.endpoint) == list else self.endpoint,
				tld = random.choice(self.__tld) if type(self.__tld) == list else self.__tld,
				method   = '%s_tts' % config.key[1],
			),
			var   = self.__isvalid(cfgvar), 
			proxy = self.proxy,
			full  = True
		)

		return TextToSpeech({'lang' : lang, 'text' : text, 'file' : self.__savetts(download, result.content) or result.url})
	
	def iso(self, full: bool = False) -> dict:
		"""Lists all supported iso langauge codes for both google translate (gts) and text2speech (tts).
		
		Returns:
			langs (dict of list[str]) : Having both `gts` and `tts`.
		
		"""
		return {'gts' : config.supported_gts_lang if full else config.supported_gts_lang.values(), 'tts' : config.supported_tts_lang}

	def __isvalid(self, var: dict) -> dict:
		"""Validates var
		
		Args:
			var (dict): Var to be validated,
		
		"""

		if not var['q']: 
			raise ValueError("Text can't be empty")
		if not var.get('sl') and var['tl'] not in config.supported_tts_lang:
			raise errors.InvalidLanguage("Unlisted target language code given. tts")
		if var.get('tl') and var['tl'] not in config.supported_gts_lang.values(): 
			raise errors.InvalidLanguage("Unlisted target language code given. gts")
		if var.get('sl') and var['sl'] not in config.supported_gts_lang.values() and var['sl'] != 'auto':
			raise errors.InvalidLanguage("Unlisted source language code given. gts")

		return var


	def __parsets(self, content: str) -> dict:
		"""Parses translation from content
		
		Args:
			content (str): Content from which to be extracted.
		
		"""

		match = re.search(r"aria-label=\"Source text\".+value=\"(.*)\"><div class=\"translate-button-container\">.+<div class=\"result-container\">(.*)</div><div class=\"links-container\">", content, re.MULTILINE)
		result = {}
		if match:
			result = {
				'src' : match.group(1),
				'sentences' : [{'trans' : match.group(2)}]
			}
		return result
	
	def __savetts(self, path: Union[str, bool, io.BytesIO], payload: Union[bytes, str]):
		"""Saves tts to local file
		
		Args:
			path (str): Path to save file.
			payload (byte): Content of the tts output.
		
		"""
		
		if type(path) == io.BytesIO:
			path.write(payload)
		elif path or path == None:
			paths = path.rsplit('/', 1)
			if len(paths)> 1:
				os.makedirs(paths[0], exist_ok=True)
			if len(paths)> 1 and not paths[1]:
				path += 'text2speech.mp3'
			open(path, 'wb').write(payload)
		else:
			path = False
		
		return path

	def __request(self, url: str, var: dict, proxy: dict, full: bool = False) -> dict:
		"""Request to google translator api
		
		Args:
			var (dict): Configuration arguemnts for translator.
		
		"""

		self.__ioses = self.__ioses or requests.Session()
		response = self.__ioses.get(url, params = var, proxies = proxy, headers = config.headers)

		if response.status_code == 200:
			return response if full else response.content.decode('UTF-8')
		
		elif response.status_code in [404, 403, 408, 504]:
			raise errors.ConfigError('Invalid endpoint url or client given.')
		
		elif response.status_code in [503]:
			raise errors.FloodError('Too many requests please try later.')
		
		else:
			response.raise_for_status()
