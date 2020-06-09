'''
The program contain the client operation and connection 
to the server
-------
when the connection is set-up between the server 
and the client the commands that are entered by the user
gets executed
'''
import asyncio

async def Client():
    '''
    this client function is used to set-up connection between
    the client and the server
    '''
    read, write = await asyncio.open_connection(
        '127.0.0.1', 8080)
    command = ''
    while True:
        message = input('***Enter your command***:')
        write.write(message.encode())
        data = await read.read(4096)
        print("Recived Data:")
        print(data.decode())
        if command == "quit":
            print('***connection closed***')
            write.close()
            break
        if command == "":
            print("***Invalid Command***")
            continue

asyncio.run(Client())
