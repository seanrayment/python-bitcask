from bitcask_file import File
import os
from keydir import KeyDir
import codec
import struct

TOMBSTONE_VALUE = 'd49200c8-0a26-4f00-b4f0-7a9dffe0e288'

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
        """
        rebuild keydir in memory from existing db by reading through every
        file and adding keys that we've never seen or are newer than the key
        """
        for filename in os.listdir(self.dir):
            with open(f'{self.dir}/{filename}', 'rb') as f:
                file = File(self.dir, filename, 0)
                self.filemap[file.filename] = file
                while(True):
                    curr_offset = file.offset
                    r = file._load_next_record()
                    if (r):
                        entry = self.keydir.get(r.key)
                        if entry and r.timestamp > entry.timestamp and r.value != TOMBSTONE_VALUE:
                            # key exists but record we found is newer
                            size = file.offset - curr_offset
                            self.keydir.put(file.filename, r.timestamp, r.key, r.value, curr_offset, size)
                        elif entry and r.timestamp > entry.timestamp and r.value == TOMBSTONE_VALUE:
                            self.keydir.delete(r.key)
                        elif (not entry) and r.value != TOMBSTONE_VALUE:
                            # add new key to the keydir
                            size = file.offset - curr_offset
                            self.keydir.put(file.filename, r.timestamp, r.key, r.value, curr_offset, size)
                    else:
                        break

    def put(self, key, value):
        (timestamp, offset, size) = self.active_file.write(key, value)
        self.keydir.put(self.active_file.filename,
                        timestamp, key, value, offset, size)

    def get(self, key):
        entry = self.keydir.get(key)
        if entry:
            return self.filemap[entry.file_id].read(entry.pos, entry.size).decode()

    def delete(self, key):
        self.keydir.delete(key)
        self.active_file.write(key, TOMBSTONE_VALUE)
