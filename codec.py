import struct
import bitcask_file

"""
simplified on-disk data representation
 _________________________________________________
|           |            |           |            |
| key size  | value size |   key     |    value   |
|___________|____________|___________|____________|


METADATA_STRUCT defines the types and byte-order 
of the fixed-size fields of the above record.

In this simplified version, those are just the key
size and the value size.

The struct module uses this to convert to and from
a binary encoding of the data.

> -> big endian
q -> long long (8 byte integer)

https://docs.python.org/3/library/struct.html
"""
METADATA_STRUCT = ">qq"
METADATA_BYTE_SIZE = 16 # 2 * 8 bytes

def encode(record):
	# 64 bit integers
	key_size = record.keysize
	value_size = record.valuesize

	# variable length strings
	key = record.key
	value = record.value

	metadata = struct.pack(METADATA_STRUCT, key_size, value_size)
	data = key.encode() + value.encode()
	record_bytes = metadata + data
	return record_bytes

def decode(data):
	(ksize, vsize) = struct.unpack(METADATA_STRUCT, data[:METADATA_BYTE_SIZE])
	string_data = data[METADATA_BYTE_SIZE:]
	key = string_data[:ksize]
	value = string_data[ksize:]
	return bitcask_file.Record(ksize, vsize, key, value)

