import asyncssh
import asyncio
from _SSH import Abstract_SSH
from aioconsole import ainput
import pickle


class Client(Abstract_SSH):
    def __init__(self, reader, writer, name):
        super().__init__(reader, writer, name)

    async def run(self):
        tasks = asyncio.gather(self.watch_reader(), self.watch_writer())
        await tasks

    # Overloaded because the default behavior sends a dict
    # and here we only want to send a string
    async def watch_writer(self):
        while True:
            line = await ainput()
            self.writeline(line)

    # Opens a connection to the server, and using that connection opens a session
    # where data can be sent and retrieved. The socket is opened with no encoding,
    # which means all data will be sent as bytes.
    # This means bytes() objects don't need any converting
    @staticmethod
    async def start_client(host, port, username="user123", password="password"):
        # Open connection
        connection, client = \
            await asyncssh.create_connection(Client.SSHClient, host, port,
                username=username, password=password, known_hosts=None)

        # Open session. We'll obtain a reader and writer
        # (and optionally a second reader for stderr)
        # Another way, which uses the session factory below:
        # channel, session = await connection.create_session(Client.SSHClientSession)
        # Since is the SSH client, stdin is the session input, where the client writes into
        # and stdout is where the session writes output into and the client reads it
        writer, reader, _ = await connection.open_session(encoding=None)
        client = Client(reader, writer, username)
        await client.run()


    class SSHClientSession(asyncssh.SSHClientSession):
        def data_received(self, data, datatype):
            print(data, end='')

        def connection_lost(self, exc):
            if exc:
                print('SSH session error: ' + str(exc))


    class SSHClient(asyncssh.SSHClient):
        def connection_made(self, conn):
            print('Connection made to %s.' % conn.get_extra_info('peername')[0])

        def auth_completed(self):
            print('Authentication successful.')

