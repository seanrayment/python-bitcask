from crccheck.crc import Crc32
from crccheck.checksum import Checksum32
import time

class KeyDir:
	"""
	Stores a map of all the keys stored in the bitcask instance to their most
	recent item
	"""
	def __init__(self):
		self.items = {}

	def put(self, k:, v:, offset:)
		self.items[k] = KeyDirItem(v: v, offset:)

	def get(self, k)
		return self.items[k]

class KeyDirItem:
	"""
	The value type of a KeyDir entry.

     _______________________________________________
	|         |            |           |            |
	| File ID | value size | value pos | timestamp  |
	|_________|____________|___________|____________|
	
	"""

	def __init__(self, v:, offset:):
		self.file_id = # Global active file
		self.value = v
		self.value_size = len(v)
		self.offset = offset
		self.timestamp = int(time.time())