import asyncio
from threading import Thread

class Worker(Thread):
    def __init__(self):
        super( type(self) ).__init__()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    worker = Worker()
    