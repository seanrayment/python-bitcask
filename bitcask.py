import uuid
from bitcask_file import File
import os

class BitCask:
	_instance = None

	def __new__(cls, dir):
		if cls._instance is None:
			cls._instance = super(BitCask, cls).__new__(cls)
			cls._instance.setup(dir)
		return cls._instance

	def setup(self, dir):
		self.dir = dir
		os.makedirs(self.dir, exist_ok=True)
		self.active_file = File(self.dir)
