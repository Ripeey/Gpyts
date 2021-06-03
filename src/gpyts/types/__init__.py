#MIT License
#Copyright (c) 2021 Ripe

from typing import Union

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
			try: self.text = result['sentences'][0]['trans']
			except (KeyError, IndexError): pass
			try: self.origin = result['sentences'][0]['orig']
			except (KeyError, IndexError): pass
			try: self.translit = result['sentences'][1]['src_translit']
			except (KeyError, IndexError): pass
			try: self.confidence = result['confidence']
			except (KeyError, IndexError): pass
			try:
				for phrase in result['alternative_translations'][0]['alternative']: self.alternative.append(phrase['word_postproc'])
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
