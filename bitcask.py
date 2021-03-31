import uuid
from bitcask_file import File
import os
from keydir import KeyDir

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
		self.keydir = KeyDir()

	def put(self, key, value):
		(offset, size) = self.active_file.write(key, value)
		self.keydir.put(self.active_file.filename, key, value, offset, size)

	def get(self, key):
		entry = self.keydir.get(key)
		if entry:
			return self.active_file.read(entry.pos, entry.size).decode()