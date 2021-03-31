import time
import uuid
import codec
from collections import namedtuple

"""
Represents a single record in a bitcask file
 _______________________________________________
|           |            |          |           |
| key size  | value size |   key    |   value   |
|___________|____________|__________|___________|

"""
Record = namedtuple('Record', ['keysize', 'valuesize', 'key', 'value'])

class File:
	"""
	Class representing a bitcask file, which is an append-only log 
	of key, value pairs and their associated metadata
	"""
	def __init__(self, dir):
		self.filename = '/'.join([dir, str(uuid.uuid4())])
		self.offset = 0

	def write(self, key, value):
		'''
		encode the data and append to the file
		'''
		keysize = len(key)
		valuesize = len(value)
		record = Record(keysize, valuesize, key, value)
		data = codec.encode(record)
		count = 0
		with open(self.filename, 'ab') as f:
			count = f.write(data)
		curr_offset = self.offset
		self.offset += count
		return (curr_offset, count)

	def read(self, pos, size):
		'''
		read bytes from the file and decode into record
		'''
		data = b''
		with open(self.filename, 'rb') as f:
			f.seek(pos, 0)
			data = f.read(size)
		return codec.decode(data).value
