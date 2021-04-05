import struct
import bitcask_file
from collections import namedtuple

"""
simplified on-disk data representation
 _____________________________________________________________
|             |            |            |           |         |
|  timestamp  | key size   | value size |   key     |  value  |
|_____________|____________|____________|___________|_________|


METADATA_STRUCT defines the types and byte-order
of the timestamp, keysize, and valuesize fields.

The struct module uses this to convert to and from
a binary encoding of the data.

> -> big endian
q -> long long (8 byte integer)

https://docs.python.org/3/library/struct.html
"""
METADATA_STRUCT = ">dqq"
METADATA_BYTE_SIZE = 24  # 3 * 8 bytes

def encode(record):
    # 64 bit integers
    key_size = record.keysize
    value_size = record.valuesize
    timestamp = record.timestamp

    # variable length strings
    key = record.key
    value = record.value

    metadata = struct.pack(METADATA_STRUCT, timestamp, key_size, value_size)
    data = key.encode() + value.encode()
    record_bytes = metadata + data
    return record_bytes

def decode_metadata(data):
    (timestamp, keysize, valuesize) = struct.unpack(METADATA_STRUCT, data)
    return (timestamp, keysize, valuesize)

def decode(data):
    (timestamp, ksize, vsize) = decode_metadata(data[:METADATA_BYTE_SIZE])
    string_data = data[METADATA_BYTE_SIZE:]
    key = string_data[:ksize]
    value = string_data[ksize:]
    return bitcask_file.Record(timestamp, ksize, vsize, key, value)
