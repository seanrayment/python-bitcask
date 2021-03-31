class KeyDir:
    """
    Stores a map of all the keys stored in the bitcask instance to their most
    recent item
    """

    def __init__(self):
        self.items = {}

    def put(self, file, k, v, offset, size):
        self.items[k] = KeyDirItem(file, v, offset, size)

    def get(self, k):
        return self.items[k]


class KeyDirItem:
    """
    The value type of a KeyDir entry.
     __________________________________
    |         |            |           |
    | File ID | value size | value pos |
    |_________|____________|___________|

    """

    def __init__(self, file, v, offset, size):
        self.file_id = file
        self.value = v
        self.size = size
        self.pos = offset
