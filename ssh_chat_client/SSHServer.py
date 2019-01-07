import asyncssh
import sys
from _SSH import Abstract_SSH
import pickle


class Server(Abstract_SSH):
    _clients = []

    def __init__(self, stdin, stdout, name):
        super().__init__(stdin, stdout, name)

    async def run(self):
        print("Entered run")
        self.writeobj("Welcome to my server, {}!".format(self.name))
        self.writeobj("{} other clients are connected".format(len(self._clients)))
        self.broadcast("*** {} has entered the room ***".format(self.name))
        self._clients.append(self)
        await self.watch_reader()
        self.broadcast("*** {} has left the room ***\n".format(self.name))
        self._clients.remove(self)

    # This gets overloaded since we don't just want to print a line,
    # but broadcast it to everyone else
    async def watch_reader(self):
        try:
            while True:
                line = await self.readobj() # )["message"]
                print("[{}] {}".format(self.name, line))
                self.broadcast(line)
        except asyncssh.BreakReceived:
            print("Some weird exception")

    def broadcast(self, message):
        for client in self._clients:
            if client != self:
                client.writeobj(message, sender=client.name)

    @staticmethod
    async def handle_session(stdin, stdout, stderr):
        print("Inside session handler")
        name = stdin.get_extra_info("username")
        server = Server(stdin, stdout, name)
        await server.run()

    @staticmethod
    async def start_server(port):
        await asyncssh.create_server(Server.SSHServer, "localhost", port,
                server_host_keys=["./keys/server_rsa"],
                session_factory=Server.handle_session,
                session_encoding=None)


    class SSHServer(asyncssh.SSHServer):
        passwords = {"guest": "",  # guest account with no password
                     "user123": "password"
                     }
        def session_requested(self):
            return True

        def connection_requested(self):
            return True

        def connection_made(self, conn):
            print('SSH connection received from %s.' %
                  conn.get_extra_info('peername')[0])

        def connection_lost(self, exc):
            if exc:
                print('SSH connection error: ' + str(exc), file=sys.stderr)
            else:
                print('SSH connection closed.')

        def begin_auth(self, username):
            # If the user's password is the empty string, no auth is required
            return self.passwords.get(username) != ''

        def password_auth_supported(self):
            return True

        def validate_password(self, username, password):
            pw = self.passwords[username]
            #return crypt.crypt(password, pw) == pw
            return pw == password

        def debug_msg_received(self, msg, lang, always_display):
            print("Message from client: {}".format(msg))