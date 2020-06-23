#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Sound.py
MIT License (c) Faure Systems <dev at faure dot systems>

Sound play audio with aplay (until it ends).
'''

import os, subprocess
	
class Sound:

	#__________________________________________________________________
	def __init__(self, logger=None):
		super().__init__()

		self._logger = logger
		self._file = None
		self._player = None

	#__________________________________________________________________
	def play(self, file):
		if self.isPlaying():
			return
			
		if os.path.exists(file):
			self._file= file
			try:
				self._player = subprocess.Popen(
					['aplay', file],
					stdout=subprocess.DEVNULL,
					stderr=subprocess.DEVNULL)
			except Exception as e:
				if self._logger:
					self._logger.error("Sound API : failed to load file")
					self._logger.debug(e)
			if self._logger:
				self._logger.info("{} {}".format("Sound API : playing", file))
		else:
			self._file= None
			if self._logger:
				self._logger.info("{} {}".format("Sound API : file not found", file))

	#__________________________________________________________________
	def isPlaying(self):
		if self._player is not None:
			self._player.poll()
			if self._player.returncode is None:
				return  True
			else:
				return False
		else:
			return False
