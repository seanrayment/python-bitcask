import time
import binascii

class File:
	"""
	Class representing a bitcask file, which is an append-only log 
	of key, value pairs and their associated metadata
	"""
	def __init__(self):
		pass

class FileRecord:
	"""
	Class representing a single record in a bitcask file

	 _____________________________________________________________________
	|         |            |           |            |         |           |
	|   crc   | timestamp  | key size  | value size |   key   |   value   |
	|_________|____________|___________|____________|_________|___________|
	
	"""

	def __init__(self, k, v):
		self.timestamp = str(time.time())
		self.key = k
		self.value = v
		self.key_size = len(self.key)
		self.value_size = len(self.value)
		self.crc = binascii.crc32(self.crc_data())

	def byte_data(self):
		return str(self.crc).encode() + self.crc_data()

	def crc_data(self):
		"""
		inefficiently converts everything to a string and encodes it as ascii
		and concatenates it all together for the crc
		"""
		return (
			self.timestamp.encode() + \
			str(self.key_size).encode() + \
			str(self.value_size).encode() + \
			self.key.encode() + \
			self.value.encode()
		)

