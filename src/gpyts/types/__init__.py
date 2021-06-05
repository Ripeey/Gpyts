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
			try: self.text = result[0][0][0]
			except IndexError: pass
			try: self.origin = result[0][0][1]
			except IndexError: pass
			try: self.translit = result[0][1][3]
			except IndexError: pass
			self.confidence = result[6]
			try: 
				for pharse in result[5][0][2]: self.alternative.append(pharse[0])
			except IndexError: pass
		
		else:
			self.src = result.get('src')
			try: 
				if result.get('alternative_translations', []):
					self.text = ''.join([sentence['alternative'][-1]['word_postproc'] for sentence in result['alternative_translations']]) or None
				else:
					self.text = ''.join([sentence['trans'] for sentence in result['sentences']]) or None
			except (KeyError, IndexError): pass
			try: self.origin = ''.join([sentence['orig'] for sentence in result['sentences']]) or None
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
							text += sentence['alternative'][_]['word_postproc']
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
