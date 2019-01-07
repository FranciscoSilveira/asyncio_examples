import asyncio
import asyncssh
from SSHServer import Server
from SSHClient import Client


async def main():
    while True:
        port_str = await ainput("What is my port?\n> ")
        try:
            port = int(port_str)
            if port not in range(1024, 65535):
                raise ValueError
            break
        except ValueError:
            print("Invalid port number")

    mode = await ainput("Am I a server [s/S] or a client [c/C]?\n> ")

    if mode in ["C", "c"]:
        remote = await ainput("What local port should I connect to? \n> ")
        host = "localhost"
        port = int(remote)
        await Client.start_client(host, port)

    elif mode in ["S", "s"]:
        try:
            await Server.start_server(port)
        except (OSError, asyncssh.Error) as exc:
            sys.exit("Error starting server: " + str(exc))


if __name__ == "__main__":
    from aioconsole import ainput
    import sys

    loop = asyncio.get_event_loop()
    server_key_filename = "/home/francisco/.ssh/id_rsa"
    authorized_keys_filename = "/home/francisco/.ssh/authorized_keys"
    print('Let\'s start...')

    loop.run_until_complete(main())
    loop.run_forever()
