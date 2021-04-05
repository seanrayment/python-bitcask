# python-bitcask

Python implementation of a [bitcask](https://github.com/basho/bitcask/blob/develop-3.0/doc/bitcask-intro.pdf) inspired KV store.

Keys are stored in a in-memory hash table (python dictionary). Each key maps to an entry indicating where the value can be found on disk, in a single seek.

**Disclaimer**: Not for production use. I implemented this project for educational purposes after hearing about it in Chapter 3 of Designing Data Intensive Applications.

Currently implemented features:
- [x] PUT item
- [x] GET item
- [x] DELETE item
- [x] Rebuild hash table from data files after crash
- [ ] CRC checksums for data integrity
- [ ] merge data files (more efficient storage)
- [ ] Rebuild hash table faster from hint files
- [ ] CLI

##  Usage

```python
>> from bitcask import BitCask
>> bcask = BitCask("db")
>> bcask.put("message", "Hello, World!")
>> bcask.get("message")
'Hello, World!"
```
