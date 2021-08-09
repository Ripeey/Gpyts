#MIT License
#Copyright (c) 2021 Ripe

from typing import Union
import json
class Translation():
	"""A Result class for post `translation`.

	Attributes:
		src (str): Detected language which is translated from.
		text (str): Translated text.
		origin (str): Original text.
		translit (str): (Optional) If transliteration pharse is available.
		confidence (float): Confidence value of translation.
		alternative (list of str): (optional) If alternative translations are available.
		
	
	"""

	src = None
	text = None
	origin = None
	translit = None
	confidence = None
	alternative = list()
	

	def __init__(self, result : Union[list, dict]) -> None:
		"""result (dict): Json decoded dict from google translation `result`."""
		if type(result) == list:
			self.src = result[2]
			try: 
				if result[5]:
					self.text = ''.join([(sentence[2][-1][0] if sentence[2] else sentence[0]) for sentence in result[5]]) or None
				else:
					self.text = ''.join([(sentence[0] or '') for sentence in result[0]]) or None
			except IndexError: pass
			try: self.origin = ''.join([(sentence[1] or '') for sentence in result[0]]) or None
			except IndexError: pass
			try: self.translit = result[0][-1][3]
			except IndexError: pass
			self.confidence = result[6]
			try: 
				if result[5]:
					for _ in range(len(result[5][0][2])-1):
						text = ''
						for sentence in result[5]:
							try:
								text += sentence[2][_][0] if sentence[2] else sentence[0]
							except IndexError:
								text += sentence[2][0][0] if sentence[2] else sentence[0]
						if text: self.alternative.append(text)
			except IndexError: pass
		
		else:
			self.src = result.get('src')
			try: 
				if result.get('alternative_translations', []):
					text = ''
					for sentence in result['alternative_translations']:
						text += sentence['alternative'][-1]['word_postproc'] if sentence.get('alternative') else sentence['src_phrase']
					self.text = text or None
				else:
					self.text = ''.join([sentence.get('trans','') for sentence in result['sentences']]) or None
			except (KeyError, IndexError): pass
			try: self.origin = ''.join([sentence.get('orig','') for sentence in result['sentences']]) or None
			except (KeyError, IndexError): pass
			try: self.translit = result['sentences'][-1].get('src_translit',None) or result['sentences'][-1].get('translit',None)
			except (KeyError, IndexError): pass
			try: self.confidence = result['confidence']
			except (KeyError, IndexError): pass
			try:
				if result.get('alternative_translations', []):
					for _ in range(len(result['alternative_translations'][0]['alternative'])-1):
						text = ''
						for sentence in result['alternative_translations']:
							if sentence.get('alternative'):
								try:
									text += sentence['alternative'][_]['word_postproc']
								except (KeyError, IndexError):
									text += sentence['alternative'][0]['word_postproc']
							else:
								text += sentence['src_phrase']
						if text: self.alternative.append(text)
			except (KeyError, IndexError): pass

class TextToSpeech():
	"""A Result class for post `tts`.

	Attributes:
		lang (str): Language which is spoken from.
		text (str): Payload text.
		file (str, io.BytesIO): Buffer if provided or Path to file if downloaded. 
	
	"""

	lang = None
	text = None
	file = None

	def __init__(self, result: dict) -> None:
		self.lang = result.get('lang')
		self.text = result.get('text')
		self.file = result.get('file')
