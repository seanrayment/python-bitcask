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
                    if (record):
                        entry = self.keydir.get(record.key)
                        if entry and record.timestamp > entry.timestamp:
                            # key exists but record we found is newer
                            size = file.offset - curr_offset
                            self.keydir.put(file.filename, r.timestamp, r.key, r.value, curr_offset, size)
                        elif (not entry):
                            # add new key to the keydir
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
