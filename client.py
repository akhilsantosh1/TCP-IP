import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)
    message = ''
    while True:
        message = input('[Enter Message]\n')
        if message == 'exit':
            break

        writer.write(message.encode())
        data = await reader.read(100)
        print(f'Received: {data.decode()}')
    print('Close the connection')
    writer.close()


asyncio.run(tcp_echo_client())