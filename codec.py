import struct

"""
on-disk data representation
 _________________________________________________
|           |            |           |            |
| key size  | value size |   key     |    value   |
|___________|____________|___________|____________|

"""

'''
Defines the types and byte-order of the metadata in an entry
for encoding to and decoding from binary date.

> -> big endian
q -> long long (8 byte unsigned integer)

https://docs.python.org/3/library/struct.html
'''
METADATA_STRUCT = ">qq"
METADATA_BYTE_SIZE = 16 # 2 * 8 bytes

def encode(record):
	# 64 bit integers
	key_size = record["key_size"]
	value_size = record["value_size"]

	# variable length strings
	key = record["key"]
	value = record["value"]

	metadata = struct.pack(METADATA_STRUCT, key_size, value_size)
	data = key.encode() + value.encode()
	record_bytes = metadata + data
	return record_bytes

def decode(data):
	(ksize, vsize) = struct.unpack(METADATA_STRUCT, data[:METADATA_BYTE_SIZE])
	string_data = data[METADATA_BYTE_SIZE:]
	key = string_data[:ksize]
	value = string_data[ksize:]
	return (ksize, vsize, key, value)

