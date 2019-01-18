from aioconsole import ainput
import pickle
import json


class BaseSSH:
    def __init__(self, stdin, stdout, name=None):
        self.stdin = stdin
        self.stdout = stdout
        self.name = name
        self.encoding = "utf-8"
        self.separator = "|".encode(self.encoding)

    # Abstract coroutine that both the Client and Server should implement
    async def run(self):
        raise NotImplemented

    # Receives any JSON-able object (dict, array)
    # Converts it to a JSON string, encodes that string and sends
    # through the channel the resulting size in an encoded string bytes,
    # a separator and the encoded JSON
    def write(self, object):
        payload = json.dumps(object).encode(self.encoding)
        size = str(len(payload)).encode(self.encoding)
        self.stdout.writelines([size, self.separator, payload])

    # Read the data until the header separator, then strip it
    # Interpret the read data as a number which is the message size
    # Read that length and interpret the data as a Python object
    async def read(self):
        data = await self.stdin.readuntil(self.separator)
        data = data.rstrip(self.separator) # non-destructive method
        size = int(data.decode(self.encoding))
        payload = await self.stdin.read(size)
        object = json.loads(payload.decode(self.encoding))
        return object

    # Read the socket until there is data,
    # then print it
    async def watch_reader(self):
        while True:
            object = await self.read()
            if not dict:
                return
            yield object
