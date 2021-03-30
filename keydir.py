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

	def put(self, k:, v:)
		self.items[k] = KeyDirItem(k: k, v: v)

	def get(self, k)
		return self.items[k]

class KeyDirItem:
	"""
	The value type of a KeyDir entry.

     _______________________________________________________
	|     |           |          |            |     |       |
	| CRC | timestamp | key size | value size | key | value |
	|_____|___________|__________|____________|_____|_______|
	
	"""

	def __init__(self, k:, v:):
		self.key = k.encode()
		self.value = v.encode()
		self.checksum = Checksum32.calc(self.value.encode())
		self.timestamp = int(time.time())