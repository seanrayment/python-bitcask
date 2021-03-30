class BitCask:
	_instance = None

	def __new__(cls, dir):
		if cls._instance is None:
			cls._instance = super(BitCask, cls).__new__(cls)
			cls._instance.setup(dir)
		return cls._instance

	def setup(self, dir):
		print(f'Initializing bitcask db in {dir}')
