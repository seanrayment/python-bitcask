from bitcask_file import File
import os
from keydir import KeyDir
import codec
import struct


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
        self.filemap = {self.active_file.filename: self.active_file}
        self.keydir = KeyDir()
        self.populate_keys()

    def populate_keys(self):
        for filename in os.listdir(self.dir):
            with open(f'{self.dir}/{filename}', 'rb') as f:
                offset = 0
                while (True):
                    meta_bytes = f.read(codec.METADATA_BYTE_SIZE)
                    if meta_bytes:
                        (timestamp, ksize, vsize) = struct.unpack(
                            codec.METADATA_STRUCT, meta_bytes)
                        key_bytes = f.read(ksize)
                        value_bytes = f.read(vsize)
                        if key_bytes and value_bytes:
                            key = key_bytes.decode()
                            value = value_bytes.decode()
                            file_id = '/'.join([self.dir, filename])
                            entry = self.keydir.get(key)
                            if entry and timestamp > entry.timestamp:
                                self.keydir.put(
                                    file_id, timestamp, key, value, offset, codec.METADATA_BYTE_SIZE + ksize + vsize)
                            elif not entry:
                                self.keydir.put(
                                    file_id, timestamp, key, value, offset, codec.METADATA_BYTE_SIZE + ksize + vsize)
                            offset += codec.METADATA_BYTE_SIZE + ksize + vsize
                        else:
                            break
                    else:
                        break
                self.filemap['/'.join([self.dir, filename])
                             ] = File(self.dir, filename, offset)

    def put(self, key, value):
        (timestamp, offset, size) = self.active_file.write(key, value)
        self.keydir.put(self.active_file.filename,
                        timestamp, key, value, offset, size)

    def get(self, key):
        entry = self.keydir.get(key)
        if entry:
            return self.filemap[entry.file_id].read(entry.pos, entry.size).decode()
