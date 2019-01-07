from aioconsole import ainput
import pickle


class Abstract_SSH:
    def __init__(self, stdin, stdout, name=None):
        self.stdin = stdin
        self.stdout = stdout
        self.name = name
        self.separator = b'|'

    # Abstract coroutine that both the Client and Server should implement
    async def run(self):
        pass

    def writeobj(self, message, sender=None):
        dict = {
            "name" : sender if sender else self.name,
            "message" : message
        }
        data = pickle.dumps(dict)
        size = pickle.dumps(len(data))
        self.stdout.writelines([size, self.separator, data])

    # Writes a string into the socket
    def writeline(self, message):
        data = pickle.dumps(message) # .encode()
        size = pickle.dumps(len(data))
        self.stdout.writelines([size, self.separator, data])

    # Read the data until the header separator, then strip it
    # Interpret the read data as a number which is the message size
    # Read that length and interpret the data as a Python object
    async def readobj(self):
        data = (await self.stdin.readuntil(self.separator))
        data = data.rstrip(self.separator) # non-destructive method
        size = pickle.loads(data)
        data = await self.stdin.read(size)
        dict = pickle.loads(data)
        return dict

    # Read the socket until there is data,
    # then print it
    async def watch_reader(self):
        while True:
            dict = await self.readobj()
            if not dict:
                break
            print("[{}] {}".format(dict["name"], dict["message"]))

    # Read the user's input until there is data,
    # then send it through the socket
    async def watch_writer(self):
        while True:
            line = await ainput()
            self.writeobj(line)
