import asyncio
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    message = f"{addr} is connected !!!!"
    print(message)
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        if message == 'exit':
            break

        print(f"Received {message} from {addr}")
        print(f"Send: {message}")
        writer.write(data + '\n'.encode())
        await writer.drain()
    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())